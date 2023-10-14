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

with open('island_translations.json', 'r', encoding='utf-8') as f:
    i_names = json.load(f)

for name, d in zip(i_names, data[len(names):]):
    assert name[0] == d['fields']['english_name']
    d['fields']['portuguese_name'] = name[1]
    d['fields']['spanish_name'] = name[2]

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
