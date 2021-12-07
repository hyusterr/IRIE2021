#!usr/bin/python3
# encoding: utf-8


import sys

with open(sys.argv[1], 'r') as f:
    data = [i.strip() for i in f.readlines()]

print('topic,doc')
for i in range(0, len(data), 50):
    sub_data = data[i: i + 50]
    idx = sub_data[0].split()[0]
    predictions = " ".join([i.split()[1] for i in sub_data])
    print(f'{idx},{predictions}')
