# coding=utf-8
'''
作用：
统计一段代码执行的时间，在代码执行前后输出log信息
'''

import time


class stopwatch(object):
    def __init__(self, desc, logging=None, print_screen=True):
        self.logging = logging
        self.desc = desc
        self.print_screen = print_screen
        self.start = time.time()
        msg = '{0} start...'.format(self.desc)
        self.print_msg(msg)

    def __del__(self):
        delta = int((time.time() - self.start) * 1000)
        msg = '{0} end: {1} ms'.format(self.desc, delta)
        self.print_msg(msg)

    def print_msg(self, desc):
        if self.print_screen:
            print (desc)
        if self.logging:
            self.logging.info(desc)
