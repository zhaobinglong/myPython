#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 微信小程序海报生成脚本
# 1. 合并三张图片为一排

from PIL import Image, ImageDraw,ImageFont
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

# 新建蒙版，为了把二维码变成圆形
def mask(img):
	# 首先获取一个alpha图像:
	mask = Image.new('RGBA', img.size, color=(0,0,0,0))
	# draw = ImageDraw.Draw(alpha_layer)
	# 画一个圆
	mask_draw = ImageDraw.Draw(mask)
	# draw.ellipse((0, 0, w, w), fill=255)
	mask_draw.ellipse((0,0, img.size[0], img.size[1]), fill=(0,0,0,255))
	return mask

# 合并标题部分
def mergeTitle(summary):
	bk = Image.open("bk-middle.png")
	n = 30             # 每一行字的最大数量
	summary_line = 42  # 每行文字的高度
	w = bk.size[0]
	h = (len(summary) // n + 1 ) * summary_line
	bk = bk.resize((w, h),Image.ANTIALIAS)
	draw = ImageDraw.Draw(bk)

	font_type = './SourceHanSansCN-Normal.ttf' # 字体文件
	font = ImageFont.truetype(font_type, 36) # 字体名字和大小
	summary_x = 60     # 文字左边距
	summary_y = 0    # 文字开始张贴的高度
	
	summary_list = [summary[i:i + n] for i in range(0, len(summary), n)]
	for num, summary in enumerate(summary_list):
		y = summary_y + num * summary_line
		draw.text((summary_x, y), u'%s' % summary, "#000000", font)
	return bk

# 合并二维码部分


if __name__ == "__main__":
	id = '1797'
	summary = '习惯在一个任务开始之前，先给自己设立一个看起来不太可能达到的完美标准，并因为这个标准而迟迟无法动手，那你可能也是一个完美主义者'
	
	bk = Image.open("bk.png")
	top_image = Image.open("bk-top.png")

	# 二维码
	qrcodeBytes = getQrcode(id) # 二维码的二进制文件
	flag = Image.open(BytesIO(qrcodeBytes))

	title_image = mergeTitle(summary)
	# response = req.get("https://static.examlab.cn/img/15831632081148511.jpg")


	# 计算缩放比例
	ratio = bk.width/flag.width/4 
	size = (int(flag.width*ratio)-50,int(flag.height*ratio)-50)
	flag = flag.resize(size,Image.ANTIALIAS)#缩放国旗图片

	# 蒙版
	mask = mask(flag)

	# 计算二维码显示的坐标
	x = (bk.width-flag.width)/2
	y = bk.height-flag.height - 130

	box = (int(x),y, int(x) + flag.width, y + flag.height )
	print(top_image.width)
	title_image_start_x = top_image.height
	# bk.paste(flag, box, mask)
	bk.paste(top_image,(0,0))
	bk.paste(title_image,(0,top_image.height))
	bk.save("head_flag.png","png")#合并图片并保存

