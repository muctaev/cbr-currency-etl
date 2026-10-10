from extract import fetch_cbr_data
from transform import transform_to_dataframe
from load import load_to_postgres

def run_etl():
    print("=== ЗАПУСК ETL ПАЙПЛАЙНА ===")
    
    print("\n1. [EXTRACT] Отправка запроса к API ЦБ РФ...")
    cbr_json = fetch_cbr_data()
    
    print("2. [TRANSFORM] Очистка и преобразование данных...")
    df_rates = transform_to_dataframe(cbr_json)
    
    print("3. [LOAD] Загрузка данных в PostgreSQL (UPSERT)...")
    load_to_postgres(df_rates)
    
    print("\n=== ETL-ПАЙПЛАЙН УСПЕШНО ЗАВЕРШЕН ===")

if __name__ == "__main__":
    run_etl()