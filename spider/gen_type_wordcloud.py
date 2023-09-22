import csv
from wordcloud import WordCloud
from matplotlib import pyplot as plt

type_src_path = 'spider\\hadoop\\type\\part-r-00000' #   词语源文件
hot_type_path = 'spider\\type\\hot_type.csv'

cloud_show_words = 15 #   设置显示多少词语
file_show_words = 5 #   设置保存到文件中的词语需要出现的次数

def WriteIntoFile(dic):
    sorted_list = sorted(dic.items(),key=lambda s:s[1],reverse = True)
    with open(hot_type_path,'w',encoding='utf-8',newline='') as fd:
        csv_header = ['tname','counts']
        csv_writer = csv.DictWriter(fd,csv_header,delimiter='\t')
        # 如果文件不存在，则写入表头；如果文件已经存在，则直接追加数据不再次写入表头
        if fd.tell() == 0:
            csv_writer.writeheader()
        csv_list = []
        for row in sorted_list:
            if row[1] > file_show_words:
                each = {
                    'tname':row[0],
                    'counts':row[1],
                }
                csv_list.append(each)
        csv_list.sort(key=lambda k: (k.get('counts')),reverse=True)
        csv_writer.writerows(csv_list)

def GetFreq():
    with open(type_src_path,'r',encoding='utf-8') as f:
        dic={}
        for line in f.readlines():
            line = line.split('\n')
            b = line[0].split('\t') #   将每一行以空格为分隔符转换成列表
            dic[b[0]]=int(b[1])
    del dic['tname']    #   处理数据，去掉多余的标题

    WriteIntoFile(dic)  #   写入文件保存

    count = sum(dic.values())   #   将数量变为词频
    for i in dic:
            dic[i] = dic[i] / count
    print("共有"+str(len(dic))+"种词语")
    return dic

def GetWordCloud(dic):
    wc = WordCloud(
        font_path="STXINWEI.TTF",
        max_words=cloud_show_words,   #   最多显示的词语数量
        width=2000,
        height=1200,
        background_color='white',
        colormap="hsv"
    )
    word_cloud = wc.generate_from_frequencies(dic)
    # 写词云图片
    word_cloud.to_file("wordcloud2.jpg")
    # 显示词云文件
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    dic = GetFreq()
    GetWordCloud(dic)