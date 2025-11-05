"""
Тесты для клиента AppsFlyer
"""

import pytest
import responses
from datetime import datetime, timedelta
from src.appsflyer_client import AppsFlyerClient
from src.config import config


def test_appsflyer_client_initialization(mock_appsflyer_api_key):
    """Тест инициализации клиента"""
    client = AppsFlyerClient(api_key=mock_appsflyer_api_key)
    
    assert client.api_key == mock_appsflyer_api_key
    assert client.base_url == config.APPSFLYER_BASE_URL


def test_appsflyer_client_default_api_key():
    """Тест инициализации с ключом из конфига"""
    client = AppsFlyerClient()
    
    assert client.api_key == config.APPSFLYER_API_KEY


@responses.activate
def test_get_in_app_events_report_success(mock_appsflyer_api_key, sample_csv_response):
    """Тест успешного получения отчета"""
    client = AppsFlyerClient(api_key=mock_appsflyer_api_key)
    
    app_id = "test_app_id"
    from_date = datetime(2024, 1, 1)
    to_date = datetime(2024, 1, 31)
    
    # Мокаем HTTP ответ
    url_pattern = f"{config.APPSFLYER_BASE_URL}/{app_id}/in_app_events_report/v5"
    responses.add(
        responses.GET,
        url_pattern,
        body=sample_csv_response,
        status=200,
        content_type='text/csv'
    )
    
    result = client.get_in_app_events_report(app_id, from_date, to_date)
    
    assert isinstance(result, list)
    assert len(result) > 0
    
    # Проверяем структуру первой записи
    first_event = result[0]
    assert "Event Time" in first_event
    assert "Install Time" in first_event
    assert "Media Source" in first_event
    assert "Campaign" in first_event


@responses.activate
def test_get_in_app_events_report_custom_event(mock_appsflyer_api_key, sample_csv_response):
    """Тест получения отчета с кастомным событием"""
    client = AppsFlyerClient(api_key=mock_appsflyer_api_key)
    
    app_id = "test_app_id"
    from_date = datetime(2024, 1, 1)
    to_date = datetime(2024, 1, 31)
    custom_event = "custom_event_name"
    
    url_pattern = f"{config.APPSFLYER_BASE_URL}/{app_id}/in_app_events_report/v5"
    
    def request_callback(request):
        # Проверяем, что передан правильный параметр event_name
        assert f"event_name={custom_event}" in request.url
        return (200, {}, sample_csv_response)
    
    responses.add_callback(
        responses.GET,
        url_pattern,
        callback=request_callback,
        content_type='text/csv'
    )
    
    result = client.get_in_app_events_report(
        app_id, from_date, to_date, event_name=custom_event
    )
    
    assert isinstance(result, list)


@responses.activate
def test_get_in_app_events_report_api_error(mock_appsflyer_api_key):
    """Тест обработки ошибки API"""
    client = AppsFlyerClient(api_key=mock_appsflyer_api_key)
    
    app_id = "test_app_id"
    from_date = datetime(2024, 1, 1)
    to_date = datetime(2024, 1, 31)
    
    url_pattern = f"{config.APPSFLYER_BASE_URL}/{app_id}/in_app_events_report/v5"
    responses.add(
        responses.GET,
        url_pattern,
        json={"error": "Invalid API token"},
        status=401
    )
    
    with pytest.raises(Exception):
        client.get_in_app_events_report(app_id, from_date, to_date)


def test_get_monthly_report_current_month(mock_appsflyer_api_key):
    """Тест получения отчета за текущий месяц"""
    client = AppsFlyerClient(api_key=mock_appsflyer_api_key)
    
    # Мокаем метод get_in_app_events_report
    called_params = []
    
    def mock_get_report(app_id, from_date, to_date, event_name=None):
        called_params.append({
            "app_id": app_id,
            "from_date": from_date,
            "to_date": to_date
        })
        return []
    
    client.get_in_app_events_report = mock_get_report
    
    app_id = "test_app_id"
    result = client.get_monthly_report(app_id)
    
    assert len(called_params) == 1
    
    # Проверяем, что from_date - это первое число месяца
    assert called_params[0]["from_date"].day == 1
    
    # Проверяем, что to_date - это вчерашний день
    yesterday = datetime.now() - timedelta(days=1)
    assert called_params[0]["to_date"].date() == yesterday.date()


def test_get_monthly_report_specific_month(mock_appsflyer_api_key):
    """Тест получения отчета за конкретный месяц"""
    client = AppsFlyerClient(api_key=mock_appsflyer_api_key)
    
    called_params = []
    
    def mock_get_report(app_id, from_date, to_date, event_name=None):
        called_params.append({
            "app_id": app_id,
            "from_date": from_date,
            "to_date": to_date
        })
        return []
    
    client.get_in_app_events_report = mock_get_report
    
    app_id = "test_app_id"
    client.get_monthly_report(app_id, year=2024, month=5)
    
    assert len(called_params) == 1
    assert called_params[0]["from_date"] == datetime(2024, 5, 1)


def test_get_reports_for_all_apps(mock_appsflyer_api_key):
    """Тест получения отчетов для всех приложений"""
    client = AppsFlyerClient(api_key=mock_appsflyer_api_key)
    
    # Мокаем метод get_monthly_report
    def mock_get_monthly_report(app_id, year=None, month=None):
        return [{"app_id": app_id, "data": "test"}]
    
    client.get_monthly_report = mock_get_monthly_report
    
    results = client.get_reports_for_all_apps()
    
    assert isinstance(results, dict)
    
    # Проверяем, что получены данные для всех приложений
    app_ids = config.get_app_ids()
    for app_id in app_ids:
        assert app_id in results
        assert isinstance(results[app_id], list)


def test_get_reports_for_all_apps_handles_errors(mock_appsflyer_api_key):
    """Тест обработки ошибок при получении отчетов для всех приложений"""
    client = AppsFlyerClient(api_key=mock_appsflyer_api_key)
    
    # Мокаем метод get_monthly_report с ошибкой
    def mock_get_monthly_report_with_error(app_id, year=None, month=None):
        raise Exception("Test error")
    
    client.get_monthly_report = mock_get_monthly_report_with_error
    
    # Не должно падать с ошибкой
    results = client.get_reports_for_all_apps()
    
    assert isinstance(results, dict)
    
    # Для приложений с ошибками должны быть пустые списки
    for app_id, data in results.items():
        assert data == []


