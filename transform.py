import pandas as pd

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