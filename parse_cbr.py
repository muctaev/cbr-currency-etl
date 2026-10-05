import pandas as pd
from fetch_cbr import fetch_cbr_data

def parse_to_dataframe(raw_json):
    """
    Функция принимает сырой JSON, достает нужные валюты 
    и превращает их в DataFrame (таблицу).
    """
    # 1. Достаем дату из ответа
    raw_date = raw_json['Date'][:10]
    
    # 2. Задаем список валют, которые будем отслеживать
    target_currencies = ['USD', 'EUR', 'CNY']

    parsed_data = []

    valute_dict = raw_json['Valute']
    
    # 3. Проходимся циклом только по нужным нам валютам
    for currency_code in target_currencies:
        if currency_code in valute_dict:
            currency_info = valute_dict[currency_code]

            row = {
                'date': raw_date,
                'currency': currency_code,
                'rate': currency_info['Value'],      # Текущий курс
                'nominal': currency_info['Nominal']  # Номинал 
            }
            parsed_data.append(row) # Добавляем строку в общий список

    df = pd.DataFrame(parsed_data)
    
    return df

# Блок для проверки скрипта
if __name__ == "__main__":
    print("1. Получаем данные из API...")
    raw_data = fetch_cbr_data()
    
    print("2. Парсим JSON и создаем DataFrame...")
    df = parse_to_dataframe(raw_data)

    print("\nИтоговая таблица:")
    print(df)
    
    print("\n3. Сохраняем в файл exchange_rates.csv...")
    df.to_csv('exchange_rates.csv', index=False)
    print("Готово! Проверь папку проекта.")