#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''

@author: zyq
'''
import json
import traceback

import requests

from app.baseCrawler import BaseCrawler
from app.mianFeiFixer import fixUnFinished
from app.shuqi import getBookObjFromSQid, getCapObjsByBookObj, crawlCapsWithBookObj
from dao.connFactory import getDushuConnCsor
from dao.dushuService import updateOneFieldByOneField, updateBoostWithUpdateTime, getBookObjById, delBookById
from dao.dushuShuqiService import getShuqiAllLianZaiBookObjs
from exception.InputException import InputException
from util.logHelper import myLogging


def updateFromMysql():
    '''
        永远运行，从数据库中查询出于连载状态的小说，进行更新
    '''

    # crawlInput = dict()
    # crawlInput['crawlerName'] = 'shuqiById'
    # data = dict()
    # crawlInput['data']  = data
    #
    # conn,csor = getDushuConnCsor()
    #
    # csor.execute("SELECT source from cn_dushu_book where operateStatus = 0  AND bookType = '连载' and rawUrl like 'http://api.shuqireader.com/reader/bc_cover.php%';")
    # conn.commit()
    #
    # ss = csor.fetchall()
    # for source in ss:
    #     sid = source[0].replace('shuqi', '')
    #     if '' == sid:
    #         continue
    #     data['sid'] = sid
    #
    #
    #     try:
    #         r = requests.post('http://0.0.0.0:10008/simpleCrawler', data = json.dumps(crawlInput))
    #     # print 'dine id: ',sid, 'with response: ',
    #     except Exception as e:
    #         print 'sid: ',sid, ' done with exception: ', e.message
    bookObjs = getShuqiAllLianZaiBookObjs()
    for bookObj in bookObjs:
        try:
            updateByBookObj(bookObj)
        except Exception as e:
            myLogging.error('update book' + str(bookObj['id']) +' raise exception ')
            myLogging.error(traceback.format_exc())

def updateByDbBookId(dbid):

    bookObj = getBookObjById(dbid)
    if not bookObj:
        raise InputException('wrong id')
    updateByBookObj(bookObj)

def updateByBookObj(bookObj):
    source = int(bookObj['source'].replace('shuqi', ''))
    newBookObj, digest = getBookObjFromSQid(source)
    if not newBookObj:
        # delBookById(bookObj['id'])
        myLogging.error( 'shuqi book has been droped, plz consider to delete id: '+ str(bookObj['id'])+ ' sid: '+ str(source))
        return
    if newBookObj['chapterNum'] > bookObj['chapterNum']:
        newBookObj['id'] = bookObj['id']
        newChapNum = crawlCapsWithBookObj(bookObj=newBookObj, bookId=source, allowUpdate=True)

        if newChapNum >= bookObj['chapterNum']:
            updateOneFieldByOneField('chapterNum', newChapNum, 'id', bookObj['id'])
            updateBoostWithUpdateTime(bookObj['id'])
            myLogging.info( newBookObj['title'].encode('utf-8') + ' update ' + str(newChapNum - bookObj['chapterNum'])\
                  + ' chaps ')

            if u'连载' != newBookObj['bookType']:
                updateOneFieldByOneField('bookType', newBookObj['bookType'], 'id', bookObj['id'])
                myLogging.warning(newBookObj['title'].encode('utf-8') + newBookObj['bookType'].encode('utf-8'))
        else:
            myLogging.info(newBookObj['title'].encode('utf-8') + ' has unexcepted, please check. didnot update ')
    else:
        myLogging.info(newBookObj['title'].encode('utf-8') + ' no update ()')

class ShuqiUpdater(BaseCrawler):

    def __init__(self):
        self.bookId = None

    def init(self, data = None):
        if data and isinstance(data, dict) and data.has_key('bookId'):
            self.bookId = data['bookId']

    def crawl(self):
        if self.bookId:
            updateByDbBookId(self.bookId)
        else:
            updateFromMysql()
    def output(self):
        pass



if __name__ == '__main__':
    # fixUnFinished()
    updateFromMysql()
