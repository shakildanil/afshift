"""
Интеграционные тесты
"""

import pytest
from datetime import datetime, timedelta
from src.appsflyer_client import AppsFlyerClient
from src.data_processor import DataProcessor
from src.google_sheets_updater import GoogleSheetsUpdater


def test_full_pipeline_mock():
    """Тест полного пайплайна с мок-данными"""
    
    # 1. Создаем мок-данные как будто от AppsFlyer
    now = datetime.now()
    mock_events = []
    
    for i in range(10):
        install_time = now - timedelta(days=i+1)
        mock_events.append({
            "Event Time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "Install Time": install_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Media Source": f"source_{i % 3}",
            "Campaign": f"campaign_{i % 4}",
            "Event Name": "af_ftd"
        })
    
    # Добавляем несколько невалидных событий
    for i in range(3):
        install_time = now - timedelta(days=31+i)
        mock_events.append({
            "Event Time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "Install Time": install_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Media Source": f"old_source_{i}",
            "Campaign": f"old_campaign_{i}",
            "Event Name": "af_ftd"
        })
    
    mock_apps_data = {
        "test_app_1": mock_events,
        "test_app_2": mock_events[:5]
    }
    
    # 2. Обрабатываем данные
    processor = DataProcessor()
    processed_data = processor.process_all_apps_data(mock_apps_data)
    
    # 3. Проверяем результаты обработки
    assert len(processed_data) == 2
    assert "test_app_1" in processed_data
    assert "test_app_2" in processed_data
    
    # Для test_app_1 должно быть 10 валидных событий
    assert processed_data["test_app_1"]["valid_events"] == 10
    assert processed_data["test_app_1"]["total_events"] == 13
    
    # Для test_app_2 должно быть 5 валидных событий
    assert processed_data["test_app_2"]["valid_events"] == 5
    
    # 4. Форматируем для Google Sheets
    updater = GoogleSheetsUpdater()
    formatted_data = updater.format_processed_data_for_sheet(processed_data)
    
    # Проверяем структуру данных
    assert isinstance(formatted_data, list)
    assert len(formatted_data) > 0
    
    # Проверяем наличие ключевых элементов
    data_str = str(formatted_data)
    assert "test_app_1" in data_str
    assert "test_app_2" in data_str


def test_data_processor_handles_empty_events():
    """Тест обработки пустого списка событий"""
    processor = DataProcessor()
    
    result = processor.process_app_data([], "empty_app")
    
    assert result["app_id"] == "empty_app"
    assert result["total_events"] == 0
    assert result["valid_events"] == 0
    assert len(result["deposits_by_campaign"]) == 0
    assert len(result["summary"]) == 0


def test_data_processor_handles_all_invalid_events():
    """Тест обработки событий, где все невалидны"""
    processor = DataProcessor()
    
    now = datetime.now()
    invalid_events = []
    
    for i in range(5):
        install_time = now - timedelta(days=40+i)
        invalid_events.append({
            "Event Time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "Install Time": install_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Media Source": "source",
            "Campaign": "campaign"
        })
    
    result = processor.process_app_data(invalid_events, "invalid_app")
    
    assert result["total_events"] == 5
    assert result["valid_events"] == 0
    assert len(result["deposits_by_campaign"]) == 0


def test_google_sheets_updater_formats_empty_data():
    """Тест форматирования пустых данных"""
    updater = GoogleSheetsUpdater()
    
    processed_data = {
        "empty_app": {
            "total_events": 0,
            "valid_events": 0,
            "summary": []
        }
    }
    
    formatted = updater.format_processed_data_for_sheet(processed_data)
    
    # Должен вернуть хотя бы заголовки
    assert isinstance(formatted, list)
    assert len(formatted) > 0


