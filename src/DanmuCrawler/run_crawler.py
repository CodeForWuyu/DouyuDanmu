'''
运行爬虫的程序
'''
from DyDanmuCrawler import DyDanmuCrawler


roomid = "74751"
dy_barrage_crawler = DyDanmuCrawler(roomid)
dy_barrage_crawler.start()