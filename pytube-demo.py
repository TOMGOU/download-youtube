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
    # self.urlList = ['https://www.youtube.com/watch?v=YjbVRm-zbVo', 'https://www.youtube.com/watch?v=Y9Ckk-dE0nI', 'https://www.youtube.com/watch?v=s8cEFryDOG0', 'https://www.youtube.com/watch?v=2YSPpLqdMxQ', 'https://www.youtube.com/watch?v=j0RBVqJ_C_M', 'https://www.youtube.com/watch?v=PEKJzv4H0P8', 'https://www.youtube.com/watch?v=cunEVSXjv3w', 'https://www.youtube.com/watch?v=eapytZdodfY', 'https://www.youtube.com/watch?v=z5wrxzsn5AA', 'https://www.youtube.com/watch?v=wsfCQypxOCQ', 'https://www.youtube.com/watch?v=ila-fK1qDIQ', 'https://www.youtube.com/watch?v=n50qwytMPlQ', 'https://www.youtube.com/watch?v=pL6byJDDuU0', 'https://www.youtube.com/watch?v=aBa-IuohM20', 'https://www.youtube.com/watch?v=G2ByGcmoMfs', 'https://www.youtube.com/watch?v=NrvkpMrZcFI', 'https://www.youtube.com/watch?v=U2MtWwSVEPY', 'https://www.youtube.com/watch?v=7Ub5VlF-75E', 'https://www.youtube.com/watch?v=rVAuo2m1e28', 'https://www.youtube.com/watch?v=FLCQW8Pop2A', 'https://www.youtube.com/watch?v=wiyimMK9zfE', 'https://www.youtube.com/watch?v=CRIhx4OMMxg', 'https://www.youtube.com/watch?v=YnPoW-IttS0', 'https://www.youtube.com/watch?v=Mz3TBKrBp5M', 'https://www.youtube.com/watch?v=oNCkWW6i3Ww', 'https://www.youtube.com/watch?v=N3K6VuI4XEw', 'https://www.youtube.com/watch?v=SqZMYjXjRIo', 'https://www.youtube.com/watch?v=UEq4FOQrH68']
    self.urlList = ['https://www.tiktok.com/@macrofying/video/6863838877476556037', 'https://www.tiktok.com/@macrofying/video/6861241386084076806']
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
      # yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').last().download(self.path)
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

