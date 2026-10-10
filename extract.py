import requests

def fetch_cbr_data():
    """Получает JSON с курсами валют от API Центробанка."""
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url)
    response.raise_for_status() 
    return response.json()