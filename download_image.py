# 解析網頁
import requests as req
import json
from bs4 import BeautifulSoup as bs
import cloudscraper
from fake_useragent import UserAgent

# 睡眠用
from time import sleep
from random import randint

import os 



ua = UserAgent(cache = True)

my_headers = {
    'user-agent' : ua.random
    }

my_cookies = {
    '__cfruid':'526e8a3666c94a7da2335c462f8fb509bf381305',
    'cf_chl_rc_m':'1',
    '_cfuvid':'lDaoC_62jmMqKfbz',
    'cf_clearance':'ru.QBUcEg22HOQKJDtCwdD4aynIe2zBUCvrI1_t8Ymw',
    'dcsrd':'9V8Tstv5Vm0yFGx0kRYL85aq',
    'cf_chl_2':'66db26ddd8d85a0',
    'cf_chl_prog':'x10'
    
    }

# 要搜尋的版
board = 'pet'

# 建立資料夾
file_path = f'{board}'
if not os.path.exists(file_path):
    os.makedirs(file_path)
    


articles = 30   #一頁幾篇文章
pages = 10       #要爬幾次
page_attr = ''  #api最後一篇文章的元素
ids = []        # 儲存文章的id
img_urls = {}   # 儲存圖片url

#取得文章url
for page in range(pages): 
    try:
        url = f'https://www.dcard.tw/service/api/v2/forums/{board}/posts?popular=false&limit={articles}' + page_attr 

        new_body = cloudscraper.create_scraper().get(url, cookies=my_cookies)
        print(new_body.status_code)

        obj = json.loads(new_body.text)
        
        ids = []
        for i in range(0,articles):
            ids.append(obj[i]['id'])
        
        page_attr = f'&before={ids[-1]}'
        sleep(randint(1,10))
    
    except Exception:
        sleep(randint(1,10))
        continue


    for i in range(len(ids)):
        mediaMetas = obj[i]['mediaMeta']
        for j in range(len(mediaMetas)):
            if mediaMetas[j]['id'] not in img_urls:
                img_urls.update({mediaMetas[j]['id']:mediaMetas[j]['url']})



# 儲存檔案
for link in img_urls.values():
    if 'images' in link:
        with open(f'{file_path}\{link[39:47]}.png', 'wb') as f:
            f.write(req.get(link, 'lxml').content)
    elif 'videos' in link:   #儲存影片
        with open(f'{file_path}\{link[37:45]}.mp4', 'wb') as f:
            res_video = req.get(link)
            soup = bs(res_video.text, 'lxml')
            url_video = soup.select_one('video#dc_player source')['src']
            f.write(req.get(url_video).content)
    elif link[-3:] == 'png' or 'jpg':  # 儲存圖片
        with open(f'{file_path}\{link[-11:-3]}.png', 'wb') as f:
            f.write(req.get(link, 'lxml').content)