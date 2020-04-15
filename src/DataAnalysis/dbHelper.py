'''
操作数据库类
'''

import pymysql
import config

class DouyuDanmuDao():
    def __init__(self):
        self.__conn = None
        self.__cursor = None
        self.__db_name = 'dybarrage'
        self.__table_name = 'barrages'

    #数据库连接
    def connect(self):
        self.__conn = pymysql.connect(host = config.host,
                                      user = config.user,
                                      password = config.password,
                                      database = "dybarrage"
                                      )
        self.__cursor = self.__conn.cursor()

    #关闭数据库连接
    def disConnect(self):
        self.__cursor.close()
        self.__conn.close()

    #执行SQL查询语句
    def excuteQuery(self,SQL):
        print(SQL)
        try:
            self.__cursor.execute(SQL)
            return self.__cursor.fetchall()
        except Exception as ex:
            print(ex)
            print("查询失败！")
            return -1