import sys
import urllib.request
import urllib.error
import time
import os
import re
import json
from urllib import parse
import ssl
from bs4 import BeautifulSoup
import db
from phpserialize import *
 
def loadPage(url, filename):
    """
        作用：根据url发送请求，获取服务器响应文件
        url: 需要爬取的url地址
        filename : 处理的文件名
    """
    print ("正在下载 " + filename)
    req = urllib.request.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(req,context=context)
    # print(response.read() )
    return response.read() 
    # # request = urllib.Request(url, headers = headers)
    # html = urlopen(url).read().decode("utf-8")
    # # print(html.read().decode("utf-8"))
    # print(html)
    # return html

#
def pageDetail(id):
    """
        作用：根据帖子的id，拼接出来完整的url，读取帖子详情
        html：id
    """
    
    url = "http://tieba.baidu.com/p/" + id
    html = loadPage(url, url).decode('utf-8')
    print(url)
    soup = BeautifulSoup(html,'lxml')
    # print(soup.prettify())
    
    # 读取帖子的标题 
    reg = '<h1 class="core_title_txt  " title="(.*?)"'
    res = re.findall(reg, html)[0]
    # print(res)
    
    # 读取帖子楼主发布的内容
    regContent = 'class="d_post_content j_d_post_content  clearfix" style="display:;">([\s\S]*?)</div>'
    resContent = re.findall(regContent, html)[0] 
    
    # 取出楼主帖子中所有的图片
    reImg = 'src="(.*?)"'
    resImg = re.findall(reImg, resContent)
    
    # 提取用户昵称
    soup = BeautifulSoup(html,'lxml')
    nickname = soup.find_all("a", class_="p_author_name j_user_card",limit=1)[0].get_text()
    
    # 提取用户头像
    regAvatar = '<img username="(.*?)" class="" src="(.*?)"'
    resAvatar = re.findall(regAvatar, html)[0]
    # print(resAvatar)
    
    # 提取用户id
    regUserId = 'user_id":(.*?),'
    resUserId = re.findall(regUserId, html)[0]
    
    # print('id：' + id)
    # print('昵称:' + nickname )  
    # print('openid:' + 'tieba-' + resUserId)
    # print('头像:' + resAvatar[0])
    # print('标题:' + res)
    # print('内容:' + re.sub('<img (.*?)>', "", resContent).strip())
    # print(resImg)
    # print(dumps(resImg))
    # print(li)
    # for each in li:
    #     print(each)
    #     print(type(each))
    #     print(each.slect('a'))
    userInfo = {
      'openid': 'tieba-' + resUserId,
      'nickName': nickname,
      'avatarUrl': resAvatar[1]
    }
    content = {
        'title': res,
        'cont': re.sub('<img (.*?)>', "", resContent).strip(),
        'imgs': dumps(resImg).decode('utf-8'),
        'openid': 'tieba-' + resUserId,
        'belong': 'tieba-' + id,  # belong用来防止出现重复的帖子
        'college': '西安外国语大学',
        'createtime': int(time.time())
    }

    saveInfo(userInfo, content)
def saveInfo(info, content):
    """
        作用：保存用户数据和帖子数据到数据库
        info：用户数据字典
        content：帖子数据
    """
    # print(content)
    mysql = db.Mysql()
    saveContent(mysql, content)
    saveUser(mysql, info)
    mysql.end()

# 保存帖子信息
def saveContent(mysql,cont):
    sql = 'select id from ershou where belong="'+cont['belong']+'"'
    res = mysql.query(sql)
    print(res)
    if (len(res) > 0):
        print('帖子已经被插入数据库，不再插入')
    else :
        sql = '''insert into 
        ershou(openid,title,cont,imgs,college,createtime,updatetime,belong) 
        value('%s','%s','%s','%s','%s','%s','%s','%s')
        '''
        sql = sql%(cont['openid'],cont['title'],cont['cont'],cont['imgs'],cont['college'],cont['createtime'],cont['createtime'],cont['belong'])
        # print(sql)
        res = mysql.query(sql)
        print(res)

# 保存用户信息到数据库
def saveUser(mysql, info):
    sql = 'select id from user where openid="%s"'%(info['openid'])
    res = mysql.query(sql)
    if (len(res) > 0):
        print('用户已经被插入数据库，不再插入')
    else :
        sql = '''insert into 
        user(openid,nickName,avatarUrl) 
        value('%s','%s','%s')
        '''%(info['openid'],info['nickName'],info['avatarUrl'])
        print(sql)
        res = mysql.query(sql)
        print(res)

def writePage(html, filename):
    """
        作用：获取首页的所有的帖子 id
        html：服务器相应文件内容
    """
    # reg = '<div class="ti_title">([\s\S]*?)</div>'
    # reg = '<a rel="noreferrer" href="/p/(.*?)"'
    # reg = 'data-tid="(.*?)" data-tasktype="" data-floor='
    reg = 'href="/p/(\d+?)" title="(.*?)"'
    res = re.findall(reg, html)
    arr = []
    for each in res:
        # print(each)
        # print(each[0])
        # print(each[1])
        if(each[1].find('吧规') != -1 ):
            print("===============")
        elif(each[1].find('集中') != -1):
            print("===============")
        else:
            arr.append(each)
    # print(arr)
        # get_info(each
    # pageDetail('6252332220')
    # tie_nums = re.findall('<a href="/p/(.*?)" title="', html, re.S)
    # for num in arr:
    #     print(num)
    pageDetail(arr[0][0])

def tiebaSpider(url, beginPage, endPage):
    """
        作用：贴吧爬虫调度器，负责组合处理每个页面的url
        url : 贴吧url的前部分
        beginPage : 起始页
        endPage : 结束页
    """
    for page in range(beginPage, endPage + 1):
        pn = (page - 1) * 50
        filename = "第" + str(page) + "页.html"
        fullurl = url + "&pn=" + str(pn)
        # print (fullurl)
        html = loadPage(fullurl, filename).decode('utf-8')
        # print(html)
        writePage(html, filename)
    # pageDetail('6183754479')
    print ("谢谢使用")
 
if __name__ == "__main__":
    # kw = input("请输入需要爬取的贴吧名:")
    # beginPage = int(input("请输入起始页："))
    # endPage = int(input("请输入结束页："))
 
    url = "http://tieba.baidu.com/f?"
    key = parse.urlencode({"kw": '西安外国语大学'}) #.encode("utf-8")
    fullurl = url + key
    tiebaSpider(fullurl, 1, 1)
    # print(parse.urlencode("关于Python在"))
    # print("key",key)
    # print(parse.urlencode({"kw":"除了web开发以外，还有其他吗？"}))
    # html = urlopen("http://tieba.baidu.com/f?kw=python&pn=100")

    # print(html.read().decode("utf-8"))