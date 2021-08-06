# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json


# Выполним выгрузку данных о репозиториях юзера defunkt

url = 'https://api.github.com/users/defunkt/repos'
req = requests.get(url)

data = json.loads(req.text)

# Сохраним данные в .json

with open('defunkt_repos.json', 'w') as outfile:
    json.dump(data, outfile)
