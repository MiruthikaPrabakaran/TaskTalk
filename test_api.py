import requests

url = "http://127.0.0.1:5000/api/tasks/1"

task = {
    "title": "Complete TaskTalk API",
    "priority": "NORMAL"
}

response = requests.put(url, json=task)

print(response.status_code)
print(response.json())