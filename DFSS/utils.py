# -*- coding: utf-8 -*-
import htmllib
import os
import re
import sys
import time
import traceback
from os import path


SPACE_PATTERN = '&nbsp;|\s'
CLEAN_CONSOLE_LINE = '\r%78s\r' % ' '


def Unescape(text):
  p = htmllib.HTMLParser(None)
  p.save_bgn()
  p.feed(text)
  return p.save_end()


def RemoveAllSpaces(text):
  spaceRe = re.compile(r'%s' % SPACE_PATTERN, re.MULTILINE)
  return spaceRe.sub('', text)


def CollapsAllSpaces(text):
  spaceRe = re.compile(r'(%s)+' % SPACE_PATTERN, re.MULTILINE)
  return spaceRe.sub(' ', text)


def RemoveAllHtmlTags(text):
  tagRe = re.compile(r'<[^>]*>', re.MULTILINE)
  return tagRe.sub('', text)


def StripSpacesLeft(text):
  spaceRe = re.compile(r'^(%s)*' % SPACE_PATTERN, re.MULTILINE)
  return spaceRe.sub('', text)


def StripSpacesRight(text):
  spaceRe = re.compile(r'(%s)*$' % SPACE_PATTERN, re.MULTILINE)
  return spaceRe.sub('', text)


def StripSpaces(text):
  return StripSpacesLeft(StripSpacesRight(text))


def ClearSpaces(text):
  return CollapsAllSpaces(StripSpaces(text))


def CleanHtml(text):
  return Unescape(CollapsAllSpaces(RemoveAllHtmlTags(text)))


class ParseHtmlFailedException(Exception):
  def __init__(self, ex):
    Exception.__init__(self, 'Failed to parse html page content: %s' % ex)
    self.ex = ex


def ParseHtml(content
    , _charsetRe=re.compile(
      r'<meta [^>]*charset\s*=[\s\'"]*([\w-]+)', re.I)
    , _nbspRe=re.compile(
      r'&nbsp;', re.I)
    , _xmlRe=re.compile(
      r'^<\?xml version="1.0" encoding="[^"]+"\?>')
    ):
  if not content: return None

  from xml.dom import minidom
  import tidy
  m = _charsetRe.search(content)
  charset = None
  if m:
    charset = m.group(1)
    if charset.lower() != 'utf8' and charset.lower() != 'utf-8':
      content = content.decode(charset, 'ignore')
  if charset.lower() != 'utf8' and charset.lower() != 'utf-8':
    content = content.encode('utf8')
  options = dict(output_xml=1, add_xml_decl=1, show_warnings=1,
      indent=0, tidy_mark=0, wrap=0, quote_nbsp=1,
      force_output=1, hide_comments=1,
      input_encoding='utf8', output_encoding='utf8')
  txml = tidy.parseString(content, **options)
  l = len(str(txml))
  xmlcontent = str(txml)

  #TODO# The next two lines are not good solution.
  xmlcontent = _nbspRe.sub(' ', xmlcontent)
  xmlcontent = _xmlRe.sub('<?xml version="1.0"?>', xmlcontent)
  #f = open('testpage.xml', 'w')
  #f.write(xmlcontent)
  #f.close()

  try:
    return minidom.parseString(xmlcontent)
  except Exception, ex:
    raise ParseHtmlFailedException(ex)


def FindHtmlTag(root, tagName, onlyFirst=False, attrs=None):
  if not root:
    return (onlyFirst and [None] or [[]])[0]
  nodes = root.getElementsByTagName(tagName)
  return _DoFindHtmlTag(nodes, onlyFirst, attrs)


def FindChildTag(root, tagName, onlyFirst=False, attrs=None):
  if not root:
    return (onlyFirst and [None] or [[]])[0]
  nodes = [node for node in root.childNodes if node.nodeName == tagName]
  return _DoFindHtmlTag(nodes, onlyFirst, attrs)


def _DoFindHtmlTag(nodes, onlyFirst, attrs):
  attrRes = {}
  if attrs:
    for (key, val) in attrs.iteritems():
      attrRes[key] = re.compile(val)

  validNodes = []
  for node in nodes:
    isValid = True
    for (attr, attrRe) in attrRes.iteritems():
      if not node.hasAttribute(attr) or  \
          not attrRe.match(node.getAttribute(attr)):
        isValid = False
        break
    if not isValid: continue
    if onlyFirst: return node
    validNodes.append(node)

  if validNodes: return validNodes
  return (onlyFirst and [None] or [[]])[0]


def TruncateString(text, maxLen, encoding='gbk'):
  if not text: return text
  decoded = False
  if encoding:
    try:
      text = text.decode(encoding)
      decoded = True
    except Exception, ex:
      print ex
      pass
  text = len(text) > maxLen and ('%s...' % text[:maxLen]) or text
  if decoded:
    try:
      text = text.encode(encoding)
    except:
      pass
  return text


def ShowException(ex, msg=None, f=sys.stdout):
  #print CLEAN_CONSOLE_LINE,
  f.write(time.strftime('[%m-%d %H:%M:%S] ', time.localtime()))
  if msg: f.write('%s\n' % msg)

  if ex:
    traceback.print_exc()

  f.flush()


def ShowMessage(*args):
  #print args
  ShowException(None, ' '.join(['%s' % x for x in args]))


def ShowMessageEx(f, *args):
  ShowException(None, ' '.join(['%s' % x for x in args]), f)


def Sleep(sec, msg=''):
  if not sec: return
  print CLEAN_CONSOLE_LINE,
  print '[%s] [%s] Sleep %ss...' % (
      time.strftime('%H:%M:%S', time.localtime()), msg, str(sec)),
  print '\r',
  time.sleep(sec)
  #print CLEAN_CONSOLE_LINE,


def ConvStr2Time(s, format=None):
  formats = [format, '%Y-%m-%d %H:%M', '%Y-%m-%d']
  for i in xrange(len(formats)):
    try: return int(time.mktime(time.strptime(s, formats[i])))
    except: pass
  return 0


def CompareTime(ts1, ts2, format='%Y-%m-%d %H:%M'):
  '''Returns 1 if ts1 is older than ts2;
  Returns -1 if ts1 is newer than ts2'''
  tm1 = ConvStr2Time(ts1, format)
  tm2 = ConvStr2Time(ts2, format)

  if not tm1:
    return tm2 and 1 or 0
  if not tm2:
    return -1
  return tm1 > tm2 and -1 or (tm1 < tm2 and 1 or 0)


def ExecSysCmd(cmd):
  os.system(cmd)


class Enumerate(object):
  def __init__(self, names):
    for number, name in enumerate(names.strip().split()):
      setattr(self, name, name)
      #setattr(self, name, number)
