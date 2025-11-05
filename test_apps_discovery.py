"""
Попытка найти доступные App IDs через разные методы
"""

import requests
import json
import sys
from src.config import config

# Исправляем кодировку для Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_apps_discovery():
    """Попытка найти доступные приложения"""
    print("=" * 80)
    print("ПОИСК ДОСТУПНЫХ ПРИЛОЖЕНИЙ")
    print("=" * 80)
    
    api_key = config.APPSFLYER_API_KEY
    
    # Разные endpoints для получения списка приложений
    endpoints = [
        # Pull API v1.0
        ("https://hq1.appsflyer.com/v1.0/partners/apps", {"Authorization": f"Bearer {api_key}"}),
        ("https://hq1.appsflyer.com/v1.0/partners/apps", {"Authorization": api_key}),
        
        # Raw Data Export API
        ("https://hq1.appsflyer.com/api/raw-data/export/app", {"Authorization": f"Bearer {api_key}"}),
        
        # Apps API
        ("https://hq1.appsflyer.com/api/v1.0/apps", {"Authorization": f"Bearer {api_key}"}),
        ("https://api2.appsflyer.com/v1.0/apps", {"Authorization": f"Bearer {api_key}"}),
        
        # Partners API
        ("https://hq1.appsflyer.com/api/v1.0/partners/apps", {"Authorization": f"Bearer {api_key}"}),
        
        # С api_token в параметрах
        ("https://hq1.appsflyer.com/v1.0/partners/apps", None, {"api_token": api_key}),
    ]
    
    for endpoint_info in endpoints:
        if len(endpoint_info) == 2:
            endpoint, headers = endpoint_info
            params = {}
        else:
            endpoint, headers, params = endpoint_info
        
        try:
            print(f"\nПробуем: {endpoint}")
            if headers:
                print(f"  Headers: {list(headers.keys())}")
            if params:
                print(f"  Params: {list(params.keys())}")
            
            response = requests.get(
                endpoint,
                headers=headers if headers else {},
                params=params,
                timeout=10
            )
            
            print(f"  Статус: {response.status_code}")
            
            if response.status_code == 200:
                print("  SUCCESS!")
                try:
                    data = response.json()
                    print(f"  Ответ (первые 500 символов):")
                    print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
                    
                    # Пытаемся найти App IDs
                    if isinstance(data, dict):
                        if 'apps' in data:
                            apps = data['apps']
                            print(f"\n  Найдено приложений: {len(apps)}")
                            for app in apps[:5]:  # Показываем первые 5
                                app_id = app.get('app_id') or app.get('id') or app.get('bundle_id')
                                app_name = app.get('app_name') or app.get('name')
                                print(f"    - {app_id}: {app_name}")
                    elif isinstance(data, list):
                        print(f"\n  Найдено элементов: {len(data)}")
                        for item in data[:5]:
                            print(f"    - {item}")
                    
                except:
                    print(f"  Ответ (текст): {response.text[:500]}")
                    
            elif response.status_code == 401:
                print(f"  Ошибка 401: Неавторизован")
            elif response.status_code == 403:
                print(f"  Ошибка 403: {response.text[:200]}")
            else:
                print(f"  Ответ: {response.text[:200]}")
                
        except Exception as e:
            print(f"  Ошибка: {e}")

def test_direct_app_access():
    """Прямой доступ к известному App ID с разными форматами"""
    print("\n" + "=" * 80)
    print("ПРЯМОЙ ДОСТУП К APP ID")
    print("=" * 80)
    
    api_key = config.APPSFLYER_API_KEY
    
    # Разные форматы App ID
    app_ids_to_try = [
        "ru.bkfon-Android",
        "id1234567890",  # iOS формат
        "com.bkfon.android",
        "ru.bkfon.android",
    ]
    
    for app_id in app_ids_to_try:
        print(f"\nТестируем App ID: {app_id}")
        
        # Пробуем получить базовую информацию о приложении
        endpoints = [
            f"https://hq1.appsflyer.com/v1.0/apps/{app_id}",
            f"https://hq1.appsflyer.com/api/v1.0/apps/{app_id}",
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(
                    endpoint,
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=10
                )
                print(f"  {endpoint}: {response.status_code}")
                if response.status_code == 200:
                    print(f"  SUCCESS! {response.text[:200]}")
            except:
                pass

if __name__ == "__main__":
    test_apps_discovery()
    test_direct_app_access()

