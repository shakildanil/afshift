"""
Тесты для модуля обновления Google Sheets
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
import os

from src.google_sheets_updater import GoogleSheetsUpdater


def test_google_sheets_updater_initialization(mock_spreadsheet_id):
    """Тест инициализации обновлятора Google Sheets"""
    updater = GoogleSheetsUpdater(
        spreadsheet_id=mock_spreadsheet_id,
        credentials_file="test_creds.json",
        token_file="test_token.json"
    )
    
    assert updater.spreadsheet_id == mock_spreadsheet_id
    assert updater.credentials_file == "test_creds.json"
    assert updater.token_file == "test_token.json"
    assert updater.service is None


def test_format_processed_data_for_sheet():
    """Тест форматирования обработанных данных"""
    updater = GoogleSheetsUpdater()
    
    processed_data = {
        "app_1": {
            "total_events": 100,
            "valid_events": 80,
            "summary": [
                {
                    "Media Source": "source_1",
                    "Campaign": "campaign_1",
                    "Deposits (af_ftd)": 10
                },
                {
                    "Media Source": "source_2",
                    "Campaign": "campaign_2",
                    "Deposits (af_ftd)": 5
                }
            ]
        }
    }
    
    result = updater.format_processed_data_for_sheet(processed_data)
    
    assert isinstance(result, list)
    assert len(result) > 0
    
    # Проверяем наличие заголовков
    assert any("Дата обновления" in str(row) for row in result)
    assert any("Media Source" in str(row) for row in result)
    
    # Проверяем наличие данных
    assert any("source_1" in str(row) for row in result)
    assert any("campaign_1" in str(row) for row in result)


def test_format_processed_data_multiple_apps():
    """Тест форматирования данных для нескольких приложений"""
    updater = GoogleSheetsUpdater()
    
    processed_data = {
        "app_1": {
            "total_events": 50,
            "valid_events": 40,
            "summary": [
                {
                    "Media Source": "source_1",
                    "Campaign": "campaign_1",
                    "Deposits (af_ftd)": 5
                }
            ]
        },
        "app_2": {
            "total_events": 30,
            "valid_events": 25,
            "summary": [
                {
                    "Media Source": "source_2",
                    "Campaign": "campaign_2",
                    "Deposits (af_ftd)": 3
                }
            ]
        }
    }
    
    result = updater.format_processed_data_for_sheet(processed_data)
    
    assert isinstance(result, list)
    
    # Проверяем наличие данных для обоих приложений
    result_str = str(result)
    assert "app_1" in result_str
    assert "app_2" in result_str


@patch('src.google_sheets_updater.build')
@patch('src.google_sheets_updater.Credentials')
def test_authenticate_with_existing_token(mock_credentials, mock_build, tmp_path):
    """Тест аутентификации с существующим токеном"""
    updater = GoogleSheetsUpdater()
    
    # Создаем временный файл токена
    token_file = tmp_path / "test_token.json"
    token_file.write_text('{"token": "test_token", "refresh_token": "refresh", "token_uri": "uri", "client_id": "id", "client_secret": "secret"}')
    updater.token_file = str(token_file)
    
    # Мокаем credentials
    mock_creds = Mock()
    mock_creds.valid = True
    mock_credentials.from_authorized_user_file.return_value = mock_creds
    
    # Мокаем build
    mock_service = Mock()
    mock_build.return_value = mock_service
    
    updater.authenticate()
    
    assert updater.service == mock_service
    mock_build.assert_called_once()


def test_authenticate_missing_credentials_file():
    """Тест ошибки при отсутствии файла credentials"""
    updater = GoogleSheetsUpdater()
    updater.credentials_file = "non_existent_file.json"
    updater.token_file = "non_existent_token.json"
    
    with pytest.raises(FileNotFoundError):
        updater.authenticate()


@patch('src.google_sheets_updater.GoogleSheetsUpdater.authenticate')
def test_get_or_create_sheet_existing(mock_authenticate):
    """Тест получения существующего листа"""
    updater = GoogleSheetsUpdater()
    
    # Мокаем service
    mock_service = Mock()
    mock_spreadsheets = Mock()
    mock_get = Mock()
    
    mock_get.execute.return_value = {
        'sheets': [
            {'properties': {'title': 'Sheet1', 'sheetId': 1}},
            {'properties': {'title': 'Sheet2', 'sheetId': 2}}
        ]
    }
    
    mock_spreadsheets.get.return_value = mock_get
    mock_service.spreadsheets.return_value = mock_spreadsheets
    updater.service = mock_service
    
    sheet_id = updater.get_or_create_sheet('Sheet1')
    
    assert sheet_id == 1


@patch('src.google_sheets_updater.GoogleSheetsUpdater.authenticate')
def test_clear_sheet(mock_authenticate):
    """Тест очистки листа"""
    updater = GoogleSheetsUpdater()
    
    # Мокаем service
    mock_service = Mock()
    mock_spreadsheets = Mock()
    mock_values = Mock()
    mock_clear = Mock()
    
    mock_clear.execute.return_value = {}
    mock_values.clear.return_value = mock_clear
    mock_spreadsheets.values.return_value = mock_values
    mock_service.spreadsheets.return_value = mock_spreadsheets
    updater.service = mock_service
    
    # Не должно падать с ошибкой
    updater.clear_sheet('TestSheet')
    
    mock_values.clear.assert_called_once()


@patch('src.google_sheets_updater.GoogleSheetsUpdater.authenticate')
@patch('src.google_sheets_updater.GoogleSheetsUpdater.get_or_create_sheet')
@patch('src.google_sheets_updater.GoogleSheetsUpdater.clear_sheet')
def test_update_sheet(mock_clear, mock_get_sheet, mock_authenticate):
    """Тест обновления данных в листе"""
    updater = GoogleSheetsUpdater()
    
    # Мокаем service
    mock_service = Mock()
    mock_spreadsheets = Mock()
    mock_values = Mock()
    mock_update = Mock()
    
    mock_update.execute.return_value = {'updatedCells': 10}
    mock_values.update.return_value = mock_update
    mock_spreadsheets.values.return_value = mock_values
    mock_service.spreadsheets.return_value = mock_spreadsheets
    updater.service = mock_service
    
    test_data = [
        ["Header 1", "Header 2"],
        ["Value 1", "Value 2"]
    ]
    
    updater.update_sheet('TestSheet', test_data)
    
    mock_get_sheet.assert_called_once_with('TestSheet')
    mock_clear.assert_called_once_with('TestSheet')
    mock_values.update.assert_called_once()


