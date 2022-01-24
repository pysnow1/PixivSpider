import requests
import lxml
import re
from bs4 import BeautifulSoup
import time
import random
import os
from fake_useragent import UserAgent
import json
# url='http://api.89ip.cn/tqdl.html?api=1&num=60&port=&address=香港&isp='
# data={
#     'num':	"100",
#     'port':	"",
#     'kill_port':	"",
#     'address':"",
#     'kill_address':"中国",
#     'anonymity':	"",
#     'type':	"",
#     'post':	"",
#     'sort':	"",
#     'key':"7be4a806e1d98c0c4fc39b74403bc7a7"
# }
# # res=requests.post(url=url,data=data)
# # print(res.text)
# res=requests.get(url='http://api.89ip.cn/tqdl.html?api=1&num=60&port=&address=香港&isp=')
# ip_list=re.findall(r'r>(.*?)<b',res.text,re.S)
# del ip_list[0]
# for i in ip_list:
#     i=re.sub('\n','',i)
#     print(i)
word='樱岛麻衣'
# num=input('输入你要爬取图片的数量 ')
# thr=input('输入爬取时使用的线程数量 ')
ipath=r'C:\Users\86185\Desktop\临时文件夹\学习爬虫\PIXIV爬虫\爬取仓库'
uname='3195303848@qq.com'
passwd='946311011bula'
ses=requests.session()
local_proxies={'http': 'http://127.0.0.1:1080', 'https': 'http://127.0.0.1:1080'}

class PixivSpider:
    def __init__(self):
        self.base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        self.login_url = 'https://accounts.pixiv.net/api/login?lang=zh'
        self.target_url = 'http://www.pixiv.net/search.php?word={}&order=date_d&p='.format(word)
        self.main_url='http://www.pixiv.net'
        self.headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
            'referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        }
        self.load_path=ipath
        self.username=uname
        self.password=passwd
        self.return_to='https://www.pixiv.net'
        self.post_key=[]
        self.ip_list=[]

    def login(self):
        html_post_key=ses.get(url=self.base_url,headers=self.headers,proxies=local_proxies).text
        soup_posy_key=BeautifulSoup(html_post_key,'lxml')
        str_key = soup_posy_key.find('input')['value']
        # print(type(self.post_key))
        self.post_key = json.loads(str_key)['pixivAccount.postKey']
        # print(self.post_key)
        print(self.post_key)
        data = {
            'password': self.password,
            'pixiv_id': self.username,
            'post_key': self.post_key,
            'source': 'pc',
            'return_to': self.return_to
        }
        print(data)
        res=ses.post(url=self.login_url,data=data,headers=self.headers,proxies=local_proxies)
        print(res.text)

    def check_login(self):
        content = ses.get(url=self.main_url,headers=self.headers,proxies=local_proxies)
        print(content.status_code)
        print(content.headers)
        print(content.cookies)
        with open('./test.html','w',encoding='utf-8') as f:
            f.write(content.text)
        if '注册' in content.text:
            print('未登陆成功')
        if '注册' in content.text and '插画交流网站' in content.text:
            print('登陆成功')
            print(content.text)


a=PixivSpider()
a.login()
a.check_login()