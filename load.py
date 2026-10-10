import psycopg2
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

def load_to_postgres(df):
    """Загружает DataFrame в таблицу exchange_rates (UPSERT)."""
    db_params = {
        'host': DB_HOST,
        'port': DB_PORT,
        'dbname': DB_NAME,
        'user': DB_USER,
        'password': DB_PASS
    }
    
    conn = None 
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        print("[DB] Подключение к PostgreSQL успешно установлено.")
        
        for index, row in df.iterrows():
            upsert_query = """
                INSERT INTO exchange_rates (date, currency, rate, nominal)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (date, currency) 
                DO UPDATE SET 
                    rate = EXCLUDED.rate,
                    nominal = EXCLUDED.nominal,
                    loaded_at = NOW();
            """
            cursor.execute(upsert_query, (row['date'], row['currency'], row['rate'], row['nominal']))
        
        conn.commit()
        print(f"[DB] Успешно обработано {len(df)} записей (INSERT/UPDATE).")
        
    except psycopg2.Error as e:
        print(f"[DB] Ошибка при работе с базой данных: {e}")
        if conn is not None:
            conn.rollback() 
            
    finally:
        if conn is not None:
            cursor.close()
            conn.close()
            print("[DB] Соединение с PostgreSQL закрыто.")