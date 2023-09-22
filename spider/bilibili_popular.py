import bilibili_rank as rank
import requests
from lxml import etree
import csv
import json
import time

request_url = "https://api.bilibili.com/x/web-interface/popular"

popular_url = "https://www.bilibili.com/v/popular/all/"

page = 50

headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'referer': popular_url,
        'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31'
    }
params = {
        'ps': 20,
        'pn': page #页数,每一页有20条信息
    }

for i in range(1,page):
    params['pn'] = i
    page = i
    response = requests.get(request_url, headers=headers, params=params)
    response.encoding = 'utf-8'                  # 修改编码格式
    try:
        data_json = json.loads(response.text)        # 通过 json 解析数据
        list = data_json['data']['list']
        comments = []      
        for j in range(len(list)):  
            comment = {
                'title':    list[j]['title'],  # 标题
                'BV':   list[j]['bvid'],  # BV号
                'tname':    list[j]['tname'],  # 类型
                # 评论时间，由时间戳转换
                'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(list[j]['ctime'])),  
                'up_uid':   list[j]['owner']['mid'],      # up的uid
                'up_name':  list[j]['owner']['name'],      # up名
                'view': list[j]['stat']['view'],  # 喜欢
                'like': list[j]['stat']['like'],    #   点赞
                'coin': list[j]['stat']['coin'],    #   投币
                'share': list[j]['stat']['share'],    #   分享
                'rcmd_reason': list[j]['rcmd_reason']['content'],    # 推荐理由
            }
            if not comment['rcmd_reason']:
                comment['rcmd_reason'] = '无推荐理由'
            comments.append(comment)  # 每页的评论数据
        with open("spider\\popular\\"+"popular_rank.csv", 'a', newline='', encoding='utf-8') as fp:
            csv_header = ['title','BV','tname','time','up_uid','up_name','view','like','coin','share','rcmd_reason']
            csv_writer = csv.DictWriter(fp,csv_header,delimiter='\t')
            # 如果文件不存在，则写入表头；如果文件已经存在，则直接追加数据不再次写入表头
            if fp.tell() == 0:
                csv_writer.writeheader()    
            csv_writer.writerows(comments)  # 写入数据
            print("爬取第"+str(20*i-19)+"至第"+str(i*20)+"条成功")
    except Exception as e:
        print("爬取第"+str(20*i-19)+"至第"+str(i*20)+"条失败")
        break



