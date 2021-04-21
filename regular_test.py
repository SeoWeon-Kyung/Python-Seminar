import re

p = re.compile(r'[a-zA-Z]')
p2 = re.compile(r'\d+[.]*\d+')
p3 = re.compile(r'([a-zA-Z]*\d*[a-zA-Z]*)[,](.+)')
p4 = re.compile(r'(^\w+)[,](.+)')

data = 'DN8007403SJPYQ5T6,5.12219,5.388074,5.184751,5.599218\n'
comma = ','
data_parsed = data.strip().split(',')

for word in data_parsed:
    m = p.search(word)
    print(m)

m2 = p2.findall(data)
m3 = p3.search(data)
m4 = p4.search(data)
result = p4.sub('\g<2>', data)
print(result)