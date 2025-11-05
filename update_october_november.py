"""
Обновление данных за октябрь и ноябрь
"""

import sys
from src.fonbet_stats_updater import FonbetStatsUpdater

# Исправляем кодировку для Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def update_two_months():
    """Обновление за октябрь и ноябрь"""
    print("=" * 80)
    print("ОБНОВЛЕНИЕ ЗА ОКТЯБРЬ И НОЯБРЬ 2025")
    print("=" * 80)
    print()
    
    updater = FonbetStatsUpdater()
    
    # Октябрь 2025
    print("[1/2] Обновление за ОКТЯБРЬ 2025...")
    print("Лист: AF_Stats_Октябрь25")
    print()
    
    try:
        result_oct = updater.update_monthly_stats(
            year=2025,
            month=10,
            load_spend_from_sheet=False
        )
        
        print("✅ Октябрь завершен!")
        print(f"   Источников: {result_oct['sources_count']}")
        print(f"   Депозитов: {result_oct['total_deposits']}")
        print(f"   Revenue: ${result_oct['total_revenue']:,.2f}")
        print()
        
    except Exception as e:
        print(f"❌ Ошибка октябрь: {e}")
        print()
    
    # Ноябрь 2025
    print("[2/2] Обновление за НОЯБРЬ 2025...")
    print("Лист: AF_Stats_Ноябрь25")
    print()
    
    try:
        result_nov = updater.update_monthly_stats(
            year=2025,
            month=11,
            load_spend_from_sheet=False
        )
        
        print("✅ Ноябрь завершен!")
        print(f"   Источников: {result_nov['sources_count']}")
        print(f"   Депозитов: {result_nov['total_deposits']}")
        print(f"   Revenue: ${result_nov['total_revenue']:,.2f}")
        print()
        
    except Exception as e:
        print(f"❌ Ошибка ноябрь: {e}")
        print()
    
    print("=" * 80)
    print("ГОТОВО!")
    print("=" * 80)
    print()
    print("Проверьте листы в Google таблице:")
    print("  - AF_Stats_Октябрь25")
    print("  - AF_Stats_Ноябрь25")
    print()

if __name__ == "__main__":
    update_two_months()

