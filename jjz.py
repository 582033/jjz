#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import base64
import requests
import time
import json
from werkzeug.contrib.cache import FileSystemCache

# 消息二维码 https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=gQG_8TwAAAAAAAAAAS5odHRwOi8vd2VpeGluLnFxLmNvbS9xLzAySS1Zdk5aQ2ZlNjAxMDAwME0wNzUAAgQG4u9ZAwQAAAAA
class Message:
    def __init__(self):
        self.sendkey = '1194-6d848e48e50333408425d6b8370f612a'
        self.text = 'yjiang'
        self.push_url = 'https://pushbear.ftqq.com/sub'
        #缓存
        self.cache = FileSystemCache('/tmp/jjz_cache')
        #push次数
        self.cache_push_times_key  = 'today_push_times'

    #计算距离当天24点还多少秒
    def _shengyu(self):
        h = int(time.strftime('%H',time.localtime(time.time())))
        m = int(time.strftime('%M',time.localtime(time.time())))
        s = int(time.strftime('%S',time.localtime(time.time())))

        shengyu = int(24*60 - (h*60 + m + 1)) * 60
        return shengyu + (60 - s)

    #发送消息
    def _send(self, desp):
        push_data = {
            'sendkey' : self.sendkey,
            'text' : self.text,
            'desp' : desp
        }
        r = requests.post(self.push_url, data=push_data)
        #print r.text

    #获取当前已经提醒了几次, 如果大于3次了, 今天不再提醒
    def push(self, desp, max_remind_times=3):
        push_times = self.cache.get(self.cache_push_times_key)


        if push_times is None:
            #今天还没有发送过消息时
            push_times = 1
        else:
            #今天已经发送过时
            if push_times < max_remind_times:
                push_times = push_times + 1
            else:
                print "[今日已提醒超过%s次,不再提醒]" % (max_remind_times)
                return False

        self.cache.set(self.cache_push_times_key, push_times, timeout=self._shengyu())
        desp = ("%s [今日已提醒%s次]") % (desp, push_times)
        self._send(desp)





class jjz:
    def __init__(self):
        self.cafile = './charles-ssl-proxying-certificate.pem'
        self.cookie = {
             'JSESSIONID' : '0687B4603F1298EADD52B05945D6BB0C',
             'UM_distinctid' : '15ad9489fb5db-0d08f425adab3b-4f20076b-38400-15ad9489fb71f1',
        }

    def _request(self, url, headers={}):
        requests.packages.urllib3.disable_warnings()
        #verify             证书
        #allow_redirects    不进行302
        r = requests.get(url, headers=headers, verify=False, allow_redirects=False)
        return r

    def check302(self):
        url = 'https://enterbj.zhongchebaolian.com/enterbj/platform/enterbj/curtime_03'
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
        r = self._request(url, headers)
        status_code = r.status_code
        headers = r.headers

        location = ''
        if 'Location' in headers:
            location = headers['Location']

        if  location == 'https://enterbj.zhongchebaolian.com/errorpage/enterbj.html':
            #print '不能办理'
            return False
        else:
            #print '可以办理'
            return True

jjz = jjz()
msg = Message()
res = jjz.check302()

if res:
    print '可以办理'
    # 默认每日只提醒3次
    msg.push('可以办理进京证啦~')
    #msg.push('可以办理进京证啦~', 4)
else:
    print '不能办理'
