"""
Тест нового токена AppsFlyer
"""

import requests
import sys
from datetime import datetime, timedelta

# Исправляем кодировку для Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Новый токен
NEW_TOKEN = "eyJhbGciOiJBMjU2S1ciLCJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwidHlwIjoiSldUIiwiemlwIjoiREVGIn0.Rx_EtUeaRa2TikH0PzjFx9644SJmaxtYu2Fdv0pOuRtJb_y5Z7n9Dw.nUFaGRl9LW3ChFDm.J-NBMA5lN3mArAIvpHmoR-_dgSMBUc8k3kmP3wRy5BC3vlx4wj8KCuFGajwUDMPUIJT8URiRKNBvcnw-TKtdnhnWvjT3novRhZWMLQZc6NVq4MJImDPTmptzix8zLwKNzjCm9gMJdVSKjEvdGHtG4F9MRBbMRfXMyenoSNd4B8K7lj0P7K3uBN-K22PVEc9S8bLZlypmxX78SiYiq64dh4eqoLa4kQ0xV_I1J8GwgSy9whascOyDzaV5LWt72X9Ax_i6vWQxu7eswAybQDtXNEuGsFCwnZtYjO0g-uQ90yLJOrmL2nVTNkyDlvlGeCCzd6uGb5nb_qSp6yK5TzU8GMrfVw.fRN7ZNEAHxuGeNeLgEPH7g"

def test_new_token():
    """Тест нового токена"""
    print("=" * 80)
    print("ТЕСТ НОВОГО ТОКЕНА APPSFLYER")
    print("=" * 80)
    print()
    
    app_id = "ru.bkfon-Android"
    url = f"https://hq1.appsflyer.com/api/raw-data/export/app/{app_id}/in_app_events_report/v5"
    
    # Пробуем получить данные за последние 7 дней
    to_date = datetime.now() - timedelta(days=1)
    from_date = to_date - timedelta(days=7)
    
    params = {
        "from": from_date.strftime("%Y-%m-%d"),
        "to": to_date.strftime("%Y-%m-%d"),
        "event_name": "af_ftd",
        "timezone": "UTC"
    }
    
    headers = {
        "Authorization": f"Bearer {NEW_TOKEN}"
    }
    
    print(f"App ID: {app_id}")
    print(f"Период: {from_date.date()} - {to_date.date()}")
    print(f"Событие: af_ftd")
    print()
    
    try:
        print("Отправка запроса...")
        response = requests.get(url, params=params, headers=headers, timeout=60)
        
        print(f"Статус: {response.status_code}")
        print()
        
        if response.status_code == 200:
            print("=" * 80)
            print("SUCCESS! Токен работает!")
            print("=" * 80)
            print()
            
            csv_content = response.text
            lines = csv_content.split('\n')
            
            print(f"Размер ответа: {len(csv_content)} байт")
            print(f"Строк в CSV: {len(lines)}")
            print()
            
            if len(lines) > 0:
                print("Заголовки CSV:")
                print(lines[0])
                print()
                
            if len(lines) > 1 and lines[1].strip():
                print("Первая строка данных:")
                print(lines[1][:500])
                print()
                
                # Показываем несколько строк
                print("Примеры данных (первые 5 строк):")
                for i, line in enumerate(lines[1:6], 1):
                    if line.strip():
                        print(f"{i}. {line[:200]}")
                
            print()
            print(f"Всего событий: {len([l for l in lines if l.strip()]) - 1}")  # -1 для заголовка
            
            # Парсим CSV для проверки структуры
            import csv as csv_module
            import io
            csv_reader = csv_module.DictReader(io.StringIO(csv_content))
            data = list(csv_reader)
            
            if data:
                print()
                print("Поля в данных:")
                for key in data[0].keys():
                    print(f"  - {key}")
                
                print()
                print("Пример первой записи:")
                import json
                print(json.dumps(data[0], indent=2, ensure_ascii=False))
            
            return True
            
        elif response.status_code == 401:
            print("=" * 80)
            print("ОШИБКА 401: Неавторизован")
            print("=" * 80)
            print("Токен неверный или формат неправильный")
            print(f"Ответ: {response.text[:500]}")
            
        elif response.status_code == 403:
            error_text = response.text
            print("=" * 80)
            print("ОШИБКА 403: Доступ запрещен")
            print("=" * 80)
            print(f"Ответ: {error_text}")
            
            if "Inactive token" in error_text:
                print("Токен неактивен или истек")
            elif "No access" in error_text or "access" in error_text.lower():
                print("Нет доступа к этому App ID")
                
        elif response.status_code == 404:
            print("=" * 80)
            print("ОШИБКА 404: App ID не найден")
            print("=" * 80)
            print(f"App ID '{app_id}' не найден")
            
        else:
            print("=" * 80)
            print(f"ОШИБКА {response.status_code}")
            print("=" * 80)
            print(f"Ответ: {response.text[:500]}")
            
    except requests.exceptions.Timeout:
        print("=" * 80)
        print("ОШИБКА: Таймаут")
        print("=" * 80)
        print("Запрос занял слишком много времени (>60 сек)")
        print("Возможно, данных очень много")
        
    except Exception as e:
        print("=" * 80)
        print("ОШИБКА")
        print("=" * 80)
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
    
    return False

if __name__ == "__main__":
    success = test_new_token()
    sys.exit(0 if success else 1)

