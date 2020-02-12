import urllib.request
import urllib.error
import time
import os
import re
import json


def url_open(url):
	req = urllib.request.Request(url)
	req.add_header("User-Agent","Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36")
	response = urllib.request.urlopen(req)
	return response.read() 

def find_imgs(url):
	response = url_open(url)
	img_addrs = []
	ob_json=json.loads(response)
	for each in ob_json['data']['cards']:
		if('mblog' in each):
			pics = each['mblog']['pics']
			for x in pics:
				img_addrs.append(x['url'])
	# reg = 'img src="([^"]+\.jpg)"'
	# res = re.findall(reg, html)
	return img_addrs

def get_page(url):
	html = url_open(url).decode('utf-8')
	reg = '<a title="Older Comments" href="([^"]+)"'
	res = re.findall(reg, html)
	return 'http:' + res[0]

def save_img(imgs):
	path = "C:/Users/kk/Desktop/github/python/cc/"
	for each in imgs:
		file_name = each.split('/')[-1]
		urllib.request.urlretrieve(each, path + file_name, None)

def down_load(pages=5):
	index = 0
	# url = "https://m.weibo.com/u/6510616905"
	value = "6510616905"
	url = "https://m.weibo.cn/api/container/getIndex?type=uid&value="+value+"&containerid=1076036510616905"
	img_addrs = find_imgs(url)
	save_img(img_addrs)
	# print(img_addrs)
	# while index<5:
	# 	if (index >= pages) :
	# 		break
	# 	else :
	# 		img_addrs = find_imgs(url)
	# 		save_img(img_addrs)
	# 		time.sleep(5)
	# 		url = get_page(url) 
	# 		index = index + 1         
	


if __name__ == '__main__':
	down_load()