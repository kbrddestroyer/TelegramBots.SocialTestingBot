import json

with open('test.json', 'r') as f:
    data = json.load(f)
i = 0
test = open('test.txt', 'r')
Lines = test.readlines()
for question in Lines:
    if question == 'stop':
        break
    i += 1
    data['number'] = str(i)
    data[str(i)] = question

n = input('res count> ')
data['res'] = n
for i in range(int(n)):
    data[f'res{i}'] = {}
    data[f'res{i}']['title'] = input('title> ')
    k = input('k> ')
    data[f'res{i}']['add'] = []
    data[f'res{i}']['sub'] = []
    data[f'res{i}']['k'] = k
    data[f'res{i}']['add'] = [int(number) for number in input('add> ').split(', ')]
    data[f'res{i}']['sub'] = [int(number) for number in input('sub> ').split(', ')]
with open('test.json', 'w') as f:
    json.dump(data, f, indent = 4)
