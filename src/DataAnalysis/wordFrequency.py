'''
统计弹幕中词语出现的频率
'''

import jieba
import fool
import time
import datetime
from dbHelper import DouyuDanmuDao
import targetConfig

#从数据库获取弹幕内容
def getBarragesFromDatabase(date):
    date = date.timetuple()  # 转换时间格式

    SQL = f"select txt from barrages " \
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
    wordFrequency = {}

    for i in range(len(data)):
        barrage = data[i][0]
        for word in jieba.cut_for_search(barrage):
            if word in wordFrequency.keys():
                wordFrequency[word]+=1
            else:
                wordFrequency[word] = 1
    return wordFrequency

def getWordStatsWithFool(data):
    """

    :param data: tuple类型的数据，data【n】【0】是弹幕数据
    :return:
    """
    wordFrequency = {}

    for i in range(len(data)):
        barrage = data[i][0]
        # print(fool.cut(barrage))
        for word in fool.cut(barrage)[0]:
            # print(word)
            if word in wordFrequency.keys():
                wordFrequency[word]+=1
            else:
                wordFrequency[word] = 1
    return wordFrequency


#绘制词云图
from pyecharts.charts import WordCloud
from pyecharts import options as opts
from pyecharts.globals import SymbolType

def wordCloud(barrageStats):
    # WordCloud模块，链式调用配置，最终生成html文件
    c = (
        WordCloud()
            .add("", barrageStats, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
            .set_global_opts(title_opts=opts.TitleOpts(title="词语频率"))
            .render("词语频率.html")
    )


#主函数
def main():
    date = targetConfig.targetDate
    data = getBarragesFromDatabase(date)
    print(type(data))
    print(data)

    #获取词频
    wordStats = getWordStatsWithJieba(data)
    del data

    wordStats = sorted(wordStats.items(),key=lambda item:item[1],reverse=True)
    print(wordStats)
    for word in wordStats[:50]:
        print(word)
    wordCloud(wordStats)

if __name__ == '__main__':
    main()