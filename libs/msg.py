#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import ConfigParser
import requests
from werkzeug.contrib.cache import FileSystemCache

# 消息二维码 https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=gQG_8TwAAAAAAAAAAS5odHRwOi8vd2VpeGluLnFxLmNvbS9xLzAySS1Zdk5aQ2ZlNjAxMDAwME0wNzUAAgQG4u9ZAwQAAAAA
class Message:
    def __init__(self):
        #获取当前目录
        cur_path = os.path.split(os.path.realpath(__file__))[0]
        #获取父级目录
        parent_path = os.path.dirname(cur_path)
        #配置文件路径
        ini_file= "%s/conf.ini" % parent_path
        #缓存文件路径
        cache_path = "%s/cache/" % parent_path

        cf = ConfigParser.ConfigParser()
        cf.read(ini_file)
        self.sendkey = cf.get('pushbear', 'sendkey')
        self.text = cf.get('pushbear', 'sendname')
        self.push_url = 'https://pushbear.ftqq.com/sub'
        #缓存
        self.cache = FileSystemCache(cache_path)
        #push次数key
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



if __name__ == '__main__':
    msg = Message()
    msg.push('测试消息', 3)
