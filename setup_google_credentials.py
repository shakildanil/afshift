"""
Скрипт для помощи в настройке Google Sheets API
"""

import os
import sys

def check_credentials():
    """Проверка наличия файла credentials.json"""
    if os.path.exists("credentials.json"):
        print("✅ Файл credentials.json найден")
        return True
    else:
        print("❌ Файл credentials.json не найден")
        return False

def check_token():
    """Проверка наличия файла token.json"""
    if os.path.exists("token.json"):
        print("✅ Файл token.json найден (авторизация уже выполнена)")
        return True
    else:
        print("⚠️  Файл token.json не найден (требуется первичная авторизация)")
        return False

def print_instructions():
    """Вывод инструкций по настройке"""
    print("\n" + "=" * 80)
    print("НАСТРОЙКА GOOGLE SHEETS API")
    print("=" * 80)
    print()
    
    if not check_credentials():
        print("\n📋 Инструкция по получению credentials.json:")
        print()
        print("1. Перейдите в Google Cloud Console:")
        print("   https://console.cloud.google.com/")
        print()
        print("2. Создайте новый проект или выберите существующий")
        print()
        print("3. Включите Google Sheets API:")
        print("   - APIs & Services > Library")
        print("   - Найдите 'Google Sheets API'")
        print("   - Нажмите 'Enable'")
        print()
        print("4. Создайте OAuth 2.0 credentials:")
        print("   - APIs & Services > Credentials")
        print("   - Create Credentials > OAuth client ID")
        print("   - Application type: Desktop app")
        print("   - Скачайте JSON файл")
        print()
        print("5. Переименуйте скачанный файл в 'credentials.json'")
        print("   и поместите в корень проекта")
        print()
        return False
    
    check_token()
    
    print("\n" + "=" * 80)
    print()
    print("✅ Настройка завершена!")
    print()
    print("Для первого запуска выполните:")
    print("  python run_once.py")
    print()
    print("Откроется браузер для авторизации в Google.")
    print("После авторизации токен будет сохранен в token.json")
    print()
    
    return True

def test_connection():
    """Тестирование подключения к Google Sheets"""
    try:
        from src.google_sheets_updater import GoogleSheetsUpdater
        
        print("\n🔄 Тестирование подключения к Google Sheets...")
        
        updater = GoogleSheetsUpdater()
        updater.authenticate()
        
        print("✅ Подключение к Google Sheets успешно!")
        return True
        
    except FileNotFoundError as e:
        print(f"❌ Ошибка: {e}")
        return False
    except Exception as e:
        print(f"❌ Ошибка при подключении: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("ПРОВЕРКА НАСТРОЕК GOOGLE SHEETS API")
    print("=" * 80)
    
    if print_instructions():
        print("\n" + "=" * 80)
        choice = input("\nХотите протестировать подключение? (y/n): ")
        
        if choice.lower() == 'y':
            if test_connection():
                sys.exit(0)
            else:
                sys.exit(1)
    else:
        sys.exit(1)


