#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import time

class log:
    def __init__(self):
        #设置文件目录
        pj_path = os.path.split(os.path.realpath(__file__))[0]
        if not os.path.exists(pj_path):
            os.mkdir(pj_path)

        date = time.strftime("%Y-%m", time.localtime())
        filepath = "%s/log/%s.log" % (pj_path, date)

        # 创建一个logger
        self.logger = logging.getLogger('jjz_logger')
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(filepath)
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

    def debug(self, msg):
        self.logger.debug(msg)
