'''
统计完整弹幕出现的频率
'''

import time
import datetime
from dbHelper import DouyuDanmuDao
import targetConfig


#从数据库获取弹幕内容
def getBarragesFromDatabase(date):
    date = date.timetuple()  # 转换时间格式

    SQL = f"select txt from barrages" \
          f" where Date(stime)=\'{targetConfig.targetDate.strftime('%Y-%m-%d')}\'"


    danmuDao = DouyuDanmuDao()
    danmuDao.connect()

    data = danmuDao.excuteQuery(SQL)
    if not data:
        return -1

    danmuDao.disConnect()
    return data


#统计弹幕中的词频
def getWordStatsWithJieba(data):
    """

    :param data: tuple类型的数据，data【n】【0】是弹幕数据
    :return:
    """
    barrageFrequency = {}

    for i in range(len(data)):
        barrage = data[i][0]

        if barrage in barrageFrequency.keys():
            barrageFrequency[barrage]+=1
        else:
            barrageFrequency[barrage] = 1
    return barrageFrequency

#写入到csv中
def writeInCSV():
    pass


#绘制词云图
from pyecharts.charts import WordCloud
from pyecharts import options as opts
from pyecharts.globals import SymbolType

def wordCloud(barrageStats):
    # WordCloud模块，链式调用配置，最终生成html文件
    c = (
        WordCloud()
            .add("", barrageStats, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
            .set_global_opts(title_opts=opts.TitleOpts(title="重复弹幕统计"))
            .render(f"./chart/{targetConfig.targetDate.strftime('%Y-%m-%d')}重复弹幕统计.html")
    )


#主函数
def main():

    date = targetConfig.targetDate
    data = getBarragesFromDatabase(date)
    print(type(data))
    print(data)

    #获取弹幕频率
    barrageStats = getWordStatsWithJieba(data)
    del data

    barrageStats = sorted(barrageStats.items(),key=lambda item:item[1],reverse=True)
    for barrage in barrageStats[:50]:
        print(barrage)
    print(type(barrageStats))
    wordCloud(barrageStats)

if __name__ == '__main__':
    main()
