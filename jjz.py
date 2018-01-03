#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import requests
import time
import os
import random
from libs import Log, Message, Proxy

class jjz:
    def __init__(self):
        self.sign_url = 'https://enterbj.zhongchebaolian.com/enterbj/platform/enterbj/curtime_03?userid=26B0EBD0E8AB47E58FDDCA0861235A7B'
        self.headers = {
            'Host' : 'enterbj.zhongchebaolian.com',
            'Connection' : 'keep-alive',
            'Content-Length' : '0',
            'Pragma' : 'no-cache',
            'Cache-Control' : 'no-cache',
            'Accept' : 'application/json, text/javascript, */*; q=0.01',
            'Origin' : 'https://enterbj.zhongchebaolian.com',
            'X-Requested-With' : 'XMLHttpRequest',
            'User-Agent' : 'Mozilla/5.0 (Linux; Android 7.0; MI 5 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36',
            'Content-Type' : 'application/json',
            'Referer' : 'https://enterbj.zhongchebaolian.com/enterbj/platform/enterbj/toVehicleType',
            'Accept-Encoding' : 'gzip, deflate',
            'Accept-Language' : 'zh-CN,en-US;q=0.9',
            'Cookie' : 'JSESSIONID=3B1D99AF5EC0B00C8A06D713CC820DA4; UM_distinctid=16056847d8fa1-0bde8ee3b666dc-442d056d-38400-16056847d911f1; CNZZDATA1260761932=746657558-1513275416-%7C1514633209'
        }
        self.error_url = [
            'https://enterbj.zhongchebaolian.com/errorpage/enterbj.html',
            'http://bjjj.zhongchebaolian.com/images/cdn_image.png',
        ]

    def _get_proxy(self):
        proxy_url = "http://www.xicidaili.com/nt/"                                          #代理来源
        target_url = "https://enterbj.zhongchebaolian.com/enterbj/jsp/enterbj/index.html"   #验证代理的url
        ver_keyword = "flushbtn"                                                            #验证关键字
        timeout = 10                                                                        #验证超时时间

        p = Proxy(proxy_url, target_url, ver_keyword, timeout)
        proxies = p.get()
        proxy = random.choice(proxies)
        proxy_obj = { 'http' : proxy }
        print "获取到有效代理: %s " % proxy
        return proxy_obj

    def _request(self, url, headers={}):
        requests.packages.urllib3.disable_warnings()
        #获取代理
        proxy = self._get_proxy()
        #verify             证书
        #allow_redirects    不进行302
        r = requests.post(url, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
        return r

    def check302(self):
        r = self._request(self.sign_url, self.headers)
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

