# -*- coding: utf-8 -*-
import cookielib
import socket
import urllib2
from os import path

from utils import ShowMessage
from utils import Sleep


class CrawlException(Exception):
  def __init__(self, url):
    Exception.__init__(self, 'Failed to crawl page "%s" too many times.' % url)


class Connector:
  def __init__(self, referer, cookiepath, proxy='', agent='MSIE 7.0'):
    self._referer = referer
    self._cookiepath = cookiepath
    self._opener = None
    self._cookiejar = None
    self._proxies = None

    self.proxy = proxy
    self.agent = agent
    self.sockettimeout = 60
    self.spancrawlfailed = 10

    ##self._lock = threading.RLock()
    self.CreateOpener()

  def CreateOpener(self):
    socket.setdefaulttimeout(self.sockettimeout)

    if self._cookiepath:
      self._cookiejar = cookielib.MozillaCookieJar(self._cookiepath)
      if path.exists(self._cookiepath):
        self._cookiejar.load()
    if self.proxy:
      self._proxies = {'http':self.proxy}

    self._opener = urllib2.build_opener(
        urllib2.HTTPCookieProcessor(self._cookiejar),
        urllib2.ProxyHandler(self._proxies))
    self._opener.addheaders = [
        ('Referer', self._referer),
        ('User-Agent', self.agent),
        ]

  def SaveCookie(self):
    if self._cookiejar:
      self._cookiejar.save()

  def CrawlPage(self, url, data=None, retry=0):
    while True:
      ##self._lock.acquire()
      try:
        fobj = self._opener.open(url, data)
        content = fobj.read()
        fobj.close()
        return content
      except Exception, ex:
        ShowMessage('Failed to crawl page "%s": %s' % (url, ex))
      finally:
        pass
        ##self._lock.release()

      if retry > 0:
        retry -= 1
        Sleep(self.spancrawlfailed, 'Crawler')
      else:
        break

    raise CrawlException(url)
    return None
