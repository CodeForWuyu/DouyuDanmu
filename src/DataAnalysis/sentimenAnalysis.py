'''
弹幕情感分析
'''
import pymysql
import targetConfig
from dbHelper import DouyuDanmuDao
from SentimentPolarityAnalysis.spa import classifiers


#从数据库获取弹幕数据
def getDanmu():

    SQL = f"select stime,txt from barrages" \
          f" where Date(stime)=\'{targetConfig.targetDate.strftime('%Y-%m-%d')}\'"
    danmuDao = DouyuDanmuDao()
    danmuDao.connect()

    data = danmuDao.excuteQuery(SQL)
    if not data:
        return -1

    danmuDao.disConnect()
    return data

#对弹幕数据进行逐条情感分析，获得情感得分List
def getScores(data):
    danmuScore = {}
    classifier = classifiers.DictClassifier()
    for t in data:
        danmu = t[1]
        score = classifier.analyse_sentence(danmu, runout_filepath=None, print_show=False)
        danmuScore[danmu] = score

    for k in danmuScore:
        print("弹幕‘%s’的情感得分是%f"%(k,danmuScore[k]))


def main():
    data = getDanmu()
    print(data[0])
    print(data[0][1])
    getScores(data)


if __name__ == '__main__':
    main()

