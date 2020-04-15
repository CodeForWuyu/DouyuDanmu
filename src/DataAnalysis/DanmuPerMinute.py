'''
弹幕的数量-时间(分钟)数据
'''
import time
import datetime
from dbHelper import DouyuDanmuDao
import numpy as np
import gc
import targetConfig

#获取给定日期当日的时间序列
def getTimeSerise(date):
    danmuDao = DouyuDanmuDao()
    danmuDao.connect()

    # SQL = f"select stime from barrages " \
    #       f"where UNIX_TIMESTAMP(stime)-{time.mktime(date)}>0 and " \
    #       f"UNIX_TIMESTAMP(stime)-{time.mktime(date)}<86400000"
    SQL = f"select stime from barrages where Date(stime)=\'{targetConfig.targetDate.strftime('%Y-%m-%d')}\'"
    print(SQL)
    data =  danmuDao.excuteQuery(SQL)
    danmuDao.disConnect()
    return data

#对时间序列进行统计分析
def Statistic(timeData):
    #使用字典存储 分钟-弹幕数量
    danmuPerMinute = {}
    for i in range(len(timeData)):
        #将时间转换为分钟
        time = timeData[i][0].replace(second=0)
        #更新字典
        if time not in danmuPerMinute.keys():
            danmuPerMinute[time] = 1
        else:
            danmuPerMinute[time] += 1
    return danmuPerMinute



def getHightsTime(time_num_dic):
    '''
    获取弹幕数量大于平均值75%的分钟-弹幕数据
    :param time_num_dic: 时间-弹幕数量词典
    :return:
    '''

    #获取弹幕数量的均值
    avgBarrageNum = np.mean(list(time_num_dic.values()))
    print(f"平均每分钟弹幕数量为：{avgBarrageNum}")

    print("在这些时刻，弹幕数量特别的多：")
    threshold = avgBarrageNum*1.5  #定义高能时刻的阈值，为均值的1.25倍
    highLightDic = {}
    for key in time_num_dic:
        if time_num_dic[key] >= threshold:
            highLightDic[key] = time_num_dic[key]
            print(key.strftime("%Y-%m-%d %H:%M:%S")+
                  f" 弹幕数量为{highLightDic[key]}")

#写入到csv中
import csv
def writeInCSV(data):
    path = "../file/时间_弹幕数量.csv"
    with open(path,"w",newline='') as f:
        csv_write = csv.writer(f)
        csv_head = ["时间","弹幕数量"]
        csv_write.writerow(csv_head)
        for key in data.keys():
            time = key.strftime("%Y-%m-%d %H:%M:%S")
            number = data[key]
            csv_write.writerow([time,number])
    f.close()


#绘制折线图
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.globals import ThemeType
def getChart(stats):
    x_time = []
    y_count = []
    for key in stats.keys():
        timeStr = key.strftime('%H:%M:%S')
        x_time.append(timeStr)
        y_count.append(stats[key])

    line = (Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(x_time)
            .add_yaxis("弹幕数量",y_count)
            .set_global_opts(
        title_opts=opts.TitleOpts(title=f"{targetConfig.targetDate.strftime('%Y-%m-%d')}",subtitle="弹幕变化图"),
        tooltip_opts=opts.TooltipOpts(trigger='axis',axis_pointer_type='cross'),
        toolbox_opts=opts.ToolboxOpts(is_show=True,orient='vertical',pos_left='right'),))

    line.render(f"./chart/{targetConfig.targetDate.strftime('%Y-%m-%d')}弹幕数量变化.html")


def main():
    date = targetConfig.targetDate
    data = getTimeSerise(date.timetuple())
    if(data==-1):
        print("失败")
    else:
        print(f"一共有弹幕{len(data)}条")
        #获取时间-数量的字典
        stats = Statistic(data)
        del data
        print("一共有%d分钟"%len(stats))
        print(stats)
        getHightsTime(stats)

        #绘制折线图
        getChart(stats)


if __name__ == '__main__':
    main()