#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import time

class Log:
    def __init__(self):
        log_file = self._get_log_file()
        # 创建一个logger
        self.logger = logging.getLogger('jjz_logger')
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)


    #获取日志文件路径
    def _get_log_file(self):
        #获取当前目录
        cur_path = os.path.split(os.path.realpath(__file__))[0]

        #获取父级目录
        parent_path = os.path.dirname(cur_path)

        #获取日志目录
        log_path = "%s/log/" % parent_path
        #print log_path

        #如果不存在则创建
        if not os.path.exists(log_path):
            os.mkdir(log_path)

        #按月份区分日志
        date = time.strftime("%Y-%m", time.localtime())
        log_file = "%s/log/%s.log" % (parent_path, date)
        return log_file



    def debug(self, msg):
        self.logger.debug(msg)


if __name__ == '__main__':
    log = Log()
    log.debug('test log')
