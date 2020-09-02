import win_unicode_console
win_unicode_console.enable()
import sys
import math
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QLabel, QProgressBar, QApplication, QFileDialog)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytube import YouTube
import ssl
import time

class Download(QWidget):
  def __init__(self):
    super(Download, self).__init__()
    self.switch = True
    self.initUI()

  def initUI(self):
    # YouTube链接地址输入框和提示
    self.channelLabel = QLabel(self)
    self.channelLabel.move(30, 30)
    self.channelLabel.resize(100,30)
    self.channelLabel.setText("YouTube链接：")
    self.channel_le = QLineEdit('https://www.youtube.com/', self)
    self.channel_le.move(120,30)
    self.channel_le.resize(250,30)

    # 视频下载数量输入框和提示
    self.qtyLabel = QLabel(self)
    self.qtyLabel.move(30, 75)
    self.qtyLabel.resize(100,30)
    self.qtyLabel.setText("视频下载数量：")
    self.qty_le = QLineEdit('10', self)
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

    # 视频下载后的保存
    self.source_btn = QPushButton('存储路径：', self)
    self.source_btn.move(20, 165)
    self.source_btn.resize(100,30)
    self.source_btn.clicked.connect(self.select_source)
    self.source_le = QLineEdit(self)
    self.source_le.move(120, 165)
    self.source_le.resize(250,30)

    #上传按钮
    self.save_btn = QPushButton('开始下载',self)
    self.save_btn.move(200, 230)
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

  def select_source(self):
    dir_path = QFileDialog.getExistingDirectory(self, "请选择文件夹路径", "C:/")
    self.source_le.setText(str(dir_path))

  def set_label_func(self, text):
    self.result_le.setText(text)

  def switch_func(self, bools):
    self.switch = bools

  def kick(self):
    channel = self.channel_le.text().strip()#YouTube频道
    qty = self.qty_le.text().strip()#视频下载数量
    start_from = self.start_le.text().strip()#视频下载开始序号
    savePath = self.source_le.text().strip()#视频存储路径
    if self.switch and channel != '' and qty != '' and start_from != '' and savePath != '':
      self.switch = False
      self.set_label_func('请耐心等待，正在打开浏览器！')
      self.my_thread = MyThread(channel, qty, start_from, savePath, self.set_label_func)#实例化线程对象
      self.my_thread.start()#启动线程
      self.my_thread.my_signal.connect(self.switch_func)

class MyThread(QThread):#线程类
  ssl._create_default_https_context = ssl._create_unverified_context
  my_signal = pyqtSignal(bool)  #自定义信号对象。参数bool就代表这个信号可以传一个布尔值
  def __init__(self, channel, qty, start_from, savePath, set_label_func, ):
    super(MyThread, self).__init__()
    self.channel = channel
    self.qty = qty
    self.start_from = start_from
    self.savePath = savePath
    self.set_label_func = set_label_func

  def run(self): #线程执行函数
    string = self.fetchData(self.channel, self.qty, self.start_from, self.savePath, self.set_label_func)
    self.set_label_func(string)
    self.my_signal.emit(True)  #释放自定义的信号

  def fetchData(self, channel, qty, start_from, savePath, set_label_func):
    print(channel, qty, start_from, savePath)
    # option = webdriver.ChromeOptions()
    # option.add_argument(r'user-data-dir=C:\Users\zhuan\AppData\Local\Google\Chrome\User Data')
    # option.add_argument('--ignore-certificate-errors')
    # browser = webdriver.Chrome(options=option)
    # browser = webdriver.Chrome()
    browser = webdriver.Chrome(executable_path='/Users/tangyong/Application/chromedriver')
    browser.get(channel)

    time_elements = browser.find_elements_by_xpath('//*[@id="thumbnail"]/*[@id="overlays"]/ytd-thumbnail-overlay-time-status-renderer/span')
    thumbnail = browser.find_elements_by_xpath(r'//*[@id="thumbnail"]/*[@id="overlays"]/ytd-thumbnail-overlay-time-status-renderer/span/../../..')
    total_num_element = len(thumbnail)
    url_list = []
    for index in range(total_num_element):
      time_str = time_elements[index].get_attribute('textContent').strip()
      target = thumbnail[index]
      target_url = target.get_attribute("href")
      print(index, time_str, target_url)
      if self.isVideoLong(time_str, 15) and target_url != None:
        url_list.append(target_url)

    browser.quit()
    total_num_video = len(url_list)
    num = int(start_from)
    download_num = self.numCompare(total_num_video, int(qty) + num)
    vedio_qty_str= '视频总数量：' + str(total_num_video) + '; 需要下载的序号：' + str(num) + '-' + str(download_num)
    print(vedio_qty_str)
    self.set_label_func(vedio_qty_str)
    print('链接地址如下:', url_list)
    Downloadtube(url_list, num, download_num, savePath, self.set_label_func)

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

class Downloadtube():
  def __init__(self, urlList, num, download_num, savePath, set_label_func):
    self.index = num
    self.proxy_handler = {
      "http": "http://127.0.0.1:7890",
      'https': 'https://127.0.0.1:7890'
    }
    self.urlList = urlList
    self.download_num = download_num
    self.path = savePath
    self.set_label_func = set_label_func
    self.progress_int = 0
    self.initDownload()

  def initDownload(self):
    ssl._create_default_https_context = ssl._create_unverified_context
    while (self.index) < self.download_num:
      self.downloadVideo()

  def show_progress_bar(self, stream, chunk, bytes_remaining):
    new_progress_int = int((stream.filesize - bytes_remaining) * 100 / stream.filesize)
    if new_progress_int != self.progress_int:
      self.progress_int = new_progress_int
      print(self.progress_int)
    if bytes_remaining == 0:
      self.index = self.index + 1
      self.progress_int = 0

  def downloadVideo(self):
    try:
      yt = YouTube(self.urlList[self.index], proxies=self.proxy_handler, on_progress_callback=self.show_progress_bar)
      yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').last().download(self.path)
      current_download_str = '当前视频下载进度:' + str(self.index) + '/' + str(self.download_num)
      print(current_download_str)
      self.set_label_func(current_download_str)
    except BaseException:
      print(self.index, BaseException)
      time.sleep(5)
      self.downloadVideo()

if __name__=="__main__":
  app = QApplication(sys.argv)
  ex = Download()
  ex.show()
  sys.exit(app.exec_())
