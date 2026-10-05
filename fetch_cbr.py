import requests

def fetch_cbr_data():
    """
    Функция делает GET-запрос к API Центробанка и возвращает JSON с курсами валют.
    """
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url)
    response.raise_for_status() 
    data = response.json()
    return data

if __name__ == "__main__":
    print("Отправка запроса к API ЦБ РФ...")
    cbr_json = fetch_cbr_data()
    print(f"Данные успешно получены за дату: {cbr_json['Date']}")
    print("Пример данных по USD:")
    print(cbr_json['Valute']['USD'])