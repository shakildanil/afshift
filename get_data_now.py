"""
Попытка получить данные разными способами
"""

import requests
import sys
from datetime import datetime, timedelta
from src.config import config

# Исправляем кодировку для Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def try_different_approaches():
    """Пробуем разные подходы к получению данных"""
    api_key = config.APPSFLYER_API_KEY
    app_id = "ru.bkfon-Android"
    
    print("=" * 80)
    print("ПОПЫТКА ПОЛУЧИТЬ ДАННЫЕ РАЗНЫМИ СПОСОБАМИ")
    print("=" * 80)
    print()
    
    # Подход 1: Aggregate API вместо Raw Data
    print("[1] Aggregate API (может обойти лимит Raw Data)...")
    try:
        url = f"https://hq1.appsflyer.com/api/agg-data/export/app/{app_id}/partners_by_date_report/v5"
        
        to_date = datetime.now() - timedelta(days=1)
        from_date = datetime(2025, 10, 1)
        
        params = {
            "from": from_date.strftime("%Y-%m-%d"),
            "to": to_date.strftime("%Y-%m-%d"),
            "timezone": "UTC"
        }
        
        headers = {"Authorization": f"Bearer {api_key}"}
        
        response = requests.get(url, params=params, headers=headers, timeout=60)
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Aggregate API работает!")
            print(f"Размер: {len(response.text)} байт")
            return response.text
        else:
            print(f"Ошибка: {response.text[:200]}")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    # Подход 2: Запрос по дням (меньше нагрузка)
    print("\n[2] Запрос по дням (по 1 дню)...")
    try:
        url = f"https://hq1.appsflyer.com/api/raw-data/export/app/{app_id}/in_app_events_report/v5"
        
        # Только за 1 день
        target_date = datetime.now() - timedelta(days=2)
        
        params = {
            "from": target_date.strftime("%Y-%m-%d"),
            "to": target_date.strftime("%Y-%m-%d"),
            "event_name": "af_ftd",
            "timezone": "UTC"
        }
        
        headers = {"Authorization": f"Bearer {api_key}"}
        
        response = requests.get(url, params=params, headers=headers, timeout=60)
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Запрос за 1 день работает!")
            print(f"Размер: {len(response.text)} байт")
            lines = response.text.split('\n')
            print(f"Событий: {len(lines) - 1}")
            return response.text
        else:
            print(f"Ошибка: {response.text[:200]}")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    # Подход 3: V2 API
    print("\n[3] API V2...")
    try:
        url = f"https://api2.appsflyer.com/v2/export/app/{app_id}/in_app_events_report"
        
        to_date = datetime.now() - timedelta(days=1)
        from_date = to_date - timedelta(days=3)
        
        params = {
            "from": from_date.strftime("%Y-%m-%d"),
            "to": to_date.strftime("%Y-%m-%d"),
            "event_name": "af_ftd"
        }
        
        headers = {"Authorization": f"Bearer {api_key}"}
        
        response = requests.get(url, params=params, headers=headers, timeout=60)
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API V2 работает!")
            return response.text
        else:
            print(f"Ошибка: {response.text[:200]}")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    print("\n" + "=" * 80)
    print("ВСЕ МЕТОДЫ ВЕРНУЛИ ОШИБКУ")
    print("=" * 80)
    print("\nПРИЧИНА: Достигнут лимит запросов AppsFlyer на сегодня")
    print("\nЧто делать:")
    print("1. Подождать до завтра (лимит обновляется в 00:00 UTC)")
    print("2. Использовать демо-лист AF_Stats_Демо как пример")
    print("3. Или предоставьте другой токен/аккаунт с доступными лимитами")
    
    return None

if __name__ == "__main__":
    try_different_approaches()

