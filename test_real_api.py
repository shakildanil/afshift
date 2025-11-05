"""
Тестовый скрипт для проверки реального подключения к AppsFlyer API
"""

import requests
import json
import sys
from datetime import datetime, timedelta
from src.config import config
from src.appsflyer_client import AppsFlyerClient

# Исправляем кодировку для Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_api_connection():
    """Тест подключения к AppsFlyer API"""
    print("=" * 80)
    print("ТЕСТ ПОДКЛЮЧЕНИЯ К APPSFLYER API")
    print("=" * 80)
    print()
    
    # Проверяем API ключ
    api_key = config.APPSFLYER_API_KEY
    print(f"API ключ: {api_key[:50]}...")
    print()
    
    # Проверяем базовый URL
    base_url = config.APPSFLYER_BASE_URL
    print(f"Базовый URL: {base_url}")
    print()
    
    # Проверяем App IDs
    app_ids = config.get_app_ids()
    print(f"App IDs для проверки: {app_ids}")
    print()
    
    # Тестируем разные методы аутентификации
    app_id = app_ids[0] if app_ids else "ru.bkfon-Android"
    
    # Пробуем получить данные за последние 7 дней
    to_date = datetime.now() - timedelta(days=1)
    from_date = to_date - timedelta(days=7)
    
    print(f"Тестирование App ID: {app_id}")
    print(f"Период: {from_date.date()} - {to_date.date()}")
    print(f"Событие: af_ftd")
    print()
    
    # Вариант 1: api_token в параметрах (текущий)
    print("=" * 80)
    print("ВАРИАНТ 1: api_token в параметрах запроса")
    print("=" * 80)
    test_method_1(app_id, from_date, to_date, api_key)
    
    # Вариант 2: Authorization header
    print("\n" + "=" * 80)
    print("ВАРИАНТ 2: Authorization header")
    print("=" * 80)
    test_method_2(app_id, from_date, to_date, api_key)
    
    # Вариант 3: X-Api-Token header
    print("\n" + "=" * 80)
    print("ВАРИАНТ 3: X-Api-Token header")
    print("=" * 80)
    test_method_3(app_id, from_date, to_date, api_key)
    
    # Вариант 4: Bearer token
    print("\n" + "=" * 80)
    print("ВАРИАНТ 4: Bearer token в Authorization")
    print("=" * 80)
    test_method_4(app_id, from_date, to_date, api_key)

def test_method_1(app_id, from_date, to_date, api_key):
    """Метод 1: api_token в параметрах"""
    url = f"{config.APPSFLYER_BASE_URL}/{app_id}/in_app_events_report/v5"
    params = {
        "api_token": api_key,
        "from": from_date.strftime("%Y-%m-%d"),
        "to": to_date.strftime("%Y-%m-%d"),
        "event_name": "af_ftd",
        "timezone": "UTC"
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            print("SUCCESS! Получены данные")
            print(f"Размер ответа: {len(response.text)} байт")
            if response.text:
                lines = response.text.split('\n')
                print(f"Строк в ответе: {len(lines)}")
                if len(lines) > 1:
                    print(f"Заголовки: {lines[0]}")
                    if len(lines) > 1:
                        print(f"Первая строка данных: {lines[1][:200]}")
            return True
        else:
            print(f"Ошибка: {response.status_code}")
            print(f"Ответ: {response.text[:500]}")
    except Exception as e:
        print(f"Ошибка: {e}")
    return False

def test_method_2(app_id, from_date, to_date, api_key):
    """Метод 2: Authorization header"""
    url = f"{config.APPSFLYER_BASE_URL}/{app_id}/in_app_events_report/v5"
    params = {
        "from": from_date.strftime("%Y-%m-%d"),
        "to": to_date.strftime("%Y-%m-%d"),
        "event_name": "af_ftd",
        "timezone": "UTC"
    }
    headers = {
        "Authorization": api_key
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            print("SUCCESS! Получены данные")
            print(f"Размер ответа: {len(response.text)} байт")
            return True
        else:
            print(f"Ошибка: {response.status_code}")
            print(f"Ответ: {response.text[:500]}")
    except Exception as e:
        print(f"Ошибка: {e}")
    return False

def test_method_3(app_id, from_date, to_date, api_key):
    """Метод 3: X-Api-Token header"""
    url = f"{config.APPSFLYER_BASE_URL}/{app_id}/in_app_events_report/v5"
    params = {
        "from": from_date.strftime("%Y-%m-%d"),
        "to": to_date.strftime("%Y-%m-%d"),
        "event_name": "af_ftd",
        "timezone": "UTC"
    }
    headers = {
        "X-Api-Token": api_key
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            print("SUCCESS! Получены данные")
            print(f"Размер ответа: {len(response.text)} байт")
            return True
        else:
            print(f"Ошибка: {response.status_code}")
            print(f"Ответ: {response.text[:500]}")
    except Exception as e:
        print(f"Ошибка: {e}")
    return False

def test_method_4(app_id, from_date, to_date, api_key):
    """Метод 4: Bearer token"""
    url = f"{config.APPSFLYER_BASE_URL}/{app_id}/in_app_events_report/v5"
    params = {
        "from": from_date.strftime("%Y-%m-%d"),
        "to": to_date.strftime("%Y-%m-%d"),
        "event_name": "af_ftd",
        "timezone": "UTC"
    }
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            print("SUCCESS! Получены данные")
            print(f"Размер ответа: {len(response.text)} байт")
            return True
        else:
            print(f"Ошибка: {response.status_code}")
            print(f"Ответ: {response.text[:500]}")
    except Exception as e:
        print(f"Ошибка: {e}")
    return False

def test_list_apps():
    """Попытка получить список доступных приложений"""
    print("\n" + "=" * 80)
    print("ПОПЫТКА ПОЛУЧИТЬ СПИСОК ПРИЛОЖЕНИЙ")
    print("=" * 80)
    print()
    
    api_key = config.APPSFLYER_API_KEY
    
    # AppsFlyer может использовать API для получения списка приложений
    endpoints_to_try = [
        ("https://api2.appsflyer.com/v1.0/partners/apps", {"Authorization": f"Bearer {api_key}"}),
        ("https://hq1.appsflyer.com/api/v1.0/partners/apps", {"Authorization": f"Bearer {api_key}"}),
        ("https://api.appsflyer.com/v1.0/partners/apps", {"Authorization": f"Bearer {api_key}"}),
        ("https://api2.appsflyer.com/v1.0/partners/apps", {"X-Api-Token": api_key}),
    ]
    
    for endpoint, headers in endpoints_to_try:
        try:
            print(f"Пробуем: {endpoint}")
            response = requests.get(endpoint, headers=headers, timeout=10)
            print(f"Статус: {response.status_code}")
            if response.status_code == 200:
                print("SUCCESS!")
                data = response.json()
                print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
                break
            else:
                print(f"Ответ: {response.text[:200]}")
        except Exception as e:
            print(f"Ошибка: {e}")
        print()

if __name__ == "__main__":
    test_api_connection()
    test_list_apps()
