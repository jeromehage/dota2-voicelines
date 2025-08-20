import os, json
import pandas as pd

files = [
    'ti13_compendium_caster_list.txt',
    ]

def txt_to_json(file, depth = 10):
    f = open(file, 'r', encoding = 'utf-8')
    data = f.read()
    f.close()

    data = data.replace('"\t\t"', '": "')
    data = data.replace('"\t"', '": "')
    for i in range(1, depth):
        data = data.replace('"\n' + '\t'*i + '{', '":\n' + '\t'*i + '{')
    data = data.replace('"\n', '",\n')
    for i in range(1, depth):
        data = data.replace('",\n' + '\t'*i + '}', '"\n' + '\t'*i + '},')
    for i in range(1, depth):
        data = data.replace('}\n' + '\t'*i + '"', '},\n' + '\t'*i + '"')
    for i in range(1, depth):
        data = data.replace('}\n' + '\t'*i + '}', '},\n' + '\t'*i + '}')
    for i in range(1, depth):
        data = data.replace('},\n' + '\t'*i + '}', '}\n' + '\t'*i + '}')

    print(data[:500])

    data = '\n'.join(data.split('\n')[1:])

    with open(file.replace('.txt', '.json'), 'w', encoding = 'utf-8') as f:
        f.write(data)

def flatten(data):
    out = []
    for k1, v1 in data.items():
        for k2, v2 in v1.items():
            out += [v2 | {'language': k1}]
    return pd.DataFrame(out)

for file in files:
    txt_to_json(file)

for file in files:
    fname = file.replace('.txt', '.json')
    data = json.load(open(fname, encoding = 'utf-8'))
    df = flatten(data)
    df['chatwheels'] = df['chatwheels'].str.split(',')
    df = df.explode('chatwheels')
    fname2 = file.split('_')[0] + '_talent.csv'
    df.to_csv(fname2, sep = ';')
