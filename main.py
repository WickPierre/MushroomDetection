import json

with open('names.txt', 'r') as file:
    names = file.read().splitlines()

output = []
for i in names:
    output.append(
        {
        'name': i,
        'attributes': []
        }
    )
with open('names.json', 'w') as file:
    file.write(json.dumps(output))
