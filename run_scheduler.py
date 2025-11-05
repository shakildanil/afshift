"""
Скрипт для запуска планировщика
Обновление будет происходить автоматически каждый день в 10:00
"""

from src.scheduler import StatisticsScheduler
import sys

if __name__ == "__main__":
    print("=" * 80)
    print("ЗАПУСК ПЛАНИРОВЩИКА ОБНОВЛЕНИЯ СТАТИСТИКИ ФОНБЕТ")
    print("=" * 80)
    print()
    print("⏰ Планировщик запущен")
    print("📅 Обновление будет происходить каждый день в 10:00")
    print("⏹️  Для остановки нажмите Ctrl+C")
    print()
    
    try:
        scheduler = StatisticsScheduler()
        scheduler.run()
    except KeyboardInterrupt:
        print("\n\n⏹️  Планировщик остановлен")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)


