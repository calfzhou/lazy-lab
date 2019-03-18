# -*- coding: utf-8 -*-
import os
from os import path
import re
import sys
import time
import urllib
import urlparse
import threading
from threading import Thread

from dfssparams import *

import rsa
from seccode import InputSecCode
from seccode import DetectSecCode
import utils
from utils import ShowMessage
from utils import ShowMessageEx
from utils import ShowException
from utils import Sleep
from utils import Enumerate
from common import Connector


_VERSION = [0, 11, 1101, 1]

YUECHE_PUB_KEY = {'e': 15427, 'n': 2348001542405642579L}
DFSS_STATE = Enumerate(
    'SIGNIN_SUCCEED '
    'MONITOR_IDLE '
    'MONITOR_FINISH '
    'NEED_SIGNIN '
    'YUECHE_OFF '
    'YUECHE_OVERFLOW '
    'YUECHE_FINISH '
    )
SVM_PREDICT_EXE_FP = 'svm-predict'
SVM_MODEL_FP = 'dfssyanzheng.mdl'
#SVM_MODEL_FP = 'model.txt'


class MyException(Exception):
  def __init__(self, message):
    Exception.__init__(self, message.encode('gb2312'))


class DfssUser:
  def __init__(self, uid, pwd, sid, requests={}):
    verified = False
    try:
      msg = rsa.verify(sid.decode('base64'), YUECHE_PUB_KEY)
      verified = True
    except:
      verified = False

    self.uid = uid
    self.pwd = pwd
    self.requests = requests
    cookiepath = None #'cookie_%s.txt' % self.uid
    self.yuecheurl = YUECHE_URL #% self.uid
    self.viewstate = ''
    self.eventvalidation = ''
    self.connector = Connector(SITE_URL, cookiepath, proxy=CRAWLER_PROXY, agent=CRAWLER_AGENT)
    self.verified = verified

    self.InitRegex()

    self.datafolder = 'data_%s' % self.uid
    if not path.exists(self.datafolder):
      os.mkdir(self.datafolder)
    logpath = path.join(self.datafolder, 'log.txt')
    self._logf = open(logpath, 'w')#'a')
    ShowMessageEx(self._logf, "=============== User loaded%s ===============" % (verified and '.' or '!'))

  def InitRegex(self):
    self.__viewstateRe = re.compile(VIEWSTATE_PATTERN)
    self.__eventvalidationRe = re.compile(EVENTVALIDATE_PATTERN)
    self.__errorpageRe = re.compile(ERROR_PAGE_PATTERN)
    self.__errordetailRe = re.compile(ERROR_DETAIL_PATTERN)
    self.__badyanzhengRe = re.compile(WRONG_YANZHENG_PATTERN)
    self.__siteoffRe = re.compile(SITE_OFF_PATTERH)
    self.__loginsuccessRe = re.compile(LOGIN_SUCCESS_PATTERN)
    self.__yuecheoverflowRe = re.compile(YUECHE_OVERFLOW_PATTERN)
    self.__needsigninRe = re.compile(SESSION_CLOSED_PATTERN)
    self.__yuechepageRe = re.compile(YUECHE_PAGE_PATTERN)
    self.__sessionExpiredRe = re.compile(SESSION_EXPIRED_PATTERN)
    self.__yuechetableRe = re.compile(YUECHE_TABLE_PATTERN)
    self.__yuechetrRe = re.compile(YUECHE_TR_PATTERN)
    self.__yuechetdRe = re.compile(YUECHE_TD_PATTERN)
    self.__yuechedateRe = re.compile(YUECHE_DATE_PATTERN)
    self.__yuechebtnRe = re.compile(YUECHE_BUTTON_PATTERN)
    self.__stagedoneRe = re.compile(YUECHE_STAGEDONE_PATTERN)

  def Close(self):
    if self._logf and self._logf != sys.stdout:
      ShowMessageEx(self._logf, "=============== User closed. ===============")
      self._logf.close()
      self._logf = sys.stdout


  def GetViewState(self, content):
    m = self.__viewstateRe.search(content)
    if not m: return ''
    return m.group('value') #urllib.url2pathname(m.group(1))

  def GetEventValidation(self, content):
    m = self.__eventvalidationRe.search(content)
    if not m: return ''
    return m.group('value') #urllib.url2pathname(m.group(1))

  def RemoveRequest(self, date, hour, reason=''):
    if date in self.requests:
      if hour in self.requests[date]:
        del self.requests[date][hour]
        ShowMessage('Request %s:%s for user %s removed' % (date, hour, self.uid),
            reason and (', reason: %s.' % reason) or '.')
        ShowMessageEx(self._logf, 'Request %s:%s removed' % (date, hour),
            reason and (', reason: %s.' % reason) or '.')
        if len(self.requests[date]) == 0:
          del(self.requests[date])
        return
    raise MyException('%s:%s is not in request list for user %s' % (date, hour, self.uid))

  def LoadPage(self, url, data=None, isbinary=False):
    content = self.connector.CrawlPage(url, data)
    if isbinary:
      if not content:
        raise MyException('binary web content is empty')
      return content

    content = DecodeContent(content, SITE_ENCODING)

    if not content:
      raise MyException('web page is empty')
    if self.__errorpageRe.search(content):
      msg = 'ErrorPage: unknown'
      m = self.__errordetailRe.search(content)
      if m:
        msg = m.group('msg')
        #msg = utils.CleanHtml(msg.encode('gb2312'))
      raise MyException(msg)

    viewstate = self.GetViewState(content)
    if viewstate: self.viewstate = viewstate
    eventvalidation = self.GetEventValidation(content)
    if eventvalidation: self.eventvalidation = eventvalidation
    return content

  def SaveSecCode(self, imgfp):
    secimgcontent = self.LoadPage(SECIMG_URL, isbinary=True)
    f = open(imgfp, 'wb')
    f.write(secimgcontent)
    f.close()

  def Signin(self):
    content = self.LoadPage(SIGNIN_URL)
    imgfp = path.join(self.datafolder, 'yanzheng.gif')
    datafp = path.join(self.datafolder, 'yanzheng.data.txt')
    resultfp = path.join(self.datafolder, 'yanzheng.result.txt')
    yanzhengretry = YANZHENG_RETRY_COUNT
    while True:
      self.SaveSecCode(imgfp)
      if yanzhengretry > 0:
        yanzheng = DetectSecCode(imgfp, SVM_PREDICT_EXE_FP, datafp, SVM_MODEL_FP, resultfp)
        if not yanzheng:
          ShowMessage('Detect YanZheng code fail')
          yanzhengretry -= 1
          continue
        else:
          ShowMessage('YanZheng code detected: %s' % yanzheng)
      else:
        yanzheng = InputSecCode(imgfp)

      params = {
          #'__EVENTTARGET': '',
          #'__EVENTARGUMENT': '',
          '__VIEWSTATE': self.viewstate,
          '__EVENTVALIDATION': self.eventvalidation,
          'txtname': self.uid,
          'txtpwd': self.pwd,
          'yanzheng': yanzheng,
          'button.x': '36',
          'button.y': '13',
          }
      data = urllib.urlencode(params)
      #print data
      content = self.LoadPage(SIGNIN_URL, data)
      #print content

      m = self.__badyanzhengRe.search(content)
      if m:
        yanzhengretry -= 1
        if yanzhengretry < 0:
          raise MyException('Sign in failed: wrong YanZheng code')
        else:
          ShowMessage('YanZhang code (%s) is wrong' % yanzheng)
      else:
        break

    m = self.__loginsuccessRe.search(content)
    if m:
      content = self.LoadPage(self.yuecheurl)
      self.connector.SaveCookie()
      return DFSS_STATE.SIGNIN_SUCCEED

    m = self.__siteoffRe.search(content)
    if m:
      return DFSS_STATE.YUECHE_OFF

    raise MyException('Sign in failed')

  def Yueche(self, stage, btnname, btnvalue, date, hour):
    params = {
        #'__EVENTTARGET': '',
        #'__EVENTARGUMENT': '',
        '__VIEWSTATE': self.viewstate,
        '__EVENTVALIDATION': self.eventvalidation,
        'RadioButtonList1': stage,
        btnname: btnvalue,
        }
    data = urllib.urlencode(params)
    if not self.verified: return DFSS_STATE.YUECHE_FINISH
    content = self.LoadPage(self.yuecheurl, data)

    if self.__yuecheoverflowRe.search(content):
      return DFSS_STATE.YUECHE_OVERFLOW
    return DFSS_STATE.YUECHE_FINISH

  def MonitorYueche(self):
    if not self.requests:
      return DFSS_STATE.MONITOR_FINISH

    stageidx = DFSS_CURRENT_STAGE

    stage = DFSS_STAGES[stageidx].encode('utf8')
    params = {
        '__EVENTTARGET': '', #'RadioButtonList1$%d' % stageidx,
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': self.viewstate,
        '__EVENTVALIDATION': self.eventvalidation,
        'RadioButtonList1': stage,
        'btnRefresh': DFSS_REFRESH.encode('utf8'),
        }
    data = urllib.urlencode(params)

    try:
      content = self.LoadPage(self.yuecheurl, data)
    except MyException, ex:
      if self.__needsigninRe.search(ex.message):
        return DFSS_STATE.NEED_SIGNIN
      raise

    if self.__sessionExpiredRe.search(content):
      ShowMessage('Seems the session is expired, need sign in again')
      return DFSS_STATE.NEED_SIGNIN

    if not self.__yuechepageRe.search(content):
      #print content
      raise MyException('Failed to recognize yueche page')

    if self.__stagedoneRe.search(content):
      ShowMessage('User %s current stage (%s) finished.' % (self.uid, DFSS_STAGES[stageidx].encode('gb2312')))
      return DFSS_STATE.MONITOR_FINISH

    m = self.__yuechetableRe.search(content)
    if not m:
      raise MyException('No yueche table')
    #f = open('t.txt', 'w')
    #f.write(content.encode('gb2312'))
    #f.close()

    content = m.group('table')

    trs = self.__yuechetrRe.findall(content)
    if len(trs) < MIN_TR_COUNT:
      raise MyException('Not enough trs (%d)' % len(trs))

    prevtdcnt = 0
    for trid in xrange(len(trs)):
      tr = trs[trid]
      tds = self.__yuechetdRe.findall(tr)
      if not prevtdcnt:
        if len(tds) < MIN_TD_COUNT:
          raise MyException('Not enough tds (%d)' % len(tds))
      else:
        if len(tds) != prevtdcnt:
          raise MyException('Inconsistent number of tds (%d != %d)' % (len(tds), prevtdcnt))
      prevtdcnt = len(tds)

      m = self.__yuechedateRe.search(tds[0])
      if not m:
        raise MyException('No date in tr_%d' % trid)
      date = m.group('date')
      #week = m.group('week')
      if date not in self.requests: continue

      for tdid in xrange(1, len(tds)):
        if date not in self.requests: break

        m = self.__yuechebtnRe.search(tds[tdid])
        if not m:
          raise MyException('No yueche button in %s:%s' % (date, tdid))

        hour = m.group('hour')
        if hour not in self.requests[date]: continue

        if m.group('carid'):  # Already done
          self.RemoveRequest(date, hour, 'Already done: car id = %s' % m.group('value'))
        elif m.group('disabled'):  # Too late
          self.RemoveRequest(date, hour, 'Too late')
        elif m.group('value') == '0':  # Not availiable yet
          pass
        else:
          try:
            v = int(m.group('value'))
          except ValueError, ex:
            self.RemoveRequest(date, hour, 'no int value: %s' % ex.message)
            continue

          #ShowMessage('Yueche %s:%s, availiable: %s' % (date, hour, v))
          # yueche
          ShowMessage('Trying to yueche %s:%s for user %s.' % (date, hour, self.uid))
          try:
            state = self.Yueche(stage, m.group('name'), m.group('value'), date, hour)
            if state == DFSS_STATE.YUECHE_OVERFLOW:
              self.RemoveRequest(date, hour, 'Overflow')
            else:
              ShowMessage('Yueche %s:%s for user %s finished.' % (date, hour, self.uid))
              ShowMessageEx(self._logf, 'Yueche %s:%s finished.' % (date, hour))
          except MyException, ex:
            if self.__needsigninRe.search(ex.message):
              ShowMessage('Yueche %s:%s for user %s failed.' % (date, hour, self.uid))
              ShowMessageEx(self._logf, 'Yueche %s:%s failed.' % (date, hour))
            else:
              raise

    return DFSS_STATE.MONITOR_IDLE


def DecodeContent(content, encodings):
  if not content: return content
  if not encodings: return content
  if not isinstance(encodings, tuple): encodings = (encodings)

  for encoding in encodings:
    try:
      return content.decode(encoding)
    except Exception, ex:
      ShowMessage('Decode from %s fail:' % encoding, ex)
  return content


class YuecheHelper(Thread):
  def __init__(self, user):
    Thread.__init__(self, name='YuecheHelper')
    self._user = user

  def run(self):
    exceptionCount = 0
    while True:
      try:
        forceReSignIn = False
        if exceptionCount == MAX_EXCEPTION_COUNT:
          forceReSignIn = True
          exceptionCount = 0
          ShowMessage('Too many times of exceptions occurred in yueche loop, trying re-sign-in...')
        self.Yueche(forceReSignIn)
        self._user.Close()
        break
      except MyException, ex:
        exceptionCount += 1
        ShowMessage('Error in yueche loop for user %s:' % self._user.uid, ex)
        Sleep(IDLE_WHEN_MYEXCEPTION, 'MyException')
      except Exception, ex:
        exceptionCount += 1
        ShowException(ex, 'Error in yueche loop for user %s' % self._user.uid)
        Sleep(IDLE_WHEN_EXCEPTION, 'Exception')

  def Yueche(self, forceReSignIn):
    if forceReSignIn:
      state = self._user.Signin()
      ShowMessage('User %s %s' % (self._user.uid, state))

    while True:
      state = self._user.MonitorYueche()
      if state == DFSS_STATE.MONITOR_FINISH:
        ShowMessage('User %s all requests finished.' % self._user.uid)
        break
      elif state == DFSS_STATE.NEED_SIGNIN:
        ShowMessage('User %s need sign in' % self._user.uid)
        state = self._user.Signin()
        ShowMessage('User %s %s' % (self._user.uid, state))
        if state == DFSS_STATE.YUECHE_OFF:
          Sleep(IDLE_WHEN_YUECHE_OFF, 'YuecheOff')
        continue
      Sleep(IDLE_BETWEEN_MONITOR, '%sIdle' % self._user.uid)


def LoadUserAndRequest():
  users = []
  uids = set()
  f = open('request.txt')
  while True:
    line = f.readline()
    if not line: break
    line = line.strip()
    if not line: continue
    if line[0] == '#': continue

    items = line.split('\t')
    if len(items) != 3:
      print 'Ivalid user info "%s"' % line
      break
    uid = items[0]
    pwd = items[1]
    sid = items[2]

    while True:
      line = f.readline()
      if not line: break
      line = line.strip()
      if not line: continue
      if line[0] == '#': continue
      break
    if not line: break
    items = line.split('\t')
    requests = {}
    for item in items:
      subitems = item.split(':')
      date = subitems[0]
      hour = subitems[1]
      force = False
      if len(subitems) > 2:
        force = subitems[2].lower()
        if force in ('t', 'true', 'y', 'yes', '1'): force = True
        else: force = False
      if date not in requests:
        requests[date] = {}
      requests[date][hour] = force
    if uid in uids:
      print 'skip duplicated user id:', uid
      continue
    user = DfssUser(uid, pwd, sid, requests)
    print 'Load user %s%s\n%s' % (uid, (user.verified and ':' or ';'), requests)
    uids.add(uid)
    users.append(user)
  f.close()
  return users


def Main():
  print '\nDFSS YueChe Assist. Version = %s\n' % _VERSION
  users = LoadUserAndRequest()
  threads = [YuecheHelper(user) for user in users]
  print '\nStarting yueche threads ...'
  for i in xrange(len(threads)):
    threads[i].start()
    Sleep(3, 'StartThread')

  for i in xrange(len(threads)):
    threads[i].join()
  print '\nAll threads stopped.'
  print '\nPress <RETURN> to exit.',
  sys.stdin.readline()


if __name__ == '__main__':
  Main()
