"""
Клиент для работы с AppsFlyer API
"""

import requests
import csv
import io
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

from src.config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AppsFlyerClient:
    """Клиент для работы с AppsFlyer Raw Data Export API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Инициализация клиента AppsFlyer
        
        Args:
            api_key: API ключ AppsFlyer (если не указан, берется из конфигурации)
        """
        self.api_key = api_key or config.APPSFLYER_API_KEY
        self.base_url = config.APPSFLYER_BASE_URL
        
    def get_in_app_events_report(
        self, 
        app_id: str, 
        from_date: datetime, 
        to_date: datetime,
        event_name: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Получение отчета по in-app событиям из AppsFlyer
        
        Args:
            app_id: ID приложения
            from_date: Дата начала периода
            to_date: Дата окончания периода
            event_name: Название события (af_ftd по умолчанию)
            
        Returns:
            Список словарей с данными событий
        """
        event_name = event_name or config.EVENT_NAME
        
        # Формируем URL для запроса
        url = f"{self.base_url}/{app_id}/in_app_events_report/v5"
        
        # Параметры запроса
        params = {
            "from": from_date.strftime("%Y-%m-%d"),
            "to": to_date.strftime("%Y-%m-%d"),
            "event_name": event_name,
            "timezone": "UTC"
        }
        
        # AppsFlyer требует Authorization header (не api_token в параметрах)
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        logger.info(f"Запрос данных для app_id={app_id}, период {from_date.date()} - {to_date.date()}, событие={event_name}")
        
        try:
            # Отправляем запрос
            response = requests.get(url, params=params, headers=headers, timeout=300)
            
            # Проверяем статус и даем понятные сообщения об ошибках
            if response.status_code == 401:
                error_msg = "Ошибка 401: Неверный API ключ или отсутствует заголовок Authorization"
                logger.error(error_msg)
                raise requests.exceptions.HTTPError(error_msg, response=response)
            elif response.status_code == 403:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                message = error_data.get('message', response.text[:200])
                if 'Inactive token' in message or 'inactive' in message.lower():
                    error_msg = (
                        f"Ошибка 403: Токен неактивен или истек. "
                        f"Проверьте токен в AppsFlyer Dashboard и убедитесь, что он активен. "
                        f"Также убедитесь, что используете правильный тип токена для Raw Data Export API."
                    )
                else:
                    error_msg = f"Ошибка 403: Доступ запрещен. {message}"
                logger.error(error_msg)
                raise requests.exceptions.HTTPError(error_msg, response=response)
            elif response.status_code == 404:
                error_msg = f"Ошибка 404: App ID '{app_id}' не найден. Проверьте правильность App ID."
                logger.error(error_msg)
                raise requests.exceptions.HTTPError(error_msg, response=response)
            
            response.raise_for_status()
            
            # Парсим CSV ответ
            csv_content = response.text
            # Убираем BOM (Byte Order Mark) если есть
            if csv_content.startswith('\ufeff'):
                csv_content = csv_content[1:]
            csv_reader = csv.DictReader(io.StringIO(csv_content))
            
            # Конвертируем в список словарей
            data = list(csv_reader)
            
            logger.info(f"Получено {len(data)} записей для {app_id}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе к AppsFlyer API: {e}")
            raise
        except csv.Error as e:
            logger.error(f"Ошибка при парсинге CSV: {e}")
            raise
    
    def get_aggregate_report(
        self,
        app_id: str,
        from_date: datetime,
        to_date: datetime
    ) -> List[Dict[str, str]]:
        """
        Получение агрегированного отчета (обходит лимит Raw Data)
        
        Args:
            app_id: ID приложения
            from_date: Дата начала
            to_date: Дата окончания
            
        Returns:
            Список событий из агрегированного отчета
        """
        # Aggregate API для получения данных по партнерам
        url = f"https://hq1.appsflyer.com/api/agg-data/export/app/{app_id}/partners_by_date_report/v5"
        
        params = {
            "from": from_date.strftime("%Y-%m-%d"),
            "to": to_date.strftime("%Y-%m-%d"),
            "timezone": "UTC"
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        logger.info(f"Запрос агрегированных данных для {app_id}, период {from_date.date()} - {to_date.date()}")
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=300)
            response.raise_for_status()
            
            csv_content = response.text
            if csv_content.startswith('\ufeff'):
                csv_content = csv_content[1:]
            csv_reader = csv.DictReader(io.StringIO(csv_content))
            data = list(csv_reader)
            
            logger.info(f"Получено {len(data)} записей из Aggregate API")
            return data
            
        except Exception as e:
            logger.error(f"Ошибка Aggregate API: {e}")
            raise
    
    def get_monthly_report(
        self, 
        app_id: str, 
        year: Optional[int] = None, 
        month: Optional[int] = None,
        use_aggregate: bool = False
    ) -> List[Dict[str, str]]:
        """
        Получение отчета за весь месяц (с 1-го числа до вчерашнего дня)
        
        Args:
            app_id: ID приложения
            year: Год (если не указан, берется текущий)
            month: Месяц (если не указан, берется текущий)
            use_aggregate: Использовать Aggregate API (обходит лимит)
            
        Returns:
            Список словарей с данными событий
        """
        now = datetime.now()
        year = year or now.year
        month = month or now.month
        
        # Начало месяца
        from_date = datetime(year, month, 1)
        
        # Вчерашний день
        to_date = now - timedelta(days=1)
        
        # Если вчерашний день не в текущем месяце, берем последний день месяца
        if to_date.month != month or to_date.year != year:
            # Находим последний день месяца
            if month == 12:
                to_date = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                to_date = datetime(year, month + 1, 1) - timedelta(days=1)
        
        # Пробуем Raw Data API, если не получилось - Aggregate
        if use_aggregate:
            return self.get_aggregate_report(app_id, from_date, to_date)
        
        try:
            return self.get_in_app_events_report(app_id, from_date, to_date)
        except requests.exceptions.HTTPError as e:
            if '400' in str(e) or 'maximum number' in str(e).lower():
                logger.warning("Лимит Raw Data достигнут, используем Aggregate API")
                return self.get_aggregate_report(app_id, from_date, to_date)
            raise
    
    def get_reports_for_all_apps(
        self, 
        year: Optional[int] = None, 
        month: Optional[int] = None,
        use_aggregate: bool = False
    ) -> Dict[str, List[Dict[str, str]]]:
        """
        Получение отчетов для всех приложений
        
        Args:
            year: Год
            month: Месяц
            use_aggregate: Использовать Aggregate API (обходит лимит)
            
        Returns:
            Словарь {app_id: [события]}
        """
        app_ids = config.get_app_ids()
        results = {}
        
        for app_id in app_ids:
            try:
                data = self.get_monthly_report(app_id, year, month, use_aggregate=use_aggregate)
                results[app_id] = data
            except Exception as e:
                logger.error(f"Ошибка при получении данных для {app_id}: {e}")
                results[app_id] = []
        
        return results


