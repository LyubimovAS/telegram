import requests
from bs4 import BeautifulSoup

url = "https://meteofor.com.ua/ru/weather-kamyanske-11850/tomorrow/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/118.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

# Проверяем успешность запроса
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    block = soup.find("div", class_="weathertab-wrap")
    
    if block:
        print(block.prettify())  # Выведет весь HTML элемента с отступами
    else:
        print("❌ Элемент .weathertab-wrap не найден. Возможно, контент загружается JavaScript.")
else:
    print(f"Ошибка запроса: {response.status_code}")