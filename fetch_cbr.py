# Импортируем библиотеку requests для отправки HTTP-запросов
import requests

def fetch_cbr_data():
    """
    Функция делает GET-запрос к API Центробанка и возвращает JSON с курсами валют.
    """
    # Бесплатный URL API ЦБ РФ, который отдает данные в формате JSON
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    
    # Отправляем GET-запрос по указанному URL
    response = requests.get(url)
    
    # Проверяем, что сервер ответил успешно (код 200 OK)
    response.raise_for_status() 
    
    # Преобразуем ответ сервера в Python-словарь (парсим JSON)
    data = response.json()
    
    return data

# Этот блок выполнится только если запускать скрипт напрямую
if __name__ == "__main__":
    print("Отправка запроса к API ЦБ РФ...")
    
    # Вызываем функцию
    cbr_json = fetch_cbr_data()
    
    # Выводим дату, за которую получены данные (чтобы убедиться, что всё работает)
    print(f"Данные успешно получены за дату: {cbr_json['Date']}")
    
    # Для наглядности выведем сырые данные по одной валюте (например, USD)
    print("Пример данных по USD:")
    print(cbr_json['Valute']['USD'])