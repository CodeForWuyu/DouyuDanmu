'''
统计每个用户发送弹幕的数量
'''
from dbHelper import DouyuDanmuDao
import time
import datetime
import targetConfig


def getUsersFromDatabase(date):
    '''
    从数据库获取所有的用户名
    :param date:传入要统计的日期
    :return: 返回tuple格式的数据
    '''
    danmuDao = DouyuDanmuDao()
    danmuDao.connect()
    date = date.timetuple()  #转换时间格式

    # SQL = f"select uid, nn from barrages " \
    #       f"where UNIX_TIMESTAMP(stime)-{time.mktime(date)}>0 and " \
    #       f"UNIX_TIMESTAMP(stime)-{time.mktime(date)}<86400000"
    SQL = f"select uid,nn from barrages" \
          f" where Date(stime)=\'{targetConfig.targetDate.strftime('%Y-%m-%d')}\'"
    data = danmuDao.excuteQuery(SQL)
    if not data:
        return -1

    danmuDao.disConnect()
    return data


#对用户名进行统计，获得{用户名：弹幕数量}词典
def getUserCountDict(data):
    userCountDict = {}
    for t in data:
        if t[1] not in userCountDict.keys():
            userCountDict[t[1]] = 1
        else:
            userCountDict[t[1]] += 1

    #对字典按照弹幕数量进行排序
    userCountDict = sorted(userCountDict.items(),key=lambda item:item[1],reverse=True)
    for item in userCountDict:
        print(item)
    return userCountDict

#绘制词云图
from pyecharts.charts import WordCloud
from pyecharts import options as opts
from pyecharts.globals import SymbolType

def wordCloud(userCountDict):
    # WordCloud模块，链式调用配置，最终生成html文件
    c = (
        WordCloud()
            .add("", userCountDict, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
            .set_global_opts(title_opts=opts.TitleOpts(title="用户发送弹幕数"))
            .render(f"./chart/{targetConfig.targetDate.strftime('%Y-%m-%d')}用户发送弹幕数.html")
    )



#主函数
def main():
    date = targetConfig.targetDate
    data = getUsersFromDatabase(date)
    print(type(data))
    print(data)
    print(f"弹幕数量一共{len(data)}条")

    userCountDict = getUserCountDict(data)
    wordCloud(userCountDict)

if __name__ == '__main__':
    main()