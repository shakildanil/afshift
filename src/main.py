"""
Основной модуль для обновления статистики Фонбет
"""

import logging
import sys
from datetime import datetime

from src.config import config
from src.appsflyer_client import AppsFlyerClient
from src.data_processor import DataProcessor
from src.google_sheets_updater import GoogleSheetsUpdater

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def update_fonbet_stats(year: int = None, month: int = None):
    """
    Основная функция для обновления статистики Фонбет
    
    Args:
        year: Год (если не указан, берется текущий)
        month: Месяц (если не указан, берется текущий)
    """
    logger.info("=" * 80)
    logger.info("НАЧАЛО ОБНОВЛЕНИЯ СТАТИСТИКИ ФОНБЕТ")
    logger.info("=" * 80)
    
    # Проверяем конфигурацию
    if not config.validate():
        logger.error("Ошибка конфигурации. Проверьте переменные окружения.")
        sys.exit(1)
    
    try:
        # Шаг 1: Получение данных из AppsFlyer
        logger.info("\n[1/3] Получение данных из AppsFlyer...")
        appsflyer_client = AppsFlyerClient()
        apps_data = appsflyer_client.get_reports_for_all_apps(year, month)
        
        total_events = sum(len(events) for events in apps_data.values())
        logger.info(f"Получено всего событий: {total_events}")
        
        # Шаг 2: Обработка данных
        logger.info("\n[2/3] Обработка данных...")
        data_processor = DataProcessor()
        processed_data = data_processor.process_all_apps_data(apps_data)
        
        # Выводим статистику
        for app_id, data in processed_data.items():
            logger.info(
                f"  {app_id}: "
                f"{data['total_events']} событий, "
                f"{data['valid_events']} валидных, "
                f"{len(data['deposits_by_campaign'])} уникальных кампаний"
            )
        
        # Шаг 3: Обновление Google Sheets
        logger.info("\n[3/3] Обновление Google Sheets...")
        sheets_updater = GoogleSheetsUpdater()
        
        # Генерируем название листа с текущей датой
        now = datetime.now()
        sheet_name = f"Фонбет_{now.year}_{now.month:02d}"
        
        sheets_updater.update_with_processed_data(processed_data, sheet_name)
        
        logger.info("\n" + "=" * 80)
        logger.info("ОБНОВЛЕНИЕ СТАТИСТИКИ ЗАВЕРШЕНО УСПЕШНО")
        logger.info("=" * 80)
        
        return processed_data
        
    except Exception as e:
        logger.error(f"\n!!! ОШИБКА ПРИ ОБНОВЛЕНИИ СТАТИСТИКИ: {e}", exc_info=True)
        raise


def main():
    """Точка входа для запуска скрипта"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Обновление статистики Фонбет из AppsFlyer'
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
    
    args = parser.parse_args()
    
    try:
        update_fonbet_stats(args.year, args.month)
    except Exception as e:
        logger.error(f"Ошибка выполнения: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


