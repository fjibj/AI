#coding:utf-8

word_lst = []
word_dict = {}

exclude_str = " .，。！？、（）【】<>《》=：+-*—“”…0123456789" 

with open("9月销售字.txt","r",encoding='UTF-8') as fileIn ,open("9-out2.txt",'w',encoding='UTF-8') as fileOut:
    
    # 添加每一个字到列表中
    for line in fileIn:
        for char in line:
            word_lst.append(char)

    # 用字典统计每个字出现的个数       
    for char in word_lst:
        if char not in exclude_str:
            if char.strip() not in word_dict: # strip去除各种空白
                word_dict[char] = 1
            else :
                word_dict[char] += 1

    # 排序
    #   x[1]是按字频排序，x[0]则是按字排序
    lstWords = sorted(word_dict.items(), key=lambda x:x[1],  reverse=True) 
   
    # 输出结果 (前100)
    print ('字符\t字频')
    print ('=============')
    for e in lstWords:
        print ('%s\t%d' % e)
        fileOut.write('%s, %d\n' % e)