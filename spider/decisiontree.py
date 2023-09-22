from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import pandas as pd
from datetime import datetime
import csv
import gen_type_wordcloud
import gen_title

data_path = "spider\\popular\\"+"popular_"+"decision_tree_date.csv"
src_path = 'spider\\popular\\popular_rank.csv'

def GetSource():
    f1 = pd.read_csv(gen_type_wordcloud.hot_type_path,delimiter='\t',encoding='utf-8')
    f2 = pd.read_csv(gen_title.output_path,delimiter='\t',encoding='utf-8')
    # 转换为字典列表
    hot_type = f1.to_dict(orient='records')
    hot_word = f2.to_dict(orient='records')


    with open(src_path, 'r',encoding='utf-8')as f:
        csv_list = csv.reader(f,delimiter='\t')
        next(csv_list)
        data = []
        for row in csv_list:
            if_hot_word = False
            if_hot_type = False
            if_rate = False
            video_time = datetime.strptime(row[3],"%Y-%m-%d %H:%M:%S")

            #   视频发布的时间段
            if video_time.hour < 5:
                period = '凌晨'
            elif video_time.hour < 8 :
                period = '早上'
            elif video_time.hour < 12:
                period = '上午'
            elif video_time.hour < 13:
                period = '中午'
            elif video_time.hour < 19:
                period = '下午'
            elif video_time.hour < 24:
                period = '晚上'

            #   视频标题是否含有热词
            for i in (0,len(hot_word)-1):
                if hot_word[i]['title'] in row[0]:
                    if_hot_word = True
                    break

            #   视频类型是否热门
            for i in (0,len(hot_type)-1):
                if hot_type[i]['tname'] in row[2]:
                    if_hot_type = True
                    break

            #   点赞率是否达到10%
            if (int(row[7]) / int(row[6])) > 0.1 :
                if_rate = True

            each = {
                'week':video_time.isoweekday(),
                'time':period,
                'hot_title':if_hot_word,
                'hot_type':if_hot_type,
                'rate_of_like':if_rate
            }
            data.append(each)


    with open(data_path, 'w', newline='', encoding='utf-8') as fp:
        csv_header = ['week','time','hot_title','hot_type','rate_of_like']
        csv_writer = csv.DictWriter(fp,csv_header,delimiter='\t')
        # 如果文件不存在，则写入表头；如果文件已经存在，则直接追加数据不再次写入表头
        if fp.tell() == 0:
            csv_writer.writeheader()    
        csv_writer.writerows(data)  # 写入数据

    
def descision():

    src = pd.read_csv(data_path,delimiter='\t')
    # 处理数据，找出特征值和目标值
    x = src[['week','time','hot_title','hot_type']]

    y = src['rate_of_like']

    # 分割数据集到训练集和测试集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    # 进行处理(特征工程)
    dict = DictVectorizer(sparse=False)

    x_train = dict.fit_transform(x_train.to_dict(orient="records"))

    x_test = dict.transform(x_test.to_dict(orient="records"))

    # 用决策树进行预测
    dec = DecisionTreeClassifier()

    dec.fit(x_train, y_train)

    # 预测准确率
    print("预测的准确率为：", dec.score(x_test, y_test))

    # 导出决策树的结构
    export_graphviz(dec, out_file="spider\\tree.dot")

if __name__=="__main__":
    GetSource()
    descision()