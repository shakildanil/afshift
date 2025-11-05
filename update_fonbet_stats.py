"""
Скрипт для обновления статистики Фонбет в Google Sheets
"""

import sys
import argparse
from datetime import datetime
from src.fonbet_stats_updater import FonbetStatsUpdater

# Исправляем кодировку для Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(
        description='Обновление статистики Фонбет в Google Sheets'
    )
    parser.add_argument(
        '--year', 
        type=int, 
        help='Год (по умолчанию текущий)'
    )
    parser.add_argument(
        '--month', 
        type=int, 
        help='Месяц (по умолчанию текущий)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Тестовый режим (создает лист "Тест")'
    )
    parser.add_argument(
        '--load-spend',
        action='store_true',
        help='Загружать данные о расходах из существующих листов (по умолчанию: НЕТ)'
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("ОБНОВЛЕНИЕ СТАТИСТИКИ ФОНБЕТ")
    print("=" * 80)
    print()
    
    updater = FonbetStatsUpdater()
    
    try:
        result = updater.update_monthly_stats(
            year=args.year,
            month=args.month,
            test_mode=args.test,
            load_spend_from_sheet=args.load_spend  # По умолчанию False - не трогаем существующие листы
        )
        
        print()
        print("=" * 80)
        print("✅ ОБНОВЛЕНИЕ ЗАВЕРШЕНО УСПЕШНО")
        print("=" * 80)
        print()
        print(f"Лист: {result['sheet_name']}")
        print(f"Источников: {result['sources_count']}")
        print(f"Всего депозитов: {result['total_deposits']}")
        print(f"Общий доход: ${result['total_revenue']:,.2f}")
        print()
        
        return 0
        
    except Exception as e:
        print()
        print("=" * 80)
        print("❌ ОШИБКА")
        print("=" * 80)
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

