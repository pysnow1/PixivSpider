import requests
import lxml
import re
from bs4 import BeautifulSoup
import time
import random
import os
from fake_useragent import UserAgent
import json

# word=input('输入你想要爬取的关键词 ')
# num=input('输入你要爬取图片的数量 ')
# thr=input('输入爬取时使用的线程数量 ')
# path=input('输入你要保存的路径')
# uname=input('请输入你的pixiv账号')
# passwd=input('请输入你的pixiv密码')

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
        self.base_url = r'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        self.login_url = r'https://accounts.pixiv.net/api/login?lang=zh'
        self.target_url = r'https://www.pixiv.net/tags/{}/illustrations'.format(word)
        self.main_url=r'http://www.pixiv.net'
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

    def login(self,mode):
        if mode == 1:
            html_post_key=ses.get(url=self.base_url,headers=self.headers,proxies=local_proxies).text
            soup_posy_key=BeautifulSoup(html_post_key,'lxml')
            str_key=soup_posy_key.find('input')['value']
            # print(type(self.post_key))
            self.post_key=json.loads(str_key)['pixivAccount.postKey']
            # print(self.post_key)
            print(self.login_url)
            data={
                'password': self.password,
                'pixiv_id': self.username,
                'post_key': self.post_key,
                'return_to': self.return_to
            }
            html1=ses.post(url=self.login_url,data=data,headers=self.headers,proxies=local_proxies)
            html=ses.post(url=self.login_url,data=data,headers=self.headers,proxies=local_proxies)
            with open('./test.html','w',encoding='utf-8') as f:
                f.write(html.text)
            print(html.headers)
        if mode == 2:
            self.headers.update({
                'cookie':r'first_visit_datetime_pc=2022-01-24+03%3A45%3A58; yuid_b=QEdUQxk; tags_sended=1; categorized_tags=-L-4bBqjrT~IVwLyT8B6k~RcahSSzeRf~WaBG1SNo80~ZNRc-RnkNl~bxDP1gMngT~tiC_2L6Ex9; _im_vid=01FT4BS92016GKAHMP0VE22NB8; _im_uid.3929=b.7b029255a0abf03b; QSI_S_ZN_5hF4My7Ad6VNNAi=r:10:4; _gat=1; p_ab_id=2; p_ab_id_2=0; p_ab_d_id=255878383; _ga=GA1.2.889938432.1642981372; _gid=GA1.2.505017385.1642981372; __cf_bm=j73IDvYIADGQ8EuW06hjRbflWowVquoNA3vkIxjjPzc-1642981372-0-AXuafalkBT+YMiCWqQY5OTkSs9NaWesj3DiQWB1mANhl4OY1gwu+lixXC+e2+MGQ+vzHthrzDpDMd3y6jUWYmL6QI7uvNqRZKc7rHhv7fY/psccJPkjDOZh6vlUV3xw3fs4nVOq6XCqRmnZGfT+HTzQgioIAT2gKZRleQNT6PXcs8yEW68YGPGJKNf2ioDscsA==; PHPSESSID=64022433_OyS0JGQV20bLA5fS9qJMhBti7hNGOR9q; device_token=0bd07f3287a37856f14330e4b906e0b8; privacy_policy_agreement=3'
            })
            print(self.headers)
            ses.get(url=self.main_url,headers=self.headers,proxies=local_proxies)
        # print(res.text)

    def check_login(self):
        content=ses.get(url=self.main_url,headers=self.headers,proxies=local_proxies)
        print(content.status_code)
        print(content.headers)
        print(content.cookies)
        if '注册' in content.text:
            print('未登陆成功')
        if '注册' in content.text and '插画交流网站' in content.text:
            print('登陆成功')
            print(content.text)

    def get_proxy(self):
        __res = requests.get(url='http://api.89ip.cn/tqdl.html?api=1&num=60&port=&address=香港&isp=')
        __ip_list = re.findall(r'r>(.*?)<b', __res.text, re.S)
        del __ip_list[0]
        for i in __ip_list:
            i = re.sub('\n', '', i)
            self.ip_list.append(i.strip())
            # print(i.strip())
        if self.ip_list:
            print('IP代理池已获取完毕')

    def get_html(self,url ,time_out, proxy=local_proxies, num_entries=6):
        print(url)
        if proxy == local_proxies:
            try:

                return ses.get(url=url,headers=self.headers,timeout=time_out,proxies=local_proxies)
            except:
                if num_entries > 0:
                    print('网页获取错误，5秒后重新获取，倒数第',num_entries,'次')
                    time.sleep(5)
                    return self.get_html(url,time_out,num_entries=num_entries-1,proxy=local_proxies)
                else:
                    print('开始切换代理')
                    ip=''.join(str(random.choice(self.ip_list)))
                    now_proxy={'http':ip}
                    return self.get_html(url,time_out,proxy=now_proxy)

        else:
            try:
                return ses.get(url=url, headers=self.headers, timeout=time_out, proxies=proxy)
            except:
                if num_entries > 0:
                    print('正在切换代理，5秒后将重新获取，倒数第',num_entries,'次')
                    time.sleep(5)
                    ip=''.join(str(random.choice(self.ip_list)))
                    now_proxy={'http':ip}
                    return self.get_html(url,time_out,proxy=now_proxy,num_entries=num_entries-1)
                else:
                    print('使用代理失败,取消代理')
                    return self.get_html(url,time_out)

    def get_image(self,html,page_num):
        print(html)
        # with open('./test.html','w',encoding='utf-8') as f:
        #     f.write(html)
        li_soup=BeautifulSoup(html,'lxml')
        li_location=li_soup.findAll('li', attrs={'class',"sc-l7cibp-2 gpVAva"})
        print(li_location)
        for list in li_location:
            href=list.find('a')['href']
            print(href)
            jumping_url=self.main_url+href
            jumping_html=self.get_html(jumping_url,3)

            image_soup=BeautifulSoup(jumping_html,'lxml')
            image_info=image_soup.find('div', attrs={'class','sc-1qpw8k9-0 gTFqQV'})\
            .find('a', attrs={'class','sc-1qpw8k9-3 eFhoug gtm-expand-full-size-illust'})
            if image_info is None:
                continue
            self.download_image(image_info, jumping_url, page_num)

    def download_image(self,image_info ,href ,page_num):
        title=image_info.find('img')['alt']
        src=image_info.find('img')['src']
        src_headers=self.headers
        src_headers['Referer']=href
        try:
            img=requests.get(url=src,headers=src_headers).content
        except:
            print('下载图片',title,'失败')
            return False
        title = title.replace('?', '_').replace('/', '_').replace('\\', '_').replace('*', '_').replace('|', '_') \
        .replace('>', '_').replace('<', '_').replace(':', '_').replace('"', '_').strip()

        if os.path.exists(os.path.join(self.load_path,str(page_num),title+'jpg')):
            for i in range(100):
                if not os.path.exists(os.path.join(self.load_path,str(page_num),title+str(i)+'jpg')):
                    title=title+str(i)
                    break
        now_path=os.path.join(self.load_path,str(page_num),title+'jpg')
        print('正在保存'+title+'图片')
        with open(now_path,'wb') as f:
            f.write(img)

    def mkdir(self,path):
        path = path.strip()
        is_exist=os.path.exists(os.path.join(self.load_path,path))
        if not is_exist:
            print('创建一个名字为'+path+'的文件夹')
            os.makedirs(os.path.join(self.load_path,path))
            return True
        else:
            print(path+' 文件夹已经存在')
            return False

    def work(self):
        print('进入工作方法')
        self.login(2)
        # 登陆
        self.check_login()
        self.get_proxy()
        # 获取代理池
        for page_num in range(1,51):
            path=str(page_num)
            self.mkdir(path)
            now_html=self.get_html(self.target_url,3).text
            self.get_image(now_html,path)
            print('第'+path+'页已经爬取完毕')
            time.sleep(3)





if __name__ == '__main__':
    pixiv_spider=PixivSpider()
    pixiv_spider.work()
