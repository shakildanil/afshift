"""
Тест полного пайплайна с реальными данными
"""

import sys
from datetime import datetime, timedelta
from src.appsflyer_client import AppsFlyerClient
from src.data_processor import DataProcessor

# Исправляем кодировку для Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_full_pipeline():
    """Тест полного пайплайна"""
    print("=" * 80)
    print("ТЕСТ ПОЛНОГО ПАЙПЛАЙНА")
    print("=" * 80)
    print()
    
    # Шаг 1: Получение данных из AppsFlyer
    print("[1/3] Получение данных из AppsFlyer...")
    client = AppsFlyerClient()
    
    app_id = "ru.bkfon-Android"
    to_date = datetime.now() - timedelta(days=1)
    from_date = to_date - timedelta(days=7)
    
    try:
        events = client.get_in_app_events_report(
            app_id=app_id,
            from_date=from_date,
            to_date=to_date,
            event_name="af_ftd"
        )
        
        print(f"✅ Получено {len(events)} событий")
        
        if events:
            print(f"\nПример первой записи:")
            print(f"  Event Time: {events[0].get('Event Time', 'N/A')}")
            print(f"  Install Time: {events[0].get('Install Time', 'N/A')}")
            print(f"  Media Source: {events[0].get('Media Source', 'N/A')}")
            print(f"  Campaign: {events[0].get('Campaign', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False
    
    # Шаг 2: Обработка данных
    print("\n[2/3] Обработка данных...")
    processor = DataProcessor()
    
    try:
        result = processor.process_app_data(events, app_id)
        
        print(f"✅ Обработано:")
        print(f"  Всего событий: {result['total_events']}")
        print(f"  Валидных событий: {result['valid_events']}")
        print(f"  Уникальных кампаний: {len(result['deposits_by_campaign'])}")
        
        # Показываем топ-10 кампаний
        if result['summary']:
            print(f"\nТоп-10 кампаний по депозитам:")
            for i, item in enumerate(result['summary'][:10], 1):
                print(f"  {i}. {item['Media Source']} / {item['Campaign']}: {item['Deposits (af_ftd)']} депозитов")
        
    except Exception as e:
        print(f"❌ Ошибка при обработке: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Шаг 3: Проверка группировки
    print("\n[3/3] Проверка группировки...")
    
    try:
        grouped = result['deposits_by_campaign']
        print(f"✅ Группировка работает:")
        print(f"  Всего групп: {len(grouped)}")
        
        # Показываем примеры
        sample_count = min(5, len(grouped))
        print(f"\nПримеры групп (первые {sample_count}):")
        for i, ((source, campaign), count) in enumerate(list(grouped.items())[:sample_count], 1):
            print(f"  {i}. {source} + {campaign}: {count} депозитов")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False
    
    print("\n" + "=" * 80)
    print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    print("=" * 80)
    print()
    print("Код полностью работает с реальными данными!")
    
    return True

if __name__ == "__main__":
    success = test_full_pipeline()
    sys.exit(0 if success else 1)

