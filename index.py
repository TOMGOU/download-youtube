import win_unicode_console
win_unicode_console.enable()
import sys
import math
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QLabel, QApplication, QFileDialog)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Upload(QWidget):
  def __init__(self):
    super(Upload, self).__init__()
    self.switch = True
    self.initUI()

  def initUI(self):
    # YouTube频道输入框和提示
    self.channelLabel = QLabel(self)
    self.channelLabel.move(30, 30)
    self.channelLabel.resize(100,30)
    self.channelLabel.setText("YouTube频道：")
    self.channel_le = QLineEdit('Motion Station', self)
    self.channel_le.move(120,30)
    self.channel_le.resize(250,30)

    # 视频下载数量输入框和提示
    self.qtyLabel = QLabel(self)
    self.qtyLabel.move(30, 75)
    self.qtyLabel.resize(100,30)
    self.qtyLabel.setText("视频下载数量：")
    self.qty_le = QLineEdit('30', self)
    self.qty_le.move(120,75)
    self.qty_le.resize(250,30)

    # 视频下载数量输入框和提示
    self.startLabel = QLabel(self)
    self.startLabel.move(30, 120)
    self.startLabel.resize(100,30)
    self.startLabel.setText("开始下载序号：")
    self.start_le = QLineEdit('0', self)
    self.start_le.move(120,120)
    self.start_le.resize(250,30)

    #上传按钮
    self.save_btn = QPushButton('开始下载',self)
    self.save_btn.move(200, 200)
    self.save_btn.resize(140, 30)
    self.save_btn.clicked.connect(self.kick)

    #用户提示区
    self.result_le = QLabel('请填写YouTube频道和下载数量', self)
    self.result_le.move(30, 270)
    self.result_le.resize(340, 30)
    self.result_le.setStyleSheet('color: blue;')

    # 整体界面设置
    self.resize(400, 400)
    self.center()
    self.setWindowTitle('YouTube视频自动化下载')#设置界面标题名
    self.show()
  
  # 窗口居中函数
  def center(self):
    screen = QtWidgets.QDesktopWidget().screenGeometry()#获取屏幕分辨率
    size = self.geometry()#获取窗口尺寸
    self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))#利用move函数窗口居中

  def set_label_func(self, text):
    self.result_le.setText(text)

  def switch_func(self, bools):
    self.switch = bools

  def kick(self):
    channel = self.channel_le.text().strip()#YouTube频道
    qty = self.qty_le.text().strip()#视频下载数量
    start_from = self.start_le.text().strip()#视频下载数量
    if self.switch and channel != '' and qty != '' and start_from != '':
      self.switch = False
      self.set_label_func('请耐心等待，正在打开浏览器！')
      self.my_thread = MyThread(channel, qty, start_from, self.set_label_func)#实例化线程对象
      self.my_thread.start()#启动线程
      self.my_thread.my_signal.connect(self.switch_func)

class MyThread(QThread):#线程类
  my_signal = pyqtSignal(bool)  #自定义信号对象。参数bool就代表这个信号可以传一个布尔值
  def __init__(self, channel, qty, start_from, set_label_func):
    super(MyThread, self).__init__()
    self.channel = channel
    self.qty = qty
    self.start_from = start_from
    self.set_label_func = set_label_func

  def run(self): #线程执行函数
    string = self.fetchData(self.channel, self.qty, self.start_from, self.set_label_func)
    self.set_label_func(string)
    self.my_signal.emit(True)  #释放自定义的信号

  # 该函数臃肿严重，后续优化【包含时间间隔判断函数优化】
  def fetchData(self, channel, qty, start_from, set_label_func):
    print(channel, qty, start_from)
    # option = webdriver.ChromeOptions()
    # option.add_argument(r'user-data-dir=C:\Users\zhuan\AppData\Local\Google\Chrome\User Data')
    # option.add_argument('--ignore-certificate-errors')
    # browser = webdriver.Chrome(options=option)
    # browser = webdriver.Chrome()
    browser = webdriver.Chrome(executable_path='/Users/tangyong/Application/chromedriver')
    browser.get('https://www.youtube.com/')
    browser.find_element_by_xpath('//input').send_keys('频道：' + channel)
    search = browser.find_element_by_id('search-icon-legacy')
    search.click()
    WebDriverWait(browser, 100).until(
      EC.presence_of_element_located((By.ID, "main-link"))
    )
    isChannelExist = self.isElementExist(browser, '#main-link')
    if not isChannelExist:
      return '频道不存在'
    main_link = browser.find_element_by_id('main-link')
    main_link.click()
    WebDriverWait(browser, 100).until(
      EC.presence_of_element_located((By.CLASS_NAME, "paper-tab"))
    )
    video = browser.find_elements_by_class_name('paper-tab')[1]
    video.click()
    self.sleep(5)
    scroll_num = math.ceil(int(qty) / 30)
    for index in range(scroll_num):
      browser.execute_script("window.scrollTo(0, 100000);")
      self.sleep(10)

    time_elements = browser.find_elements_by_xpath('//*[@id="thumbnail"]/*[@id="overlays"]/ytd-thumbnail-overlay-time-status-renderer/span')
    thumbnail = video_compile = browser.find_elements_by_xpath(r'//*[@id="thumbnail"]/*[@id="overlays"]/ytd-thumbnail-overlay-time-status-renderer/span/../../..')
    total_num_element = len(thumbnail)
    url_list = []
    for index in range(total_num_element):
      time_str = time_elements[index].get_attribute('textContent').strip()
      target = thumbnail[index]
      target_url = target.get_attribute("href")
      print(index, time_str, target_url)
      if self.isVideoLong(time_str, 15) and target_url != None:
        url_list.append(target_url)

    total_num_video = len(url_list)

    print('已经爬到的视频个数:', total_num_video)
    print('链接地址如下:', url_list)

    download_num = self.numCompare(total_num_video, int(qty))
    num = int(start_from)
    while num <= download_num:
      try:
        browser.get('https://en.savefrom.net/18/')
        WebDriverWait(browser, 30).until(
          EC.presence_of_element_located((By.XPATH,"//input"))
        )
        self.sleep(1)
        browser.find_element_by_xpath('//input').send_keys(url_list[num])
        video_compile = browser.find_element_by_xpath('//button[contains(text(),"Download")]')
        video_compile.click()
        WebDriverWait(browser, 30).until(
          EC.presence_of_element_located((By.CLASS_NAME,"def-btn-box"))
        )
        isChannelExist = self.isElementExist(browser, '.def-btn-box')
        if not isChannelExist:
          video_compile.click()
        self.sleep(1)
        download = browser.find_element_by_class_name('def-btn-box')
        download.click()
        #   关闭广告页面
        handles = browser.window_handles
        if len(handles) > 1:
          browser.switch_to.window(handles[1])
          browser.close()
          browser.switch_to.window(handles[0])
        browser.get('https://en.savefrom.net/18/')
        current_download = '当前视频下载进度:' + str(num) + '/' + str(download_num)
        print(current_download)
        self.set_label_func(current_download)
        num = num + 1
      except ZeroDivisionError as e:
        print('error:', e)
      finally:
        print('搞定一个！')

    return '自动下载了' + str(download_num) + '个视频！'

  # 视频长度判断
  def isVideoLong(self, string, times):
    time_list = string.split(':')
    length = len(time_list)
    video_time = 0
    if length == 1:
      return False
    elif length == 2:
      video_time = int(time_list[0]) * 60 + int(time_list[1])
    else:
      video_time = int(time_list[0]) * 60 * 60 + int(time_list[1]) * 60 + int(time_list[2])
    return video_time < times * 60
  
  # 元素是否存在判断函数
  def isElementExist(self, browser, element):
    flag=True
    try:
      browser.find_element_by_css_selector(element)
      return flag
    except:
      flag=False
      return flag

  # 两个数字比较取其小
  def numCompare(self, a, b):
    if a > b:
      return b
    else:
      return a

if __name__=="__main__":
  app = QApplication(sys.argv)
  ex = Upload()
  ex.show()
  sys.exit(app.exec_())
