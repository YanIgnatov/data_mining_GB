# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.


import requests

# Выбранная мной API генерирует случайное имя. Авторизация происходит через передачу в хеддере запроса ключа

headers = {
    'X-Api-Key': '61f44e2aa9294649bde8dfad4f5905c9'
}

#

url = 'https://randommer.io/api/Name?nameType=fullname&quantity=1'
req = requests.get(url, headers=headers)
print(req)

with open("log.txt", "w") as f:
    f.write(req.text)
