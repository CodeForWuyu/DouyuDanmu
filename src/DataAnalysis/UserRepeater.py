'''
找到用户中的复读机
1、首先找到所有的用户
2、根据用户名找到其发送的所有弹幕
3、为其发送的构建字典，key：弹幕  value:频次
'''

from dbHelper import DouyuDanmuDao
import time
import datetime
import targetConfig

#执行SQL语句，返回数据
def executeSQL(SQL):
    # 获取数据库连接
    danmuDao = DouyuDanmuDao()
    danmuDao.connect()

    #执行SQL
    data = danmuDao.excuteQuery(SQL)
    danmuDao.disConnect()

    # 返回数据
    if not data:
        return -1
    return data


#找到所有用户信息
def getAllUserBarrage(date):
    # 转换时间格式
    date = date.timetuple()

    #构建SQL语句并执行
    SQL = f"select nn,txt from barrages " \
          f"where Date(stime)=\'{targetConfig.targetDate.strftime('%Y-%m-%d')}\'"
    allData = executeSQL(SQL)
    return allData


#统计单个用户弹幕的频次
def getUserBarrageFrequency(userBarrageData):
    '''
    :param userBarrageData: 用户-弹幕的元祖数据
    :return:
    '''
    userBarrageDict = {}
    for data in userBarrageData:
        user,barrage= data
        #若字典里还没有用户，将用户加入到词典中，并将该条弹幕统计到用户对应的字典中
        if user not in userBarrageDict.keys():
            barrageDict = {}
            barrageDict[barrage] = 1
            userBarrageDict[user] = barrageDict
        else:
        #用户已经在字典中，检查该条弹幕是否存在于用户的字典中
            if barrage not in userBarrageDict[user]:
                userBarrageDict[user][barrage] = 1
            else:
                userBarrageDict[user][barrage] +=1

    #对用户弹幕字典进行排序,排序后变成一个list
    for user in userBarrageDict.keys():
        userBarrageDict[user] = sorted(userBarrageDict[user].items(),
                                       key=lambda item:item[1],
                                       reverse=True)
    print(userBarrageDict)

    #对所有用户进行排序 此时的usrbarrageDict为 用户-（弹幕频次列表）
    #排序完为元组数据
    userBarrageDict = sorted(userBarrageDict.items(),
                             # 使用弹幕频次列表的第一个元组的第二个元素，
                             # 即某个用户的重复最高的弹幕数量
                             key=lambda item:item[1][0][1],
                             reverse=True)
    print(userBarrageDict)
    return userBarrageDict





def main():
    date = targetConfig.targetDate
    userBarrage = getAllUserBarrage(date)

    print(userBarrage)

    userBarragetuple = getUserBarrageFrequency(userBarrage)

    for item in userBarragetuple[:20]:
        user,barrageList = item
        print(f"用户\"{user}\"发送最多的弹幕为:  \"{barrageList[0][0]}\"  ,发送次数为{barrageList[0][1]}")
        if(len(barrageList)>1):
            print(f"用户\"{user}\"发送第二多的弹幕为:  \"{barrageList[1][0]}\"  ,发送次数为{barrageList[1][1]}")

        print()



if __name__ == '__main__':
    main()
