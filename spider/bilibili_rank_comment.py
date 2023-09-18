 # coding: utf-8

import bilibili_rank as rank
import requests
from lxml import etree
import csv
import json
import time

type_name = ("bangumi","guochan")

# 对单行的操作
def EachRow(url,k,j):
    # 模仿浏览器的headers
    pre_headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    # get请求，传入参数，返回结果集
    resp = requests.get(url,headers=pre_headers)
    # 将结果集的文本转化为树的结构
    tree = etree.HTML(resp.text)
    # 获取详情网页
    comment_url = tree.xpath('/html/body/div[2]/div/div/div[2]/div/div[2]/a/@href')[0]
    word = comment_url.split('/')
    media_id = word[len(word)-1][2:]
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
        'media_id': int(media_id,base=10),
        'ps': 20,
        'sort': 0
    }

    response = requests.get('https://api.bilibili.com/pgc/review/long/list', headers=headers, params=params)

    response.encoding = 'utf-8'                  # 修改编码格式
    try:
        data_json = json.loads(response.text)        # 通过 json 解析数据
        
        if  data_json['data']['count'] != 0:
            list = data_json['data']['list'] 
            # 将长评的简写保存,只保留最新十条长评
            comments = []
            # 不够十条，全部保存
            min_num = min(10,len(list))
            for i in range(0,min_num):
                # 考虑到存在未看番就评论的情况，单独处理
                progress = list[i].get('progress',"无观看记录")
                comment = {
                        'title': list[i]['title'],  # 标题
                        # 评论时间，由时间戳转换
                        'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(list[i]['ctime'])),  
                        'up_name': list[i]['author']['uname'],      # up名
                        'up_uid': list[i]['author']['mid'],      # up的uid
                        'up_progress': progress,
                        'url': list[i]['url'] #长评原地址
                    }
                comments.append(comment)  
            with open("spider\\comment\\"+type_name[k-1]+"\\"+rank.path[k]+"_"+ str(j)+".csv", 'w', newline='', encoding='utf-8') as fp:
                csv_header = ['title','time','up_name','up_uid','up_progress','url']
                csv_writer = csv.DictWriter(fp,csv_header)
                # 如果文件不存在，则写入表头；如果文件已经存在，则直接追加数据不再次写入表头
                if fp.tell() == 0:
                    csv_writer.writeheader()    
                csv_writer.writerows(comments)  # 写入数据
    except Exception as e:
        print("爬取"+rank.path[k]+"的"+str(j)+"名的长评时出现问题！")
        # 这可能是因为该动漫没有长评，甚至没有长评板块






if __name__ == '__main__':

    with open("spider\\rank\\"+rank.path[1]+".csv",'r',encoding='utf-8') as fd :
        reader = csv.reader(fd)
        # 读取每一行
        rows = [row for row in reader]
        for i in range(1,51):
            EachRow(rows[i][7],1,i)

    with open("spider\\rank\\"+rank.path[2]+".csv",'r',encoding='utf-8') as fd :
        reader = csv.reader(fd)
        # 读取每一行
        rows = [row for row in reader]
        for i in range(1,101):
            EachRow(rows[i][7],2,i)
    print("爬取结束！")
