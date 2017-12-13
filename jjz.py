#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import requests
import time
import os
from libs import Log, Message

class jjz:
    def __init__(self):
        self.sign_url = 'https://enterbj.zhongchebaolian.com/enterbj/platform/enterbj/curtime_03'
        self.error_url = [
            'https://enterbj.zhongchebaolian.com/errorpage/enterbj.html',
            'http://bjjj.zhongchebaolian.com/images/cdn_image.png',
        ]

    def _request(self, url, headers={}):
        requests.packages.urllib3.disable_warnings()
        #verify             证书
        #allow_redirects    不进行302
        r = requests.get(url, headers=headers, verify=False, allow_redirects=False)
        return r

    def check302(self):
        r = self._request(self.sign_url)
        status_code = r.status_code
        headers = r.headers

        location = ''
        if 'Location' in headers:
            location = headers['Location']

        if  location in self.error_url:
            #print '不能办理'
            return False
        else:
            #print '可以办理'
            return True



if __name__ == '__main__':
    log = Log()
    msg = Message()
    jjz = jjz()

    now = time.strftime('%H点%M分', time.localtime())
    res = jjz.check302()
    if res:
        log.debug('可以办理')
        # 默认每日只提醒3次
        msg.push('%s 可以办理进京证啦~' % str(now))
        #msg.push('可以办理进京证啦~', 4)
    else:
        #log.debug('不能办理')
        #msg.push('%s 测试' % str(now))
        print('不能办理')

