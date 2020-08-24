from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def isVideoLong(string, times):
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

browser = webdriver.Chrome(executable_path='/Users/tangyong/Application/chromedriver')

browser.get('https://www.youtube.com/')
browser.find_element_by_xpath('//input').send_keys('频道：NBA')
search = browser.find_element_by_id('search-icon-legacy')
search.click()
main_link = browser.find_element_by_id('main-link')
main_link.click()
time.sleep(5)
video = browser.find_elements_by_class_name('paper-tab')[1]
video.click()
time.sleep(3)
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

time_elements = browser.find_elements_by_xpath('//*[@id="thumbnail"]/*[@id="overlays"]/ytd-thumbnail-overlay-time-status-renderer/span')
thumbnail = video_compile = browser.find_elements_by_xpath(r'//*[@id="thumbnail"]/*[@id="overlays"]/ytd-thumbnail-overlay-time-status-renderer/span/../../..')
total_num_element = len(thumbnail)
url_list = []
for index in range(total_num_element):
  time_str = time_elements[index].get_attribute('textContent').strip()
  target = thumbnail[index]
  target_url = target.get_attribute("href")
  print(index, time_str, target_url)
  if isVideoLong(time_str, 15) and target_url != None:
    url_list.append(target_url)

total_num_video = len(url_list)

print('已经爬到的视频个数:', total_num_video)
print('链接地址如下:', url_list)

num = 1
while num < total_num_video:
  try:
    browser.get('https://en.savefrom.net/18/')
    WebDriverWait(browser, 30).until(
      EC.presence_of_element_located((By.XPATH,"//input"))
    )
    time.sleep(1)
    browser.find_element_by_xpath('//input').send_keys(url_list[num])
    video_compile = browser.find_element_by_xpath('//button[contains(text(),"Download")]')
    video_compile.click()
    WebDriverWait(browser, 300).until(
      EC.presence_of_element_located((By.CLASS_NAME,"def-btn-box"))
    )
    time.sleep(1)
    download = browser.find_element_by_class_name('def-btn-box')
    download.click()
    #   关闭广告页面
    handles = browser.window_handles
    if len(handles) > 1:
      browser.switch_to.window(handles[1])
      browser.close()
      browser.switch_to.window(handles[0])
    browser.get('https://en.savefrom.net/18/')
    print('当前视频下载进度:', num, '/', total_num_video)
    num = num + 1
  except ZeroDivisionError as e:
    print('error:', e)
  finally:
    print('搞定一个！')