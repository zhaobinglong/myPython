#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 微信小程序海报生成脚本
# 1. 合并三张图片为一排

from PIL import Image, ImageDraw
import requests as req
from io import BytesIO

# import db
# import json

# 测试用帖子 id=1797
# mysql = db.Mysql()
# sql = 'select id,college,cont,imgs  from ershou where id="1797"'
# res = mysql.query(sql)[0]
# print(res)
# print(json.dumps(res['imgs'],ensure_ascii=False))

# 拿到小程序token
def getToken():
	url = "https://examlab.cn/uniapi/weixin.php?action=token"
	response = req.get(url)
	return response.text.strip()


# 通过帖子的id 拿到小程序二维码
def getQrcode(id):
	url = 'https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token=' + getToken()
	data = {"scene": id,"path":'pages/date/detail/index'}

	ret = req.post(url,json=data)

	return ret.content
	# with open('getWXACodeUnlimit.png','wb') as f:
	# 	f.write(ret.content)
	
def cercir(img):
	# 首先获取一个alpha图像:
	# 假设经过前处理后已经有 w == h
	w, h = img.size
	print(img.size)
	# 研究源码后发现，如果使用'1'模式的图像，内部也会转换成'L'，所以直接用'L'即可
	alpha_layer = Image.new('L', (w, w), 0)
	draw = ImageDraw.Draw(alpha_layer)
	draw.ellipse((0, 0, w, w), fill=255)

	# 接着替换图像的alpha层
	return img.putalpha(alpha_layer)


if __name__ == "__main__":
	id = '1797'
	qrcodeBytes = getQrcode(id)

	flag = Image.open(BytesIO(qrcodeBytes))
	print(flag)
	flag = cercir(flag)
	print(flag)
	head = Image.open("bk.png")

	# response = req.get("https://static.examlab.cn/img/15831632081148511.jpg")


	# 计算缩放比例
	ratio = head.width/flag.width/4 
	size = (int(flag.width*ratio),int(flag.height*ratio))
	flag = flag.resize(size,Image.ANTIALIAS)#缩放国旗图片

	# 计算二维码显示的坐标
	position_qrcode = (int((head.width-flag.width)/2),head.height-flag.height-100)
	head.paste(flag, position_qrcode)
	head.save("head_flag.png","png")#合并图片并保存

