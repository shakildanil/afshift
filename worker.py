"""
Worker для Heroku - запуск обновления статистики по расписанию
Каждый день в 8:00 МСК, кроме воскресенья
"""

import os
import sys
import time
import logging
import schedule
from datetime import datetime, timezone, timedelta

from src.fonbet_stats_updater import FonbetStatsUpdater

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Часовой пояс Москвы (UTC+3)
MOSCOW_OFFSET = timedelta(hours=3)


def get_moscow_time():
    """Получить текущее время в МСК"""
    utc_now = datetime.now(timezone.utc)
    moscow_now = utc_now + MOSCOW_OFFSET
    return moscow_now


def should_run_today():
    """
    Проверка, нужно ли запускать обновление сегодня
    Не запускаем по воскресеньям (weekday == 6)
    """
    moscow_now = get_moscow_time()
    is_sunday = moscow_now.weekday() == 6
    
    if is_sunday:
        logger.info("Сегодня воскресенье - пропускаем обновление")
        return False
    
    return True


def run_update():
    """Запуск обновления статистики"""
    moscow_now = get_moscow_time()
    logger.info("=" * 80)
    logger.info("ЗАПУСК ОБНОВЛЕНИЯ СТАТИСТИКИ ФОНБЕТ")
    logger.info(f"Время МСК: {moscow_now.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)
    
    # Проверяем, нужно ли запускать сегодня
    if not should_run_today():
        logger.info("Обновление пропущено")
        return
    
    try:
        # Создаем обновлятор
        updater = FonbetStatsUpdater()
        
        # Обновляем статистику за текущий месяц
        result = updater.update_monthly_stats(
            year=None,  # Текущий год
            month=None  # Текущий месяц
        )
        
        logger.info("=" * 80)
        logger.info("ОБНОВЛЕНИЕ ЗАВЕРШЕНО УСПЕШНО")
        logger.info(f"Лист: {result['sheet_name']}")
        logger.info(f"Источников: {result['sources_count']}")
        logger.info(f"Депозитов: {result['total_deposits']}")
        logger.info(f"Revenue: ${result['total_revenue']:.2f}")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"ОШИБКА ПРИ ОБНОВЛЕНИИ: {e}", exc_info=True)
        # Не падаем, чтобы scheduler продолжал работать


def scheduled_job():
    """Задача для планировщика"""
    try:
        run_update()
    except Exception as e:
        logger.error(f"Ошибка в scheduled_job: {e}", exc_info=True)


def main():
    """Главная функция worker'а"""
    logger.info("=" * 80)
    logger.info("ЗАПУСК HEROKU WORKER")
    logger.info("=" * 80)
    logger.info("Часовой пояс: Europe/Moscow (МСК)")
    logger.info("Расписание: Каждый день в 08:00 МСК (кроме воскресенья)")
    logger.info("=" * 80)
    
    # Проверяем конфигурацию
    from src.config import config
    if not config.validate():
        logger.error("Ошибка конфигурации! Проверьте переменные окружения:")
        logger.error("- APPSFLYER_API_KEY")
        logger.error("- GOOGLE_SPREADSHEET_ID")
        logger.error("- GOOGLE_CLIENT_EMAIL")
        logger.error("- GOOGLE_PRIVATE_KEY")
        sys.exit(1)
    
    logger.info("Конфигурация валидна")
    logger.info(f"Spreadsheet ID: {config.GOOGLE_SPREADSHEET_ID}")
    logger.info(f"Service Account: {config.GOOGLE_CLIENT_EMAIL}")
    
    # Настраиваем расписание
    # ВАЖНО: На Heroku используется UTC, поэтому 8:00 МСК = 05:00 UTC
    schedule.every().day.at("05:00").do(scheduled_job)
    
    logger.info("\n✅ Worker запущен и ожидает выполнения по расписанию...")
    logger.info("Для остановки нажмите Ctrl+C\n")
    
    # Опционально: запустить сразу при старте (раскомментируйте, если нужно)
    # logger.info("Выполняем первый запуск сразу...")
    # scheduled_job()
    
    # Бесконечный цикл проверки расписания
    while True:
        try:
            # Проверяем расписание
            schedule.run_pending()
            
            # Получаем текущее время в МСК для логирования
            moscow_now = get_moscow_time()
            
            # Логируем каждый час, что мы живы
            if moscow_now.minute == 0:
                logger.info(f"Worker работает. Текущее время МСК: {moscow_now.strftime('%Y-%m-%d %H:%M:%S')}")
            
            time.sleep(60)  # Проверяем каждую минуту
            
        except KeyboardInterrupt:
            logger.info("\n\n⏹️  Worker остановлен пользователем")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Ошибка в главном цикле: {e}", exc_info=True)
            time.sleep(60)  # Ждем минуту и продолжаем


if __name__ == "__main__":
    main()

