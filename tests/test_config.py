"""
Тесты для модуля конфигурации
"""

import pytest
import os
from src.config import Config


def test_config_has_required_fields():
    """Тест наличия обязательных полей конфигурации"""
    assert hasattr(Config, 'APPSFLYER_API_KEY')
    assert hasattr(Config, 'APPSFLYER_BASE_URL')
    assert hasattr(Config, 'FONBET_ANDROID_APP_ID')
    assert hasattr(Config, 'GOOGLE_SPREADSHEET_ID')
    assert hasattr(Config, 'MAX_DAYS_BETWEEN_INSTALL_AND_EVENT')
    assert hasattr(Config, 'EVENT_NAME')


def test_config_default_values():
    """Тест значений по умолчанию"""
    assert Config.EVENT_NAME == "af_ftd"
    assert Config.MAX_DAYS_BETWEEN_INSTALL_AND_EVENT == 30
    assert Config.SCHEDULE_TIME == "10:00"
    assert Config.FONBET_ANDROID_APP_ID == "ru.bkfon-Android"


def test_config_get_app_ids():
    """Тест получения списка App IDs"""
    app_ids = Config.get_app_ids()
    
    assert isinstance(app_ids, list)
    assert len(app_ids) >= 1
    assert Config.FONBET_ANDROID_APP_ID in app_ids


def test_config_validation_with_minimal_config():
    """Тест валидации с минимальной конфигурацией"""
    # Сохраняем оригинальные значения
    original_api_key = Config.APPSFLYER_API_KEY
    original_android_id = Config.FONBET_ANDROID_APP_ID
    original_spreadsheet_id = Config.GOOGLE_SPREADSHEET_ID
    
    try:
        # Устанавливаем тестовые значения
        Config.APPSFLYER_API_KEY = "test_key"
        Config.FONBET_ANDROID_APP_ID = "test_app"
        Config.GOOGLE_SPREADSHEET_ID = "test_sheet"
        
        assert Config.validate() is True
        
    finally:
        # Восстанавливаем оригинальные значения
        Config.APPSFLYER_API_KEY = original_api_key
        Config.FONBET_ANDROID_APP_ID = original_android_id
        Config.GOOGLE_SPREADSHEET_ID = original_spreadsheet_id


def test_config_appsflyer_base_url():
    """Тест корректности базового URL AppsFlyer"""
    assert Config.APPSFLYER_BASE_URL.startswith("https://")
    assert "appsflyer.com" in Config.APPSFLYER_BASE_URL


