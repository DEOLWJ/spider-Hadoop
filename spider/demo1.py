from lxml import etree
from html.parser import HTMLParser
import requests
import json

# 请求头数据
headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'referer': 'https://www.bilibili.com/',
        'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31'
    }

    # 构造请求参数
params = {
        'media_id': 28340121,
        'ps': 20,
        'sort': 0
    }

response = requests.get('https://api.bilibili.com/pgc/review/long/list', headers=headers, params=params)
response.encoding = 'utf-8'                  # 修改编码格式

data_json = json.loads(response.text)        # 通过 json 解析数据
list = data_json['data']['list'] 
print(list[0]['progress'])
