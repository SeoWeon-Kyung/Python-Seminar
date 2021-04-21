import re

def csv_num_parsing(line):
    p = re.compile('/D')
    return [float(num) for num in line.strip().split(',') if not p.match(num)]

data = 'DN8007403SJPYQ5T6,5.12219,5.388074,5.184751,5.599218\n'
data_parsed = csv_num_parsing(data)
print(data_parsed)
