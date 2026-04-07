from requests import request
import json

res = request.get("https://jsonplaceholder.typicode.com/todos")
todos = json.loads(res.text)

users = [1, 2, 3]   

def find(todo):
    check = todo["completed"]
    max_var = todo["userId"] in users
    return check and max_var

Value = list(filter(find, todos))

with open("sample.json", "w") as data:
    json.dump(Value, data, indent=2)