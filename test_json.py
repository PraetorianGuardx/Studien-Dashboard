import json

mein_dict = {"name": "Mathematik", "ects": 5}

with open("test.json", "w") as datei:
    json.dump(mein_dict, datei)

with open("test.json", "r") as datei:
    geladene_datei = json.load(datei)

print(geladene_datei)