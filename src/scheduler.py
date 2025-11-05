"""
Планировщик задач для автоматического обновления данных
"""

import schedule
import time
import logging
from datetime import datetime

from src.config import config
from src.fonbet_stats_updater import FonbetStatsUpdater

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StatisticsScheduler:
    """Планировщик для автоматического обновления статистики"""
    
    def __init__(self, schedule_time: str = None):
        """
        Инициализация планировщика
        
        Args:
            schedule_time: Время запуска в формате "HH:MM"
        """
        self.schedule_time = schedule_time or config.SCHEDULE_TIME
    
    def scheduled_job(self):
        """Задача для выполнения по расписанию"""
        logger.info(f"Запуск обновления статистики в {datetime.now()}")
        
        try:
            updater = FonbetStatsUpdater()
            result = updater.update_monthly_stats()
            logger.info(f"Обновление статистики завершено успешно: {result['sheet_name']}")
        except Exception as e:
            logger.error(f"Ошибка при обновлении статистики: {e}", exc_info=True)
    
    def run(self):
        """Запуск планировщика"""
        logger.info(f"Планировщик запущен. Обновление будет происходить каждый день в {self.schedule_time}")
        
        # Настраиваем расписание
        schedule.every().day.at(self.schedule_time).do(self.scheduled_job)
        
        # Бесконечный цикл для выполнения задач
        while True:
            schedule.run_pending()
            time.sleep(60)  # Проверяем каждую минуту
    
    def run_once(self):
        """Однократное выполнение задачи (для тестирования)"""
        logger.info("Однократное выполнение обновления статистики")
        self.scheduled_job()


def main():
    """Точка входа для запуска планировщика"""
    scheduler = StatisticsScheduler()
    
    # Можно запустить сразу при старте (опционально)
    # scheduler.run_once()
    
    # Запускаем планировщик
    scheduler.run()


if __name__ == "__main__":
    main()


