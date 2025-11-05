"""
Проверка токена и вывод понятных сообщений
"""

import requests
import sys
from datetime import datetime, timedelta
from src.config import config

# Исправляем кодировку для Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_token():
    """Проверка токена с понятными сообщениями"""
    print("=" * 80)
    print("ПРОВЕРКА ТОКЕНА APPSFLYER API")
    print("=" * 80)
    print()
    
    api_key = config.APPSFLYER_API_KEY
    app_id = config.FONBET_ANDROID_APP_ID
    
    print(f"App ID: {app_id}")
    print(f"Длина токена: {len(api_key)} символов")
    print()
    
    url = f"https://hq1.appsflyer.com/api/raw-data/export/app/{app_id}/in_app_events_report/v5"
    
    to_date = datetime.now() - timedelta(days=1)
    from_date = to_date - timedelta(days=7)
    
    params = {
        "from": from_date.strftime("%Y-%m-%d"),
        "to": to_date.strftime("%Y-%m-%d"),
        "event_name": "af_ftd",
        "timezone": "UTC"
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    print(f"Запрос данных за период: {from_date.date()} - {to_date.date()}")
    print(f"URL: {url}")
    print()
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        print(f"Статус ответа: {response.status_code}")
        print()
        
        if response.status_code == 200:
            print("=" * 80)
            print("SUCCESS! Токен работает корректно!")
            print("=" * 80)
            print()
            print(f"Размер ответа: {len(response.text)} байт")
            
            if response.text:
                lines = response.text.split('\n')
                print(f"Строк в ответе: {len(lines)}")
                
                if len(lines) > 0:
                    print(f"\nЗаголовки CSV:")
                    print(lines[0])
                    
                if len(lines) > 1 and lines[1].strip():
                    print(f"\nПервая строка данных:")
                    print(lines[1][:300])
                    
                print(f"\nВсего событий: {len(lines) - 1}")  # -1 для заголовка
                
            return True
            
        elif response.status_code == 401:
            print("=" * 80)
            print("ОШИБКА 401: Неавторизован")
            print("=" * 80)
            print()
            print("Возможные причины:")
            print("  1. Неверный API ключ")
            print("  2. Ключ не передается в заголовке Authorization")
            print("  3. Используется неправильный формат токена")
            print()
            print("Решение:")
            print("  - Проверьте токен в AppsFlyer Dashboard")
            print("  - Убедитесь, что используете Pull API Token")
            print("  - См. инструкции в TOKEN_SETUP.md")
            
        elif response.status_code == 403:
            error_text = response.text
            print("=" * 80)
            print("ОШИБКА 403: Доступ запрещен")
            print("=" * 80)
            print()
            print(f"Ответ сервера: {error_text[:500]}")
            print()
            
            if "Inactive token" in error_text or "inactive" in error_text.lower():
                print("ПРОБЛЕМА: Токен неактивен или истек")
                print()
                print("Что делать:")
                print("  1. Зайдите в AppsFlyer Dashboard")
                print("  2. Перейдите в Settings → API Access")
                print("  3. Проверьте статус токена")
                print("  4. Если токен истек, создайте новый")
                print("  5. Убедитесь, что токен имеет права на Export Data")
                print()
                print("Подробные инструкции: см. TOKEN_SETUP.md")
            else:
                print("Возможные причины:")
                print("  - Нет прав доступа к этому App ID")
                print("  - Токен не имеет нужных разрешений")
                print("  - App ID не существует или недоступен")
                
        elif response.status_code == 404:
            print("=" * 80)
            print("ОШИБКА 404: App ID не найден")
            print("=" * 80)
            print()
            print(f"App ID '{app_id}' не найден в AppsFlyer")
            print()
            print("Что делать:")
            print("  1. Проверьте правильность App ID в AppsFlyer Dashboard")
            print("  2. Убедитесь, что у токена есть доступ к этому приложению")
            print("  3. Проверьте, что приложение добавлено в ваш аккаунт")
            
        else:
            print("=" * 80)
            print(f"ОШИБКА {response.status_code}")
            print("=" * 80)
            print()
            print(f"Ответ сервера: {response.text[:500]}")
            
    except requests.exceptions.RequestException as e:
        print("=" * 80)
        print("ОШИБКА ЗАПРОСА")
        print("=" * 80)
        print()
        print(f"Ошибка: {e}")
        print()
        print("Возможные причины:")
        print("  - Проблемы с интернет-соединением")
        print("  - AppsFlyer API недоступен")
        print("  - Неверный URL")
        
    except Exception as e:
        print("=" * 80)
        print("НЕОЖИДАННАЯ ОШИБКА")
        print("=" * 80)
        print()
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
    
    return False

if __name__ == "__main__":
    success = check_token()
    sys.exit(0 if success else 1)

