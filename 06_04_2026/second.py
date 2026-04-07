import json

json_data = '''
[
  {"id": 1, "name": "Alice", "age": 22},
  {"id": 2, "name": "Bob", "age": 24},
  {"id": 3, "name": "Charlie", "age": 21},
  {"id": 4, "name": "David", "age": 23},
  {"id": 5, "name": "Eva", "age": 25}
]
'''
data = json.loads(json_data)
print(data[0]["id"])