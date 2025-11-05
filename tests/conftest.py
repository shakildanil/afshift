"""
Фикстуры для тестов
"""

import pytest
from datetime import datetime, timedelta


@pytest.fixture
def sample_event_valid():
    """Валидное событие (разница < 30 дней)"""
    now = datetime.now()
    install_time = now - timedelta(days=10)
    
    return {
        "Event Time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "Install Time": install_time.strftime("%Y-%m-%d %H:%M:%S"),
        "Media Source": "mintegral_int",
        "Campaign": "test_campaign_1",
        "Event Name": "af_ftd"
    }


@pytest.fixture
def sample_event_invalid():
    """Невалидное событие (разница > 30 дней)"""
    now = datetime.now()
    install_time = now - timedelta(days=35)
    
    return {
        "Event Time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "Install Time": install_time.strftime("%Y-%m-%d %H:%M:%S"),
        "Media Source": "unity_int",
        "Campaign": "test_campaign_2",
        "Event Name": "af_ftd"
    }


@pytest.fixture
def sample_events_list():
    """Список событий для тестирования"""
    now = datetime.now()
    
    events = []
    
    # 5 валидных событий
    for i in range(5):
        install_time = now - timedelta(days=i+1)
        events.append({
            "Event Time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "Install Time": install_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Media Source": f"source_{i % 2}",
            "Campaign": f"campaign_{i % 3}",
            "Event Name": "af_ftd"
        })
    
    # 3 невалидных события
    for i in range(3):
        install_time = now - timedelta(days=31+i)
        events.append({
            "Event Time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "Install Time": install_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Media Source": f"source_{i}",
            "Campaign": f"campaign_{i}",
            "Event Name": "af_ftd"
        })
    
    return events


@pytest.fixture
def sample_csv_response():
    """Пример CSV ответа от AppsFlyer"""
    csv_data = """Event Time,Install Time,Media Source,Campaign,Event Name
2024-01-15 10:00:00,2024-01-10 09:00:00,mintegral_int,winter_campaign,af_ftd
2024-01-15 11:00:00,2024-01-05 08:00:00,unity_int,winter_campaign,af_ftd
2024-01-15 12:00:00,2024-01-14 07:00:00,mintegral_int,spring_campaign,af_ftd
2024-01-15 13:00:00,2023-12-10 06:00:00,ironSource_int,old_campaign,af_ftd"""
    
    return csv_data


@pytest.fixture
def mock_appsflyer_api_key():
    """Mock API ключ для тестов"""
    return "test_api_key_12345"


@pytest.fixture
def mock_spreadsheet_id():
    """Mock ID таблицы Google Sheets"""
    return "test_spreadsheet_id_12345"


