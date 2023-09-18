 # coding: utf-8

import requests
from lxml import etree
import time
import json
import csv

# 实际的请求网址（接口）'
request_url = (
    "https://api.bilibili.com/x/web-interface/ranking/v2",
    "https://api.bilibili.com/pgc/web/rank/list",
    "https://api.bilibili.com/pgc/season/rank/web/list"
)

# 榜单网址
rank_url = (
    'https://www.bilibili.com/v/popular/rank/all/', # 全站
    'https://www.bilibili.com/v/popular/rank/bangumi/', # 番剧
    'https://www.bilibili.com/v/popular/rank/guochan/' # 国产
)

# 表格名称
path = (
    'all_rank',
    'bangumi_rank',
    'guochan_rank'
)

def GetRank(i):
    # 请求头数据
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'referer': rank_url[i],
        'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31'
    }

    # 构造请求参数
    params = (
        { # 全站参数
            'rid': '0',
            'type': 'all'
        },
        { # 番剧
            'day': 3,
            'season_type': 1
        },
        { # 国产
            'day': 3,
            'season_type': 4
        }
    )

    # 通过get方法请求数据
    response = requests.get(request_url[i], headers=headers, params=params[i])

    response.encoding = 'utf-8'                  # 修改编码格式
    data_json = json.loads(response.text)        # 通过 json 解析数据

    if i == 1:
        list = data_json['result']['list'] 
    else:
        list = data_json['data']['list']
    SaveData(i,list)


def SaveData(j,list):
    comments = []                      
    if j == 0: # 全站
        for i in range(len(list)):  
            comment = {
                'tname': list[i]['tname'],  # 类型
                # 评论时间，由时间戳转换
                'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(list[i]['ctime'])),  
                'title': list[i]['title'],  # 标题
                'up_uid': list[i]['owner']['mid'],      # up的uid
                'up_name': list[i]['owner']['name'],      # up名
                'up_ip': list[i]['pub_location'],  # ip地址
                'BV': list[i]['bvid']  # BV号
            }
            comments.append(comment)  # 每页的评论数据

    elif j == 1: # 番剧
        for i in range(len(list)):
            comment = {
                'name' : list[i]['title'], # 名称
                'badge': list[i]['badge'],  # 特别标注 
                'index_show': list[i]['new_ep']['index_show'], #最新集数
                'view': list[i]['stat']['view'],  # 观看次数
                'rating': list[i]['rating'],      # 评分
                'like': list[i]['stat']['follow'],      # 喜欢人数
                'series_follow': list[i]['stat']['series_follow'],      # 追番人数
                'url': list[i]['url'],  # url地址
                # 需要其他数据的可以再在 json 中查看并获取对应的名称
            }
            comments.append(comment)  # 每页的评论数据
    else: # 国产
        for i in range(len(list)):
            comment = {
                'name' : list[i]['title'], # 名称
                'badge': list[i]['badge'],  # 特别标注 
                'desc': list[i]['desc'], #最新集数
                'view': list[i]['stat']['view'],  # 观看次数
                'rating': list[i]['rating'],      # 评分
                'like': list[i]['stat']['follow'],      # 喜欢人数
                'series_follow': list[i]['stat']['series_follow'],      # 追番人数
                'url': list[i]['url'],  # url地址
                # 需要其他数据的可以再在 json 中查看并获取对应的名称
            }
            comments.append(comment)  # 每页的评论数据
    with open("spider\\rank\\"+path[j]+".csv", 'w', newline='', encoding='utf-8') as fp:
        csv_header = [
            ['title','tname','time','up_uid','up_name','up_ip','BV'],
            ['name','badge','index_show','view','rating','like','series_follow','url'],
            ['name','badge','desc','view','rating','like','series_follow','url']
        ]
        csv_writer = csv.DictWriter(fp,csv_header[j])
        # 如果文件不存在，则写入表头；如果文件已经存在，则直接追加数据不再次写入表头
        if fp.tell() == 0:
            csv_writer.writeheader()    
        csv_writer.writerows(comments)  # 写入数据

if __name__ == '__main__':
    for i in range(0,3):
        print("开始爬取"+path[i]+"榜单")
        GetRank(i)
    print("爬取结束！")