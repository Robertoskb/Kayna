import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('fix_names.json', 'r', encoding='utf-8') as f:
    names = json.load(f)

for name, d in zip(names, data):
    assert name[0] == d['pk']
    d['fields']['portuguese_name'] = name[1]

with open('fix_snames.json', 'r', encoding='utf-8') as f:
    names = json.load(f)

for name, d in zip(names, data):
    assert name[0] == d['pk']
    d['fields']['spanish_name'] = name[1]

with open('data.json', 'w') as f:
    json.dump(data, f)
