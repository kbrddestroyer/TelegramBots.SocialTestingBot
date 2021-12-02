import json
import codecs
with open('testmain.json', 'r') as f:
    data = json.load(f)

n = int(data["res"])

filename = input('file to read> ')
test = codecs.open( filename, "r", "utf_8_sig" )
Lines = test.readlines()
i = 0
for comm in Lines:
    print (data[f'res{i}']['title'])
    data[f'res{i}']['comm'] = comm
    i+=1

with open('testmain.json', 'w') as f:
    json.dump(data, f, indent = 4)
