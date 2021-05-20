""" romeo.py """
import re

road = "../Python-Seminar/Programming/ProgrammingHW03_Romeo/romeo.txt"
with open(road, 'r') as f:
    text = f.readlines()

    p = re.compile(r'[a-zA-Z]+')
    data = []
    for line in text:
        data += p.findall(line.lower())
    
    data_set = set(data)
    data_dic = {}
    for word in data_set:
        data_dic[word] = data.count(word)
    data_dic = sorted(data_dic.items(), key=lambda x: x[0])
    data_dic = sorted(data_dic, key=lambda x: x[1], reverse=True)
     
    for i in range(20):
        print(data_dic[i])
    
    # Bonus
    p_b = re.compile(r'.', re.DOTALL)
    all_char = []
    for line in text:
        all_char += p_b.findall(line)
    
    all_char = list(set(all_char))
    all_char.sort()
    print(all_char)



    