# import os
# import stat
import urllib.request

url = "http://tiebapic.baidu.com/forum/pic/item/8fdda144ad34598225f979e91bf431adcbef845e.jpg"
# path='C:/Users/kk/Desktop'
res = urllib.request.urlopen(url)
img = res.read()

with open('1.jpg','wb') as f:
    f.write(img)
