from pytube import YouTube, compat, Playlist
import ssl
import time

class Download():
  def __init__(self):
    self.index = 0
    self.proxy_handler = {
      "http": "http://127.0.0.1:7890",
      'https': 'https://127.0.0.1:7890'
    }
    self.urlList = ['https://www.youtube.com/watch?v=eAGXCie-zDY', 'https://www.youtube.com/watch?v=DFjq1H8LZHI', 'https://www.youtube.com/watch?v=QeJOMk4N4Xc', 'https://www.youtube.com/watch?v=Z2B4-HpXE7s', 'https://www.youtube.com/watch?v=bBrhh4VXb7I', 'https://www.youtube.com/watch?v=l9suNGdVwyU', 'https://www.youtube.com/watch?v=CcDjPdgNqeY', 'https://www.youtube.com/watch?v=MbXbs8yLmSo', 'https://www.youtube.com/watch?v=WZhp_Cci1i8', 'https://www.youtube.com/watch?v=9jYM0AGB2Bg', 'https://www.youtube.com/watch?v=ffUr9LMHMRo', 'https://www.youtube.com/watch?v=r6iImq-wTR4', 'https://www.youtube.com/watch?v=4mP3jBIZrWc', 'https://www.youtube.com/watch?v=1DkCIFHFQ6Q', 'https://www.youtube.com/watch?v=u9vSgFvFK7o', 'https://www.youtube.com/watch?v=8w8BwDhwONU', 'https://www.youtube.com/watch?v=SmaVVgfFpzQ', 'https://www.youtube.com/watch?v=u3y_Q_oukFo', 'https://www.youtube.com/watch?v=M8SUuPXNClE', 'https://www.youtube.com/watch?v=5PNk-MZrXKg', 'https://www.youtube.com/watch?v=X53yt4jdRHQ', 'https://www.youtube.com/watch?v=6Q5Hj-1U_yg', 'https://www.youtube.com/watch?v=eyB1nrLRAds', 'https://www.youtube.com/watch?v=fchAPS29dYE', 'https://www.youtube.com/watch?v=3FI3IiA2P7Q', 'https://www.youtube.com/watch?v=ko5jVyJhjPQ', 'https://www.youtube.com/watch?v=wX4LLondvNE', 'https://www.youtube.com/watch?v=qI6CAdiwOIM', 'https://www.youtube.com/watch?v=rsKBsV4V_eM', 'https://www.youtube.com/watch?v=12NgRIuNQqQ', 'https://www.youtube.com/watch?v=VhpdrTvR2iA', 'https://www.youtube.com/watch?v=qmk_0M85Z-I', 'https://www.youtube.com/watch?v=RFe3vDZh7IQ', 'https://www.youtube.com/watch?v=c8QcK7jgbu0', 'https://www.youtube.com/watch?v=f_OcIL_uP78', 'https://www.youtube.com/watch?v=MoGXTFU885A', 'https://www.youtube.com/watch?v=HXeHs3Przrk', 'https://www.youtube.com/watch?v=TfNuI3MGVkE', 'https://www.youtube.com/watch?v=KI9LaCp3ncU', 'https://www.youtube.com/watch?v=VfiJk-wCCOQ', 'https://www.youtube.com/watch?v=k4K8njjKBoU', 'https://www.youtube.com/watch?v=COpkubUZ8o4', 'https://www.youtube.com/watch?v=gpKNir8qOyE', 'https://www.youtube.com/watch?v=gulNInoEYWI', 'https://www.youtube.com/watch?v=JIb3UTiRGxA', 'https://www.youtube.com/watch?v=NdHJLtNKvhc', 'https://www.youtube.com/watch?v=ZLdAx3Jt9mQ', 'https://www.youtube.com/watch?v=GQHtrBfjegs', 'https://www.youtube.com/watch?v=7stzdHPDxSM', 'https://www.youtube.com/watch?v=TYCOu2Rx43o', 'https://www.youtube.com/watch?v=F3aSgpRYvC0', 'https://www.youtube.com/watch?v=S-V5SeXIwH0', 'https://www.youtube.com/watch?v=WYz8dqnj9S8', 'https://www.youtube.com/watch?v=8ysatD8jkSE', 'https://www.youtube.com/watch?v=QFBCDtt5wgU', 'https://www.youtube.com/watch?v=qbASIFA0fA8', 'https://www.youtube.com/watch?v=XY8DJ2i8fLI', 'https://www.youtube.com/watch?v=WHpECBHAEFs', 'https://www.youtube.com/watch?v=MvuCXCkbARQ', 'https://www.youtube.com/watch?v=JngX-B9MND0']
    self.path = '/Users/tangyong/Desktop/download'
    self.initDownload()

  def initDownload(self):
    ssl._create_default_https_context = ssl._create_unverified_context
    urlListLen = len(self.urlList)
    index = 0
    while index < urlListLen:
      self.downloadVideo()
  def show_progress_bar(self, stream, chunk, file_handle):
    # print('stream', stream)
    # print('chunk', chunk)
    print('file_handle', file_handle)

  def downloadVideo(self):
    try:
      yt = YouTube(self.urlList[self.index], proxies=self.proxy_handler, on_progress_callback=self.show_progress_bar)
      yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').last().download(self.path)
      print(yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').last())
      self.index = self.index + 1
      print(self.index)
    except BaseException:
      print(self.index, BaseException)
      time.sleep(5)
      self.downloadVideo()

Download()

# pl = Playlist("https://www.youtube.com/watch?v=JCNyI8ZQIvQ&list=PLlVlyGVtvuVl7QKPkDXCUsRwDxc6Cv8Xj", proxies=proxy_handler)
# pl.download_all(path)

