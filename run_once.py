"""
Скрипт для однократного запуска обновления статистики
Для быстрого тестирования и ручного запуска
"""

from src.main import update_fonbet_stats
import sys

if __name__ == "__main__":
    print("=" * 80)
    print("ЗАПУСК ОБНОВЛЕНИЯ СТАТИСТИКИ ФОНБЕТ")
    print("=" * 80)
    print()
    
    try:
        result = update_fonbet_stats()
        print("\n✅ Обновление завершено успешно!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)


