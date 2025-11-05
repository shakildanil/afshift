"""
Обработчик данных из AppsFlyer
"""

from datetime import datetime
from typing import Dict, List, Tuple
import logging
from collections import defaultdict

from src.config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """Класс для обработки данных из AppsFlyer"""
    
    def __init__(self, max_days: int = None):
        """
        Инициализация процессора данных
        
        Args:
            max_days: Максимальное количество дней между установкой и событием
        """
        self.max_days = max_days or config.MAX_DAYS_BETWEEN_INSTALL_AND_EVENT
    
    def parse_datetime(self, datetime_str: str) -> datetime:
        """
        Парсинг строки даты/времени в объект datetime
        
        Args:
            datetime_str: Строка с датой/временем
            
        Returns:
            Объект datetime
        """
        # AppsFlyer использует формат "YYYY-MM-DD HH:MM:SS" или "YYYY-MM-DD HH:MM:SS.fff"
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(datetime_str.strip(), fmt)
            except ValueError:
                continue
        
        raise ValueError(f"Не удалось распарсить дату: {datetime_str}")
    
    def is_valid_event(self, event: Dict[str, str]) -> bool:
        """
        Проверка валидности события (event_time - install_time < max_days)
        
        Args:
            event: Словарь с данными события
            
        Returns:
            True если событие валидно, False иначе
        """
        try:
            # Поля могут иметь разные названия в зависимости от версии API
            event_time_str = event.get("Event Time") or event.get("event_time") or event.get("Event Time (UTC)")
            install_time_str = event.get("Install Time") or event.get("install_time") or event.get("Install Time (UTC)")
            
            if not event_time_str or not install_time_str:
                logger.warning(f"Отсутствуют поля времени в событии: {list(event.keys())}")
                return False
            
            event_time = self.parse_datetime(event_time_str)
            install_time = self.parse_datetime(install_time_str)
            
            days_diff = (event_time - install_time).days
            
            return days_diff < self.max_days
            
        except Exception as e:
            logger.error(f"Ошибка при проверке валидности события: {e}")
            return False
    
    def filter_events(self, events: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Фильтрация событий по времени
        
        Args:
            events: Список событий
            
        Returns:
            Отфильтрованный список событий
        """
        valid_events = [event for event in events if self.is_valid_event(event)]
        
        logger.info(f"Отфильтровано событий: {len(events)} -> {len(valid_events)}")
        
        return valid_events
    
    def group_by_source_and_campaign(
        self, 
        events: List[Dict[str, str]]
    ) -> Dict[Tuple[str, str], int]:
        """
        Группировка событий по Media Source и Campaign с подсчетом депозитов
        
        Args:
            events: Список событий
            
        Returns:
            Словарь {(media_source, campaign): количество_депозитов}
        """
        # Используем defaultdict для автоматического создания счетчиков
        grouped = defaultdict(int)
        
        for event in events:
            # Названия полей могут варьироваться
            media_source = (
                event.get("Media Source") or 
                event.get("media_source") or 
                event.get("Media Source (pid)") or
                "Unknown"
            )
            
            campaign = (
                event.get("Campaign") or 
                event.get("campaign") or 
                event.get("Campaign (c)") or
                "Unknown"
            )
            
            grouped[(media_source, campaign)] += 1
        
        return dict(grouped)
    
    def process_app_data(
        self, 
        events: List[Dict[str, str]],
        app_id: str
    ) -> Dict[str, any]:
        """
        Полная обработка данных для одного приложения
        
        Args:
            events: Список событий
            app_id: ID приложения
            
        Returns:
            Обработанные данные
        """
        logger.info(f"Обработка данных для {app_id}: {len(events)} событий")
        
        # Фильтруем события по времени
        valid_events = self.filter_events(events)
        
        # Группируем по источнику и кампании
        grouped_data = self.group_by_source_and_campaign(valid_events)
        
        # Формируем результат
        result = {
            "app_id": app_id,
            "total_events": len(events),
            "valid_events": len(valid_events),
            "deposits_by_campaign": grouped_data,
            "summary": self._create_summary(grouped_data)
        }
        
        return result
    
    def _create_summary(self, grouped_data: Dict[Tuple[str, str], int]) -> List[Dict[str, any]]:
        """
        Создание сводной таблицы для записи в Google Sheets
        
        Args:
            grouped_data: Сгруппированные данные
            
        Returns:
            Список строк для таблицы
        """
        summary = []
        
        for (media_source, campaign), count in sorted(
            grouped_data.items(), 
            key=lambda x: (-x[1], x[0][0], x[0][1])  # Сортировка по количеству, затем по имени
        ):
            summary.append({
                "Media Source": media_source,
                "Campaign": campaign,
                "Deposits (af_ftd)": count
            })
        
        return summary
    
    def process_all_apps_data(
        self, 
        apps_data: Dict[str, List[Dict[str, str]]]
    ) -> Dict[str, Dict[str, any]]:
        """
        Обработка данных для всех приложений
        
        Args:
            apps_data: Словарь {app_id: [события]}
            
        Returns:
            Обработанные данные для всех приложений
        """
        results = {}
        
        for app_id, events in apps_data.items():
            results[app_id] = self.process_app_data(events, app_id)
        
        return results


