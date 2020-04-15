'''
自动登录斗鱼
'''

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import base64
from time import sleep
import time
import random

#定义浏览器
driver = webdriver.Chrome()
driver.get("https://www.douyu.com/")


sleep(2)

#关闭提示
driver.find_element_by_xpath("/html/body/div[3]/span[1]").click()

#点击登录
login_button = driver.find_element_by_xpath("//*[@id=\"js-header\"]/div/div/div[3]/div[7]/div/div/a/span")
login_button.click()
sleep(2)

#切换到登录iframe
driver.switch_to.frame("login-passport-frame")

#点击密码登录
driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div[2]/div[3]/div/span[2]")\
    .click()

#输入手机号
driver.find_element_by_name("phoneNum").send_keys("13880340424")

#输入密码
driver.find_element_by_name("password").send_keys("douyu2020")

#点击登录
driver.find_element_by_xpath("//*[@id=\"loginbox\"]/div[3]/div[2]/div[2]/form/div[6]/input")\
    .click()

#处理滑动验证码

#获取验证码图像
#下面的js代码根据canvas文档说明而来
def click(block):  # 自定义点击函数,模拟人工点击
    action = ActionChains(driver)
    action.click_and_hold(block).perform()
    time.sleep(random.randint(1,10)/10)
    action.release(block).perform()
btn = driver.find_element_by_class_name('geetest_slider_button')  #到点击按钮
click(btn) # 验证第一步,点击按钮进行验证


