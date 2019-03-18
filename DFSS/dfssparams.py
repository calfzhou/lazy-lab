# -*- coding: utf-8 -*-
import urlparse

CRAWLER_PROXY = ''
#CRAWLER_AGENT = 'Firefox/3.0.10'
#CRAWLER_AGENT = 'Chrome/6.0.472.59'
CRAWLER_AGENT = 'MSIE 7.0'

SITE_URL = 'http://114.251.109.215'
SIGNIN_URL = urlparse.urljoin(SITE_URL, '/WLYC/')
SECIMG_URL = urlparse.urljoin(SIGNIN_URL, 'image.aspx')
YUECHE_URL = urlparse.urljoin(SITE_URL, '/WLYC/aspx/car/XYYC22.aspx')
SITE_ENCODING = ('utf8', 'gb2312')

DFSS_HOURS = ('N/A', '7', '9', '13', '17', '19')
DFSS_STAGES = (u'模拟机', u'散段', u'综合训练')
DFSS_CURRENT_STAGE = 1  # 散段
DFSS_REFRESH = u'刷新'

VIEWSTATE_PATTERN = r'(?i)<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(?P<value>[^"]+)"\s*/>'
EVENTVALIDATE_PATTERN = r'(?i)<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(?P<value>[^"]+)"\s*/>'

ERROR_PAGE_PATTERN = ur'(?i)<title>\s*错误页面\s*</title>'
ERROR_DETAIL_PATTERN = ur'(?is)<body>\s*(?P<msg>.+?)\s*</body>'

WRONG_YANZHENG_PATTERN = ur'(?i)alert\("验证码错误！"\);'
SITE_OFF_PATTERH = ur"(?i)alert\('约车时间未到'\);"
LOGIN_SUCCESS_PATTERN = ur"(?i)window\.open\('aspx/car/XYYC22\.aspx"

YUECHE_OVERFLOW_PATTERN = ur'(?i)<script>alert\("您预约学时不能大于总学时!"\);'

SESSION_CLOSED_PATTERN = r'(?i)请刷新本页面，然后再尝试访问。'
YUECHE_PAGE_PATTERN = (ur'(?i)<td[^>]*>\s*<span[^>]*>\s*学员编号:</span></td>'
    ur'\s*<td[^>]*>\s*<span[^>]*>\s*<font[^>]*>\s*[0-9]+\s*</font></span></td>'
    )
YUECHE_STAGEDONE_PATTERN = (ur'(?i)<span[^>]*>提示信息：</span></td>\s*<td[^>]*>\s*'
    ur'<span[^>]*>(?:<font[^>]*>)?[^<]+已预约完毕(?:</font>)?</span>'
    )
SESSION_EXPIRED_PATTERN = ur'(?is)<tr align="center"[^>]*>\s*</tr>'
YUECHE_TABLE_PATTERN = ur'(?is)<table[^>]*? id="gv"[^>]*>\s*(?P<table>.+?)\s*</table>'
YUECHE_TR_PATTERN = ur'(?is)<tr align="center"[^>]*>\s*(.+?)\s*</tr>'
YUECHE_TD_PATTERN = ur'(?is)<td[^>]*>\s*(.*?)\s*</td>'
YUECHE_DATE_PATTERN = ur'(?i)(?P<date>20[0-9-]+)\((?P<week>[^(]+)\)'
YUECHE_BUTTON_PATTERN = (ur'(?i)<input type="submit" name="(?P<name>gv\$ctl0[0-9]\$I_HOUR(?P<hour>[0-9]+)_[0-9]+)"'
    ur' value="(?P<value>[0-9]+)(?P<carid>\s+)?"(?P<disabled> disabled="disabled")?.*? id="[^"]+"'
    )

YANZHENG_RETRY_COUNT = 5
MIN_TR_COUNT = 2
MIN_TD_COUNT = 3
MAX_EXCEPTION_COUNT = 10
IDLE_WHEN_MYEXCEPTION = 3
IDLE_WHEN_EXCEPTION = 10
IDLE_WHEN_YUECHE_OFF = 60
IDLE_BETWEEN_MONITOR = 3

#import re
#paramsRe = re.compile('^CRAWLER_|^DFSS_|^SITE_|_URL$|_PATTERN$')
#GLOBAL_PARAMS = '\n'.join(
#    ['global %s' % x for x in dir() if paramsRe.search(x)])

from os import path
CUSTOMIZED_PARAMS_FP = 'yuecheparams.txt'
if path.exists(CUSTOMIZED_PARAMS_FP):
  f = open(CUSTOMIZED_PARAMS_FP)
  content = f.read()
  f.close()
  exec(content)
