import json
with open("films.json", 'r') as f:
    films = json.load(f)
a['id'] = 9
a['name'] = 'sdf'
films.append(a)
print(films)