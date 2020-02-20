# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import time
import os
import re
import json
from lxml import etree
import urllib.parse 


def url_open(url):
	req = urllib.request.Request(url)
	req.add_header("User-Agent","Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36")
	response = urllib.request.urlopen(req)
	print(response)
	res = json.loads(response.read())
	return  res

def find_imgs(url):
	response = url_open(url)
	img_addrs = []
	print(response)
	# ob_json=json.loads(response)
	# for each in ob_json['data']['cards']:
	# 	if('mblog' in each):
	# 		pics = each['mblog']['pics']
	# 		for x in pics:
	# 			img_addrs.append(x['url'])
	# reg = 'img src="([^"]+\.jpg)"'
	# res = re.findall(reg, html)
	return img_addrs

def get_page(url):
	html = url_open(url)
	print(html)
	# reg ='<a href="([^"]+)" class="btn btn-action-reply new-reply"'
	# reg = '<a title="Older Comments" href="([^"]+)"'
	# reg = '<div class="usr-pic">(.*)<'
	# reg = '<div class="usr-pic">[\s\S]*?</div>'
	# res = re.findall(reg, html)
	# for each in res:
	# 	# print(each)
	# 	get_info(each)

# 拿到hmtl模块，从里面提取用户头像和昵称
# 获取到用户的头像是小头像，大头像只需要加一个l就可以； 
# 小头像：https://img3.doubanio.com/icon/u120124746-2.jpg
# 大头像:https://img3.doubanio.com/icon/ul120124746-2.jpg
def get_info(html):
	reg = 'src="(.*?)"'
	img = re.findall(reg, html)[0]
	reg_nickname = '>(.*?)</a>'
	nickname = re.findall(reg_nickname, html)[1]
	print(nickname)
	print(img + '--' + nickname )

# def save_img(imgs):
# 	path = "C:/Users/kk/Desktop/github/python/douban/"
# 	for each in imgs:
# 		file_name = each.split('/')[-1]
# 		urllib.request.urlretrieve(each, path + file_name, None)

# 入口函数，脚本每小时触发一次，自动向数据库中插入最新数据
def down_load(pages=5):
	index = 0
	# url = "https://m.weibo.com/u/6510616905"
	key = urllib.parse.quote('肖战') 
	url = "https://www.duitang.com/napi/blog/list/by_search/?kw="+key+"&start=0&limit=1&include_fields=sender%2Csource_link%2Cis_root%2Cstatus%2Croot_id%2Ctop_comments"
	get_page(url)
	# print(urls[0])
	# get_info(urls[0])

	# for each in urls:
	# 	print(each)
	# save_img(img_addrs)
	# print(img_addrs)
	# while index<5:
	#   if (index >= pages) :
	#       break
	#   else :
	#       img_addrs = find_imgs(url)
	#       save_img(img_addrs)
	#       time.sleep(5)
	#       url = get_page(url) 
	#       index = index + 1         
	
if __name__ == '__main__':
	down_load()