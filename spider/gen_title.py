import csv
import jieba

title_src_path = 'spider\\hadoop\\name\\part-m-00000'
output_path = 'spider\\title\\hot_word.csv'

with open(title_src_path,'r',encoding='utf-8') as fd:
    words = jieba.lcut(fd.read())     # 使用精确模式对文本进行分词
    counts = {}     # 通过键值对的形式存储词语及其出现的次数

    for word in words:
        if len(word) == 1:    # 单个词语不计算在内
            continue
        else:
            counts[word] = counts.get(word, 0) + 1    # 遍历所有词语，每出现一次其对应的值加 1

    del counts['title']
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)    # 根据词语出现的次数进行从大到小排序

    '''
    #   在控制台打印满足条件的词语
    for i in range(len(items)):
        word, count = items[i]
        #   出现次数要求
        if count > 5:
            print("{0:<5}{1:>5}".format(word, count))
    '''

with open(output_path,'w',newline='',encoding='utf-8') as fd:
    csv_header = ['title','counts']
    
    csv_writer = csv.DictWriter(fd,csv_header,delimiter='\t')
    # 如果文件不存在，则写入表头；如果文件已经存在，则直接追加数据不再次写入表头
    if fd.tell() == 0:
        csv_writer.writeheader()
    csv_list = []
    for k,v in counts.items():
        if v > 5:
            each = {
                'title':k,
                'counts':v,
            }
            csv_list.append(each)
    csv_list.sort(key=lambda k: (k.get('counts')),reverse=True)
    csv_writer.writerows(csv_list)
