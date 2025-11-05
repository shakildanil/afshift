"""
Основной модуль для обновления статистики Фонбет в Google Sheets
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from src.appsflyer_client import AppsFlyerClient
from src.data_processor import DataProcessor
from src.campaign_analyzer import CampaignAnalyzer
from src.google_sheets_service import GoogleSheetsService
from src.sheet_reader import SheetReader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FonbetStatsUpdater:
    """Класс для обновления статистики Фонбет"""
    
    def __init__(self):
        """Инициализация обновлятора"""
        self.appsflyer_client = AppsFlyerClient()
        self.data_processor = DataProcessor()
        self.campaign_analyzer = CampaignAnalyzer()
        self.sheets_service = GoogleSheetsService()
        self.sheet_reader = SheetReader()
    
    def get_monthly_data(
        self, 
        year: Optional[int] = None, 
        month: Optional[int] = None
    ) -> Dict[str, List[Dict[str, str]]]:
        """
        Получение данных за месяц из AppsFlyer
        
        Args:
            year: Год
            month: Месяц
            
        Returns:
            Словарь {app_id: [события]}
        """
        logger.info(f"Получение данных за {year or 'текущий'}-{month or 'текущий'}")
        return self.appsflyer_client.get_reports_for_all_apps(year, month)
    
    def process_events(
        self, 
        events: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        """
        Обработка событий с фильтрацией
        
        Args:
            events: Список событий
            
        Returns:
            Отфильтрованный список событий
        """
        return self.data_processor.filter_events(events)
    
    def analyze_campaigns(
        self, 
        events: List[Dict[str, str]]
    ) -> Dict[tuple, Dict]:
        """
        Анализ кампаний и группировка по источникам
        
        Args:
            events: Список событий
            
        Returns:
            Сгруппированные данные
        """
        return self.campaign_analyzer.group_by_source_and_platform(events)
    
    def get_sheet_name_for_month(
        self, 
        year: Optional[int] = None, 
        month: Optional[int] = None
    ) -> str:
        """
        Генерация названия листа для месяца
        
        Args:
            year: Год
            month: Месяц
            
        Returns:
            Название листа (например, "AF_Stats_Октябрь25")
        """
        if year is None or month is None:
            now = datetime.now()
            year = year or now.year
            month = month or now.month
        
        month_names = [
            '', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ]
        
        year_short = str(year)[-2:]  # Последние 2 цифры года
        month_name = month_names[month]
        
        # Создаем отдельный лист для AppsFlyer статистики
        return f"AF_Stats_{month_name}{year_short}"
    
    def load_spend_data(self, sheet_name: Optional[str] = None) -> Dict[Tuple[str, Optional[str]], float]:
        """
        Загрузка данных о расходах из существующего листа
        
        Args:
            sheet_name: Название листа (если None, пытается найти автоматически)
            
        Returns:
            Словарь {(source, platform): spend}
        """
        if sheet_name is None:
            sheet_name = self.sheet_reader.find_spend_sheet()
        
        if sheet_name is None:
            logger.warning("Не найден лист с данными о расходах")
            return {}
        
        logger.info(f"Загрузка данных о расходах из листа '{sheet_name}'")
        sheet_data = self.sheet_reader.read_sheet_data(sheet_name)
        return self.sheet_reader.parse_spend_data(sheet_data)
    
    def update_monthly_stats(
        self, 
        year: Optional[int] = None, 
        month: Optional[int] = None,
        spend_data: Optional[Dict[tuple, float]] = None,
        test_mode: bool = False,
        load_spend_from_sheet: bool = False  # По умолчанию НЕ трогаем существующие листы
    ):
        """
        Обновление статистики за месяц
        
        Args:
            year: Год
            month: Месяц
            spend_data: Данные о расходах (опционально)
            test_mode: Режим тестирования (создает лист "Тест")
        """
        # Получаем данные из AppsFlyer
        logger.info("=" * 80)
        logger.info("НАЧАЛО ОБНОВЛЕНИЯ СТАТИСТИКИ ФОНБЕТ")
        logger.info("=" * 80)
        
        apps_data = self.get_monthly_data(year, month)
        
        # Обрабатываем все события
        all_events = []
        for app_id, events in apps_data.items():
            logger.info(f"Обработка {app_id}: {len(events)} событий")
            valid_events = self.process_events(events)
            all_events.extend(valid_events)
            logger.info(f"  Валидных: {len(valid_events)}")
        
        logger.info(f"Всего валидных событий: {len(all_events)}")
        
        # Анализируем кампании
        grouped_data = self.analyze_campaigns(all_events)
        logger.info(f"Найдено уникальных источников: {len(grouped_data)}")
        
        # Загружаем данные о расходах, если не переданы и требуется
        # ВАЖНО: Только если явно указано, иначе не трогаем существующие листы
        if spend_data is None and load_spend_from_sheet:
            logger.info("Попытка загрузки данных о расходах из существующих листов...")
            try:
                spend_data = self.load_spend_data()
                if spend_data:
                    logger.info(f"Загружено {len(spend_data)} записей о расходах")
                else:
                    logger.info("Данные о расходах не найдены - будут использоваться нулевые значения")
            except Exception as e:
                logger.warning(f"Не удалось загрузить данные о расходах: {e}. Продолжаем без них.")
                spend_data = {}
        
        # Создаем сводную таблицу
        summary = self.campaign_analyzer.create_summary_table(
            grouped_data, 
            spend_data or {}
        )
        
        # Форматируем для Google Sheets
        rows = self.campaign_analyzer.format_for_sheets(summary)
        
        # Определяем название листа
        if test_mode:
            sheet_name = "AF_Stats_Тест"
        else:
            sheet_name = self.get_sheet_name_for_month(year, month)
        
        logger.info(f"Создание/обновление отдельного листа: {sheet_name}")
        logger.info("ВАЖНО: Существующие листы не изменяются!")
        
        # Записываем в Google Sheets (создаем новый лист, не трогаем существующие)
        self.sheets_service.write_sheet(
            sheet_name=sheet_name,
            data=rows,
            clear_first=True  # Очищаем только свой лист
        )
        
        logger.info("=" * 80)
        logger.info("ОБНОВЛЕНИЕ ЗАВЕРШЕНО УСПЕШНО")
        logger.info("=" * 80)
        
        return {
            'sheet_name': sheet_name,
            'sources_count': len(grouped_data),
            'total_deposits': sum(item['Deposits'] for item in summary),
            'total_revenue': sum(item['Revenue'] for item in summary)
        }

