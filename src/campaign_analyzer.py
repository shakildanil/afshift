"""
Анализатор кампаний - парсинг iOS/Android из названий и группировка
"""

import re
import logging
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CampaignAnalyzer:
    """Класс для анализа кампаний и группировки по источникам"""
    
    def __init__(self):
        """Инициализация анализатора"""
        pass
    
    def detect_platform(self, event: Dict[str, str]) -> Optional[str]:
        """
        Определение платформы из данных события
        
        Args:
            event: Событие из AppsFlyer
            
        Returns:
            'ios', 'android' или None
        """
        # Сначала проверяем поле Platform напрямую
        platform = event.get('Platform') or event.get('platform') or ''
        platform_lower = platform.lower()
        
        if 'ios' in platform_lower or platform_lower == 'ios':
            return 'ios'
        elif 'android' in platform_lower or platform_lower == 'android' or 'aos' in platform_lower:
            return 'android'
        
        # Если Platform не помог, проверяем App ID
        app_id = event.get('App ID') or event.get('app_id') or event.get('Bundle ID') or ''
        app_id_lower = app_id.lower()
        
        if 'ios' in app_id_lower or app_id_lower.startswith('id'):
            return 'ios'
        elif 'android' in app_id_lower or '.android' in app_id_lower:
            return 'android'
        
        # В последнюю очередь проверяем название кампании
        campaign_name = event.get('Campaign') or event.get('campaign') or ''
        if campaign_name:
            campaign_lower = campaign_name.lower()
            
            # Проверяем на iOS
            if any(keyword in campaign_lower for keyword in ['ios', '_ios', '-ios', 'ios_', 'ios-']):
                return 'ios'
            
            # Проверяем на Android (aos, android)
            if any(keyword in campaign_lower for keyword in ['aos', '_aos', '-aos', 'aos_', 'aos-', 'android', '_android']):
                return 'android'
        
        return None
    
    def extract_source_name(self, media_source: str) -> str:
        """
        Извлечение названия источника
        
        Args:
            media_source: Media Source из AppsFlyer
            
        Returns:
            Название источника (используем как есть, НЕ убираем суффиксы)
        """
        if not media_source:
            return "Unknown"
        
        # Используем Media Source как есть - суффиксы это часть названия источника
        # Например: mintegral_int, unity_int, bigoads_int - это правильные названия
        return media_source
    
    def group_by_source_and_platform(
        self, 
        events: List[Dict[str, str]]
    ) -> Dict[Tuple[str, Optional[str]], Dict]:
        """
        Группировка событий по источнику и платформе
        
        Args:
            events: Список событий из AppsFlyer
            
        Returns:
            Словарь {(source, platform): {deposits, revenue, ...}}
        """
        grouped = defaultdict(lambda: {
            'deposits': 0,
            'revenue': 0.0,
            'campaigns': set()
        })
        
        for event in events:
            media_source = event.get('Media Source') or event.get('media_source') or 'Unknown'
            campaign = event.get('Campaign') or event.get('campaign') or 'Unknown'
            
            # Используем Media Source как есть (не убираем суффиксы)
            source = self.extract_source_name(media_source)
            
            # Определяем платформу из данных события (Platform поле, App ID, Campaign)
            platform = self.detect_platform(event)
            
            # Ключ для группировки
            key = (source, platform)
            
            # Подсчитываем депозиты (каждая строка = 1 депозит)
            grouped[key]['deposits'] += 1
            
            # Собираем доход (если есть)
            try:
                revenue_str = event.get('Event Revenue') or event.get('event_revenue') or '0'
                revenue = float(revenue_str) if revenue_str else 0.0
                grouped[key]['revenue'] += revenue
            except (ValueError, TypeError):
                pass
            
            # Сохраняем уникальные кампании
            grouped[key]['campaigns'].add(campaign)
        
        # Конвертируем sets в списки для JSON-сериализации
        result = {}
        for key, data in grouped.items():
            result[key] = {
                'deposits': data['deposits'],
                'revenue': round(data['revenue'], 2),
                'campaigns': list(data['campaigns'])
            }
        
        return result
    
    def create_summary_table(
        self, 
        grouped_data: Dict[Tuple[str, Optional[str]], Dict],
        spend_data: Optional[Dict[Tuple[str, Optional[str]], float]] = None
    ) -> List[Dict]:
        """
        Создание сводной таблицы для записи в Google Sheets
        
        Args:
            grouped_data: Сгруппированные данные
            spend_data: Данные о расходах (опционально)
            
        Returns:
            Список словарей для записи в таблицу
        """
        summary = []
        
        # Разделяем по платформам для лучшей читаемости
        ios_items = []
        android_items = []
        all_items = []
        
        for (source, platform), data in grouped_data.items():
            if platform == 'ios':
                ios_items.append(((source, platform), data))
            elif platform == 'android':
                android_items.append(((source, platform), data))
            else:
                all_items.append(((source, platform), data))
        
        # Сортируем каждую группу
        ios_items.sort(key=lambda x: (-x[1]['deposits'], x[0][0]))
        android_items.sort(key=lambda x: (-x[1]['deposits'], x[0][0]))
        all_items.sort(key=lambda x: (-x[1]['deposits'], x[0][0]))
        
        # Объединяем: сначала iOS, потом Android, потом остальные
        sorted_items = ios_items + android_items + all_items
        
        for (source, platform), data in sorted_items:
            source_name = source
            # Форматируем название платформы для отображения
            if platform == 'ios':
                platform_name = 'iOS'
            elif platform == 'android':
                platform_name = 'Android'
            else:
                platform_name = ''  # Пустое для "all" - не показываем
            
            # Получаем spend (если есть)
            spend = spend_data.get((source, platform), 0.0) if spend_data else 0.0
            
            revenue = data['revenue']
            profit = revenue - spend
            roi = (profit / spend * 100) if spend > 0 else None
            
            summary.append({
                'Source': source_name,
                'Platform': platform_name,
                'Spend': spend,
                'Revenue': revenue,
                'Profit': profit,
                'ROI': roi,
                'Deposits': data['deposits'],
                'Campaigns': len(data['campaigns'])
            })
        
        return summary
    
    def format_for_sheets(
        self, 
        summary: List[Dict],
        include_total: bool = True
    ) -> List[List]:
        """
        Форматирование данных для записи в Google Sheets
        
        Args:
            summary: Сводная таблица
            include_total: Включать ли строку Total
            
        Returns:
            Список списков для записи в Google Sheets
        """
        # Заголовки
        headers = ['Source', 'Platform', 'Spend $', 'Revenue $', 'Profit $', 'ROI %', 'Deposits', 'Campaigns']
        rows = [headers]
        
        # Данные
        total_spend = 0.0
        total_revenue = 0.0
        total_profit = 0.0
        total_deposits = 0
        
        for item in summary:
            spend = item['Spend']
            revenue = item['Revenue']
            profit = item['Profit']
            roi = item['ROI']
            
            # Форматируем ROI
            roi_str = f"{roi:.2f}%" if roi is not None else "#DIV/0!"
            
            row = [
                item['Source'],
                item['Platform'],
                f"${spend:,.2f}".replace(',', ' '),
                f"${revenue:,.2f}".replace(',', ' '),
                f"${profit:,.2f}".replace(',', ' '),
                roi_str,
                item['Deposits'],
                item['Campaigns']
            ]
            rows.append(row)
            
            # Суммируем для Total
            total_spend += spend
            total_revenue += revenue
            total_profit += profit
            total_deposits += item['Deposits']
        
        # Добавляем строку Total
        if include_total:
            total_roi = (total_profit / total_spend * 100) if total_spend > 0 else None
            total_roi_str = f"{total_roi:.2f}%" if total_roi is not None else "#DIV/0!"
            
            rows.append([
                'Total',
                '',
                f"${total_spend:,.2f}".replace(',', ' '),
                f"${total_revenue:,.2f}".replace(',', ' '),
                f"${total_profit:,.2f}".replace(',', ' '),
                total_roi_str,
                total_deposits,
                ''
            ])
        
        return rows

