import requests
import pandas as pd
import psycopg2 # Добавили библиотеку для работы с PostgreSQL

def fetch_cbr_data():
    """Получает JSON с курсами валют от API Центробанка."""
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url)
    response.raise_for_status() 
    return response.json()

def transform_to_dataframe(raw_data):
    """Преобразует сырой JSON в плоскую таблицу."""
    date_str = raw_data['Date'][:10] 
    target_currencies = ['USD', 'EUR', 'CNY']
    rows = []
    
    for char_code in target_currencies:
        if char_code in raw_data['Valute']:
            valute_info = raw_data['Valute'][char_code]
            row = {
                'date': date_str,
                'currency': char_code,
                'rate': valute_info['Value'],
                'nominal': valute_info['Nominal']
            }
            rows.append(row)
    return pd.DataFrame(rows)

def load_to_postgres(df):
    """
    Загружает DataFrame в таблицу exchange_rates в PostgreSQL.
    """
    db_params = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'pass', 
        'host': 'localhost',
        'port': '5432'
    }
    
    conn = None     
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor() # Курсор нужен для выполнения SQL-команд
        print("\n[DB] Подключение к PostgreSQL успешно установлено.")

        for index, row in df.iterrows():
            insert_query = """
                INSERT INTO exchange_rates (date, currency, rate, nominal)
                VALUES (%s, %s, %s, %s);
            """
            cursor.execute(insert_query, (row['date'], row['currency'], row['rate'], row['nominal']))
        conn.commit()
        print(f"[DB] Успешно загружено {len(df)} записей.")
        
    except psycopg2.Error as e:
        print(f"[DB] Ошибка при работе с базой данных: {e}")
        
    finally:
        if conn is not None:
            cursor.close()
            conn.close()
            print("[DB] Соединение с PostgreSQL закрыто.")

if __name__ == "__main__":
    print("1. Отправка запроса к API ЦБ РФ...")
    cbr_json = fetch_cbr_data()
    
    print("2. Преобразование данных в таблицу...")
    df_rates = transform_to_dataframe(cbr_json)
    print(df_rates)
    
    print("3. Загрузка данных в PostgreSQL...")
    load_to_postgres(df_rates)