'''
斗鱼弹幕爬虫主程序
'''
from DyDanmuMsgHandler import DyDanmuMsgHandler
from DyDanmuWebSocketClient import DyDanmuWebSocketClient
from DyDanmuDBHandler import DyBarrageDBHandler
import threading
import time

class DyDanmuCrawler:
    def __init__(self,roomid):
        self.__room_id = roomid
        self.__heartbeat_thread = None
        self.__client = DyDanmuWebSocketClient(on_open=self.__prepare,
                                               on_message=self.__receive_msg,
                                               on_close=self.__stop)
        self.__msg_handler =  DyDanmuMsgHandler()
        self.__db_handler = DyBarrageDBHandler()
        self.__keep_HeartBeat = True

    def start(self):
        '''
        开启客户端
        :return:
        '''
        self.__db_handler.connect()
        self.__db_handler.prepare()
        self.__client.start()

    def __stop(self):
        '''
        登出
        停止客户端
        停止心跳线程
        :return:
        '''
        self.__logout()
        self.__client.stop()
        self.__db_handler.disconnect()
        self.__keep_HeartBeat=False

    def __prepare(self):
        '''
        准备工作：登陆；加入群组；开启心跳线程
        :return:
        '''
        self.__login()
        self.__join_group()
        self.__start_heartbeat()

    def __receive_msg(self, msg):
        '''
        处理收到的信息
        :param msg:
        :return:
        '''
        chat_messages = self.__msg_handler.get_chat_messages(msg)
        for message in chat_messages:
            print(f"{message['nn']}:{message['txt']}")
            # self.__db_handler.insert_barrage(message)

    def __login(self):
        '''
        登陆
        :return:
        '''
        # login_msg = 'type@=loginreq/room_id@=%s/dfl@=sn@A=105@Sss@A=1/username@=%s/uid@=%s/ver@=20190610/aver@=218101901/ct@=0/' % (
        # self.__room_id, '61609154', '61609154')
        login_msg = 'type@=loginreq/roomid@=%s/dfl@=sn@AA=105@ASss@AA=1/' \
                    'username@=%s/uid@=%s/ver@=20190610/aver@=218101901/ct@=0/.'%(
            self.__room_id,'99047358','99047358'
        )
        self.__client.send(self.__msg_handler.dy_encode(login_msg))

    def __join_group(self):
        '''
        发送群组消息
        :return:
        '''
        join_group_msg = 'type@=joingroup/rid@=%s/gid@=1/' % (self.__room_id)
        self.__client.send(self.__msg_handler.dy_encode(join_group_msg))

    def __start_heartbeat(self):
        self.__heartbeat_thread = threading.Thread(target=self.__heartbeat)
        self.__heartbeat_thread.start()

    def __heartbeat(self):
        heartbeat_msg = 'type@=mrkl/'
        heartbeat_msg_byte = self.__msg_handler.dy_encode(heartbeat_msg)

        while True:
            self.__client.send(heartbeat_msg_byte)
            for i in range(90):
                time.sleep(0.5)
                if  not self.__keep_HeartBeat:
                    return

    def __logout(self):
        logout_msg = 'type@=logout/'
        logout_msg_byte = self.__msg_handler.dy_encode(logout_msg)




