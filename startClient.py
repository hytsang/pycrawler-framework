#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
追书旗上连载书的更新
@author: zyq
'''

import time

from app.shuqiUpdater import updateFromMysql
from util.timeHelper import getToday


if __name__ == '__main__':
    lastTime = 0
    while 1:
        nowTime = time.time()
        sinceLastTime = nowTime - lastTime
        if sinceLastTime < 24 * 3600:
            print getToday() + ' sleep ' + str(24* 3600 - sinceLastTime) + 's until 24h after last time.'
            time.sleep(24* 3600 - sinceLastTime)
        lastTime = time.time()
        updateFromMysql()