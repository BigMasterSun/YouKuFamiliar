# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/5/26 11:26
from orm_pool import db_pool
import pymysql

class Mysql(object):
    def __init__(self):
        self.conn = db_pool.POOL.connection()
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def close_db(self):
        self.cursor.close()
        self.conn.close()

    def select(self, sql, args=None):
        self.cursor.execute(sql, args)
        res = self.cursor.fetchall()
        return res

    def execute(self, sql, args):
        try:
            self.cursor.execute(sql, args)
        except BaseException as e:
            print("数据增改出错: ",e)

