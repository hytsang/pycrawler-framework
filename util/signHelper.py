#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
前面
@author: zyq
'''
import json
import urllib
from urllib import quote

import requests
import time

from Config import MianFeiTXTChapBaseUrl, MianFeiTXTBookBaseUrl
from exception.InputException import InputException
from util.UUIDUtils import getMD5, getUUID
from util.timeHelper import getFormatedTimeSec


def tup2UrlStr(pMap):
    res = []
    for entry in pMap:
        res.append(entry[0] + '=' + str(entry[1]))
    return '&'.join(res)
    # mapstr = unicode(pMap).encode('utf-8')
    # return mapstr.replace("', '",'=').replace('"','').replace('[', '').replace(']', '')\
    #     .replace(', ', '&').replace("'", '').replace('(', '').replace(')', '')

def map2UrlStr(pMap):
    res = []
    for entry in pMap.keys():
        res.append(entry + '=' + pMap[entry])
    return '&'.join(res)
    # return json.dumps(pMap).replace(',','&').replace('"','').replace('{', '').replace('}', '')\
    mapstr = unicode(pMap).encode('utf-8')
    return mapstr.replace(',', '&').replace('"', '').replace('{', '').replace('}', '')\
        .replace(':', '=').replace(' ', '').replace("'", '')


def getMianTxtSign(paramMap):

    if not isinstance(paramMap,dict):
        raise InputException("input must be dict")

    sortedMap = paramMap.items()
    sortedMap.sort()

    paramStr = tup2UrlStr(sortedMap)
    # paramStr = 'algorithm=MD5&apiKey=001&appId=26&bundle=com.mftxtxs.novel&channelId=2&keyword='\
    #            + '大主宰' + '&nouce=e694501a6cd844a797c98dedfc3c04f1&osType=2&pageNum=1&pageSize=10&sid=SID&timestamp=1498921779533&type=1&userId=201706202002092307744175&userType=0&v=1&version=3.4.0'
    # paramStr = urllib.urlencode(sortedMap)

    return getMD5(paramStr  + "&" + "9dbfbfd095fe6648cbc14a8d19952791")

class paramMap(dict):
    # def __init__(self):
    #     self.paramMap = dict()

    def mianfeiTXT(self):
        self['appId'] = '26'
        self['channelId'] = '2'
        self['version'] = '3.4.0'
        self['osType'] = '2'
        self['userId'] = getFormatedTimeSec() + str(int(time.time()))
        # self['userId'] = '201706202002092307744175'
        self['userType'] = '0'
        self['bundle'] = 'com.mftxtxs.novel'
        self['v'] = '1'
        self['sid'] = 'SID'
        self['nouce'] = getUUID()
        # self['nouce'] = 'e694501a6cd844a797c98dedfc3c04f1'
        self['apiKey'] = '001'
        self['timestamp'] = str(int(time.time() * pow(10,3)))
        # self['timestamp'] = '1498921779533'
        self['algorithm'] = 'MD5'
        return self

    # def build(self):
    #
    #     return getMianTxtSign(self)

    def mianfeiTXTSign(self):
        '''
        返回生产sign后的paraMap
        :return: 
        '''
        self['sign'] = getMianTxtSign(self)
        return self

    def mBookId(self, mid):
        self['bookId'] = str(mid)
        return self


    def mChapId(self, cid):
        self['chapterId'] = str(cid)
        return self

    def toUrl(self):
        return urllib.urlencode(self)

    def put(self, k, v):
        self[k] = v
        return self

    # def

if __name__ == '__main__':
    # url = MianFeiTXTChapBaseUrl + '?' + paramMap().mianfeiTXT().mBookId(68158).mChapId('1').mianfeiTXTSign().toUrl()
    url = MianFeiTXTBookBaseUrl + '?' + paramMap().mianfeiTXT().put('bookId','358868286').mianfeiTXTSign().toUrl()
    r = requests.get(url)
    print r.text