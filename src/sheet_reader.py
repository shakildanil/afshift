"""
Модуль для чтения и анализа существующих данных из Google Sheets
"""

import logging
from typing import Dict, List, Tuple, Optional
from src.google_sheets_service import GoogleSheetsService
from src.campaign_analyzer import CampaignAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SheetReader:
    """Класс для чтения и анализа данных из существующих листов"""
    
    def __init__(self):
        """Инициализация читателя"""
        self.sheets_service = GoogleSheetsService()
        self.analyzer = CampaignAnalyzer()
    
    def read_sheet_data(self, sheet_name: str) -> List[List]:
        """
        Чтение данных из листа
        
        Args:
            sheet_name: Название листа
            
        Returns:
            Список строк с данными
        """
        try:
            data = self.sheets_service.read_sheet(sheet_name)
            logger.info(f"Прочитано {len(data)} строк из листа '{sheet_name}'")
            return data
        except Exception as e:
            logger.warning(f"Не удалось прочитать лист '{sheet_name}': {e}")
            return []
    
    def parse_spend_data(self, sheet_data: List[List]) -> Dict[Tuple[str, Optional[str]], float]:
        """
        Парсинг данных о расходах из существующего листа
        
        Args:
            sheet_data: Данные из листа
            
        Returns:
            Словарь {(source, platform): spend}
        """
        spend_data = {}
        
        if not sheet_data or len(sheet_data) < 1:
            return spend_data
        
        # Ищем заголовки
        headers = sheet_data[0] if sheet_data else []
        
        # Проверяем, есть ли заголовки или это уже данные
        has_headers = False
        if headers:
            # Если первая ячейка пустая или содержит типичные названия заголовков
            first_cell = str(headers[0]).strip().lower() if headers else ''
            if not first_cell or any(keyword in first_cell for keyword in ['source', 'источник', 'name', 'название']):
                has_headers = True
        
        # Если заголовков нет, считаем что данные начинаются с первой строки
        data_start_idx = 1 if has_headers else 0
        if not has_headers:
            logger.info("Заголовки не найдены, парсим данные с первой строки")
        
        # Находим индексы нужных колонок
        source_idx = None
        platform_idx = None
        spend_idx = None
        
        for i, header in enumerate(headers):
            header_str = str(header).strip()
            header_lower = header_str.lower()
            
            # Ищем Source (может быть первая колонка или с названием)
            if source_idx is None:
                if 'source' in header_lower or 'источник' in header_lower:
                    source_idx = i
                elif i == 0:  # Первая колонка ВСЕГДА используется как источник
                    source_idx = i
            
            # Ищем Platform
            if platform_idx is None:
                if 'platform' in header_lower or 'платформа' in header_lower:
                    platform_idx = i
            
            # Ищем Spend (может быть "Spend $", "Spend", "Расход $", "ставка")
            if spend_idx is None:
                if 'spend' in header_lower or 'расход' in header_lower or 'ставка' in header_lower or 'budget' in header_lower or 'бюджет' in header_lower:
                    spend_idx = i
        
        # Если нет заголовков или source_idx не найден, используем колонку 0
        if source_idx is None:
            source_idx = 0
            logger.info("Используем первую колонку как Source")
        
        # Spend может отсутствовать - это нормально
        # Если не нашли по заголовку, пробуем третью колонку (индекс 2) - часто там ставка
        if spend_idx is None and len(headers) > 2:
            # Проверяем, есть ли в третьей колонке числа
            try:
                if len(sheet_data) > 1 and len(sheet_data[1]) > 2:
                    test_val = str(sheet_data[1][2]).strip().replace(',', '').replace(' ', '')
                    if test_val and test_val.replace('.', '').isdigit():
                        spend_idx = 2
                        logger.info("Используем колонку 3 (индекс 2) для ставок")
            except:
                pass
        
        if spend_idx is None:
            logger.info("Колонка Spend не найдена - будут использоваться нулевые значения")
            spend_idx = -1  # Флаг что Spend нет
        
        # Парсим данные
        for row in sheet_data[data_start_idx:]:
            if len(row) <= source_idx:
                continue
            
            source = str(row[source_idx]).strip()
            
            # Пропускаем пустые строки и Total
            if not source or source.lower() == 'total':
                continue
            
            # Получаем platform
            platform_str = None
            if platform_idx is not None and platform_idx < len(row):
                platform_str = str(row[platform_idx]).strip()
            
            # Преобразуем platform
            platform = None
            if platform_str:
                platform_lower = platform_str.lower()
                if 'ios' in platform_lower:
                    platform = 'ios'
                elif 'android' in platform_lower or 'aos' in platform_lower:
                    platform = 'android'
            
            # Парсим spend (если есть колонка)
            spend = 0.0
            if spend_idx >= 0 and spend_idx < len(row):
                spend_str = str(row[spend_idx]).strip()
                # Убираем $, ₽, пробелы, запятые, неразрывные пробелы
                spend_str = spend_str.replace('$', '').replace('₽', '').replace(' ', '').replace(',', '').replace('\xa0', '').replace('\u00a0', '').replace('р', '')
                
                try:
                    spend = float(spend_str) if spend_str else 0.0
                except (ValueError, TypeError):
                    spend = 0.0
            
            key = (source, platform)
            # Если уже есть данные, суммируем
            if key in spend_data:
                spend_data[key] += spend
            else:
                spend_data[key] = spend
        
        logger.info(f"Найдено {len(spend_data)} записей о расходах")
        return spend_data
    
    def get_all_sheets(self) -> List[str]:
        """
        Получение списка всех листов
        
        Returns:
            Список названий листов
        """
        try:
            sheets = self.sheets_service.get_all_sheets()
            return [sheet['title'] for sheet in sheets]
        except Exception as e:
            logger.error(f"Ошибка при получении списка листов: {e}")
            return []
    
    def find_spend_sheet(self) -> Optional[str]:
        """
        Поиск листа с данными о расходах
        
        Returns:
            Название листа или None
        """
        sheets = self.get_all_sheets()
        
        # Ищем листы, которые могут содержать данные о расходах
        spend_keywords = ['spend', 'расход', 'бюджет', 'budget']
        
        for sheet_name in sheets:
            sheet_lower = sheet_name.lower()
            if any(keyword in sheet_lower for keyword in spend_keywords):
                return sheet_name
        
        # Если не нашли, возвращаем первый лист (кроме системных)
        system_sheets = ['test', 'тест', 'sheet1', 'лист1']
        for sheet_name in sheets:
            if sheet_name.lower() not in system_sheets:
                return sheet_name
        
        return None
    
    def find_sheet_by_month(self, year: int, month: int) -> Optional[str]:
        """
        Поиск листа по году и месяцу
        
        Args:
            year: Год
            month: Месяц
            
        Returns:
            Название листа или None
        """
        sheets = self.get_all_sheets()
        
        # Названия месяцев
        month_names = [
            '', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ]
        
        year_short = str(year)[-2:]  # Последние 2 цифры года
        month_name = month_names[month]
        
        # Ищем лист с названием типа "Октябрь25"
        target_name = f"{month_name}{year_short}"
        
        for sheet_name in sheets:
            if sheet_name == target_name:
                logger.info(f"Найден лист со ставками: {sheet_name}")
                return sheet_name
        
        logger.info(f"Лист {target_name} не найден - ставки будут = 0")
        return None

