"""
Тестовый скрипт - проверка разных API AppsFlyer
"""

import requests
import json
import sys
from datetime import datetime, timedelta
from src.config import config

# Исправляем кодировку для Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_pull_api():
    """Тест Pull API (другой вариант AppsFlyer API)"""
    print("=" * 80)
    print("ТЕСТ PULL API")
    print("=" * 80)
    
    api_key = config.APPSFLYER_API_KEY
    app_id = "ru.bkfon-Android"
    
    # Pull API может использовать другой формат
    # https://hq1.appsflyer.com/v1.0/pull/{app_id}/export/in_app_events_report/v5
    
    endpoints = [
        f"https://hq1.appsflyer.com/v1.0/pull/{app_id}/export/in_app_events_report/v5",
        f"https://api2.appsflyer.com/v1.0/pull/{app_id}/export/in_app_events_report/v5",
        f"https://hq1.appsflyer.com/api/pull/{app_id}/export/in_app_events_report/v5",
    ]
    
    to_date = datetime.now() - timedelta(days=1)
    from_date = to_date - timedelta(days=7)
    
    params = {
        "from": from_date.strftime("%Y-%m-%d"),
        "to": to_date.strftime("%Y-%m-%d"),
        "event_name": "af_ftd",
        "timezone": "UTC"
    }
    
    auth_methods = [
        {"Authorization": f"Bearer {api_key}"},
        {"Authorization": api_key},
        {"X-Api-Token": api_key},
        {"api_token": api_key},  # в параметрах
    ]
    
    for endpoint in endpoints:
        print(f"\nТестируем endpoint: {endpoint}")
        for i, headers in enumerate(auth_methods, 1):
            try:
                if "api_token" in headers:
                    # api_token в параметрах
                    test_params = {**params, "api_token": headers["api_token"]}
                    test_headers = {}
                else:
                    test_params = params
                    test_headers = headers
                
                response = requests.get(
                    endpoint,
                    params=test_params,
                    headers=test_headers,
                    timeout=30
                )
                
                print(f"  Метод {i}: {response.status_code}", end="")
                if response.status_code == 200:
                    print(" - SUCCESS!")
                    print(f"  Размер ответа: {len(response.text)} байт")
                    if response.text:
                        lines = response.text.split('\n')
                        print(f"  Строк: {len(lines)}")
                        if len(lines) > 0:
                            print(f"  Первая строка: {lines[0][:100]}")
                    return True
                else:
                    print(f" - {response.text[:100]}")
            except Exception as e:
                print(f"  Метод {i}: Ошибка - {e}")
    
    return False

def test_raw_data_export_with_auth_header():
    """Тест Raw Data Export с Authorization header и api_token в параметрах"""
    print("\n" + "=" * 80)
    print("ТЕСТ RAW DATA EXPORT С КОМБИНАЦИЕЙ МЕТОДОВ")
    print("=" * 80)
    
    api_key = config.APPSFLYER_API_KEY
    app_id = "ru.bkfon-Android"
    
    url = f"https://hq1.appsflyer.com/api/raw-data/export/app/{app_id}/in_app_events_report/v5"
    
    to_date = datetime.now() - timedelta(days=1)
    from_date = to_date - timedelta(days=7)
    
    params = {
        "api_token": api_key,
        "from": from_date.strftime("%Y-%m-%d"),
        "to": to_date.strftime("%Y-%m-%d"),
        "event_name": "af_ftd",
        "timezone": "UTC"
    }
    
    # Комбинация: и параметр, и заголовок
    headers_options = [
        {"Authorization": f"Bearer {api_key}"},
        {"Authorization": api_key},
        {"X-Api-Token": api_key},
        {},
    ]
    
    for i, headers in enumerate(headers_options, 1):
        try:
            print(f"\nКомбинация {i}: params + headers={list(headers.keys())}")
            response = requests.get(url, params=params, headers=headers, timeout=30)
            print(f"Статус: {response.status_code}")
            if response.status_code == 200:
                print("SUCCESS!")
                print(f"Размер: {len(response.text)} байт")
                if response.text:
                    lines = response.text.split('\n')
                    print(f"Строк: {len(lines)}")
                    if len(lines) > 0:
                        print(f"Заголовки: {lines[0]}")
                return True
            else:
                print(f"Ответ: {response.text[:200]}")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    return False

def check_token_format():
    """Проверка формата токена"""
    print("\n" + "=" * 80)
    print("АНАЛИЗ ТОКЕНА")
    print("=" * 80)
    
    api_key = config.APPSFLYER_API_KEY
    print(f"Длина токена: {len(api_key)} символов")
    print(f"Начинается с: {api_key[:20]}...")
    print(f"Заканчивается на: ...{api_key[-20:]}")
    
    # Проверяем, может быть это JWT
    if api_key.count('.') >= 2:
        print("\nПохоже на JWT токен (есть точки разделения)")
        parts = api_key.split('.')
        print(f"Частей: {len(parts)}")
        for i, part in enumerate(parts[:3], 1):
            print(f"  Часть {i}: {len(part)} символов")
    
    # Может быть это API V2 токен (другой формат)
    if len(api_key) > 200:
        print("\nДлинный токен - возможно это зашифрованный токен AppsFlyer")

if __name__ == "__main__":
    check_token_format()
    if not test_raw_data_export_with_auth_header():
        test_pull_api()

