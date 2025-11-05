"""
Тесты для модуля обработки данных
"""

import pytest
from datetime import datetime, timedelta
from src.data_processor import DataProcessor


def test_data_processor_initialization():
    """Тест инициализации процессора данных"""
    processor = DataProcessor()
    assert processor.max_days == 30
    
    processor_custom = DataProcessor(max_days=15)
    assert processor_custom.max_days == 15


def test_parse_datetime_standard_format():
    """Тест парсинга даты в стандартном формате"""
    processor = DataProcessor()
    
    date_str = "2024-01-15 10:30:45"
    result = processor.parse_datetime(date_str)
    
    assert isinstance(result, datetime)
    assert result.year == 2024
    assert result.month == 1
    assert result.day == 15
    assert result.hour == 10
    assert result.minute == 30
    assert result.second == 45


def test_parse_datetime_with_microseconds():
    """Тест парсинга даты с микросекундами"""
    processor = DataProcessor()
    
    date_str = "2024-01-15 10:30:45.123456"
    result = processor.parse_datetime(date_str)
    
    assert isinstance(result, datetime)
    assert result.microsecond == 123456


def test_parse_datetime_date_only():
    """Тест парсинга только даты"""
    processor = DataProcessor()
    
    date_str = "2024-01-15"
    result = processor.parse_datetime(date_str)
    
    assert isinstance(result, datetime)
    assert result.year == 2024
    assert result.month == 1
    assert result.day == 15


def test_parse_datetime_invalid_format():
    """Тест парсинга невалидной даты"""
    processor = DataProcessor()
    
    with pytest.raises(ValueError):
        processor.parse_datetime("invalid date")


def test_is_valid_event_within_30_days(sample_event_valid):
    """Тест валидности события в пределах 30 дней"""
    processor = DataProcessor()
    
    assert processor.is_valid_event(sample_event_valid) is True


def test_is_valid_event_beyond_30_days(sample_event_invalid):
    """Тест невалидности события за пределами 30 дней"""
    processor = DataProcessor()
    
    assert processor.is_valid_event(sample_event_invalid) is False


def test_is_valid_event_exactly_30_days():
    """Тест события ровно на границе 30 дней"""
    processor = DataProcessor()
    
    now = datetime.now()
    install_time = now - timedelta(days=30)
    
    event = {
        "Event Time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "Install Time": install_time.strftime("%Y-%m-%d %H:%M:%S"),
        "Media Source": "test",
        "Campaign": "test"
    }
    
    # На 30-й день должно быть невалидным (< 30, не <=)
    assert processor.is_valid_event(event) is False


def test_is_valid_event_missing_fields():
    """Тест события с отсутствующими полями"""
    processor = DataProcessor()
    
    event = {
        "Media Source": "test",
        "Campaign": "test"
    }
    
    assert processor.is_valid_event(event) is False


def test_filter_events(sample_events_list):
    """Тест фильтрации событий"""
    processor = DataProcessor()
    
    # В sample_events_list 5 валидных и 3 невалидных
    filtered = processor.filter_events(sample_events_list)
    
    assert len(filtered) == 5


def test_group_by_source_and_campaign(sample_events_list):
    """Тест группировки событий по источнику и кампании"""
    processor = DataProcessor()
    
    # Фильтруем только валидные события
    valid_events = processor.filter_events(sample_events_list)
    
    grouped = processor.group_by_source_and_campaign(valid_events)
    
    assert isinstance(grouped, dict)
    assert len(grouped) > 0
    
    # Проверяем структуру ключей
    for key, count in grouped.items():
        assert isinstance(key, tuple)
        assert len(key) == 2  # (media_source, campaign)
        assert isinstance(count, int)
        assert count > 0


def test_group_by_source_and_campaign_counts():
    """Тест подсчета депозитов при группировке"""
    processor = DataProcessor()
    
    now = datetime.now()
    install_time = now - timedelta(days=5)
    
    events = [
        {
            "Event Time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "Install Time": install_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Media Source": "source_1",
            "Campaign": "campaign_1"
        },
        {
            "Event Time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "Install Time": install_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Media Source": "source_1",
            "Campaign": "campaign_1"
        },
        {
            "Event Time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "Install Time": install_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Media Source": "source_2",
            "Campaign": "campaign_2"
        }
    ]
    
    grouped = processor.group_by_source_and_campaign(events)
    
    assert grouped[("source_1", "campaign_1")] == 2
    assert grouped[("source_2", "campaign_2")] == 1


def test_process_app_data(sample_events_list):
    """Тест полной обработки данных приложения"""
    processor = DataProcessor()
    
    result = processor.process_app_data(sample_events_list, "test_app_id")
    
    assert "app_id" in result
    assert result["app_id"] == "test_app_id"
    
    assert "total_events" in result
    assert result["total_events"] == len(sample_events_list)
    
    assert "valid_events" in result
    assert result["valid_events"] == 5  # Из sample_events_list
    
    assert "deposits_by_campaign" in result
    assert isinstance(result["deposits_by_campaign"], dict)
    
    assert "summary" in result
    assert isinstance(result["summary"], list)


def test_process_all_apps_data():
    """Тест обработки данных для всех приложений"""
    processor = DataProcessor()
    
    now = datetime.now()
    install_time = now - timedelta(days=5)
    
    events = [
        {
            "Event Time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "Install Time": install_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Media Source": "source_1",
            "Campaign": "campaign_1"
        }
    ]
    
    apps_data = {
        "app_1": events,
        "app_2": events
    }
    
    results = processor.process_all_apps_data(apps_data)
    
    assert len(results) == 2
    assert "app_1" in results
    assert "app_2" in results
    
    for app_id, data in results.items():
        assert data["app_id"] == app_id


def test_create_summary():
    """Тест создания сводной таблицы"""
    processor = DataProcessor()
    
    grouped_data = {
        ("source_1", "campaign_1"): 5,
        ("source_2", "campaign_2"): 3,
        ("source_1", "campaign_3"): 10
    }
    
    summary = processor._create_summary(grouped_data)
    
    assert isinstance(summary, list)
    assert len(summary) == 3
    
    # Проверяем структуру записей
    for item in summary:
        assert "Media Source" in item
        assert "Campaign" in item
        assert "Deposits (af_ftd)" in item
    
    # Проверяем сортировку (по убыванию количества депозитов)
    assert summary[0]["Deposits (af_ftd)"] == 10
    assert summary[1]["Deposits (af_ftd)"] == 5
    assert summary[2]["Deposits (af_ftd)"] == 3


