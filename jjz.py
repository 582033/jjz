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
        headers = {
                'Host' : 'enterbj.zhongchebaolian.com',
                'Connection' : 'keep-alive',
                'Pragma' : 'no-cache',
                'Cache-Control' : 'no-cache',
                'Upgrade-Insecure-Requests' : '1',
                'User-Agent' : 'Mozilla/5.0 (Linux; Android 7.0; MI 5 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36',
                'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Referer': 'https://enterbj.zhongchebaolian.com/enterbj/platform/enterbj/toVehicleType',
                'Accept-Encoding' : 'gzip, deflate',
                'Accept-Language' : 'zh-CN,en-US;q=0.8',
                'Cookie' : 'JSESSIONID=5F9CAA1A713B817DCD8C03D730C1405E; UM_distinctid=15ec7ad338672-0758eb2f67658a-12797d23-38400-15ec7ad338716a; CNZZDATA1260761932=1788518962-1499394672-https%253A%252F%252Fenterbj.zhongchebaolian.com%252F%7C1507934398',
                'X-Requested-With' : 'com.zcbl.bjjj_driving',
        }
        r = self._request(self.sign_url, headers)
        status_code = r.status_code
        headers = r.headers
        print r.headers

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

