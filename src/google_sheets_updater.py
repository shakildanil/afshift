"""
Модуль для обновления Google Sheets
"""

import os
import logging
from typing import List, Dict, Optional
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Scopes для работы с Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class GoogleSheetsUpdater:
    """Класс для обновления Google Sheets"""
    
    def __init__(
        self, 
        spreadsheet_id: Optional[str] = None,
        credentials_file: Optional[str] = None,
        token_file: Optional[str] = None
    ):
        """
        Инициализация обновлятора Google Sheets
        
        Args:
            spreadsheet_id: ID таблицы Google Sheets
            credentials_file: Путь к файлу с credentials
            token_file: Путь к файлу с токеном
        """
        self.spreadsheet_id = spreadsheet_id or config.GOOGLE_SPREADSHEET_ID
        self.credentials_file = credentials_file or config.GOOGLE_CREDENTIALS_FILE
        self.token_file = token_file or config.GOOGLE_TOKEN_FILE
        self.service = None
        
    def authenticate(self):
        """Аутентификация в Google API"""
        creds = None
        
        # Проверяем наличие сохраненного токена
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        
        # Если токена нет или он невалиден, запускаем OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Файл credentials не найден: {self.credentials_file}\n"
                        "Создайте OAuth 2.0 Client ID в Google Cloud Console и "
                        "скачайте JSON файл с credentials."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Сохраняем токен
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('sheets', 'v4', credentials=creds)
        logger.info("Успешная аутентификация в Google Sheets API")
    
    def get_or_create_sheet(self, sheet_name: str) -> int:
        """
        Получение или создание листа в таблице
        
        Args:
            sheet_name: Название листа
            
        Returns:
            ID листа
        """
        if not self.service:
            self.authenticate()
        
        try:
            # Получаем информацию о таблице
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            
            # Проверяем, существует ли лист
            for sheet in spreadsheet.get('sheets', []):
                if sheet['properties']['title'] == sheet_name:
                    logger.info(f"Лист '{sheet_name}' уже существует")
                    return sheet['properties']['sheetId']
            
            # Создаем новый лист
            request = {
                'addSheet': {
                    'properties': {
                        'title': sheet_name
                    }
                }
            }
            
            response = self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={'requests': [request]}
            ).execute()
            
            sheet_id = response['replies'][0]['addSheet']['properties']['sheetId']
            logger.info(f"Создан новый лист '{sheet_name}' с ID {sheet_id}")
            return sheet_id
            
        except HttpError as error:
            logger.error(f"Ошибка при работе с листом: {error}")
            raise
    
    def clear_sheet(self, sheet_name: str):
        """
        Очистка листа
        
        Args:
            sheet_name: Название листа
        """
        if not self.service:
            self.authenticate()
        
        try:
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!A:Z"
            ).execute()
            logger.info(f"Лист '{sheet_name}' очищен")
        except HttpError as error:
            logger.error(f"Ошибка при очистке листа: {error}")
            raise
    
    def update_sheet(
        self, 
        sheet_name: str, 
        data: List[List[any]], 
        clear_first: bool = True
    ):
        """
        Обновление данных в листе
        
        Args:
            sheet_name: Название листа
            data: Данные для записи (список списков)
            clear_first: Очищать ли лист перед записью
        """
        if not self.service:
            self.authenticate()
        
        # Создаем или получаем лист
        self.get_or_create_sheet(sheet_name)
        
        # Очищаем лист, если нужно
        if clear_first:
            self.clear_sheet(sheet_name)
        
        try:
            # Записываем данные
            body = {
                'values': data
            }
            
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!A1",
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            
            logger.info(
                f"Обновлено {result.get('updatedCells')} ячеек "
                f"в листе '{sheet_name}'"
            )
            
        except HttpError as error:
            logger.error(f"Ошибка при обновлении листа: {error}")
            raise
    
    def format_processed_data_for_sheet(
        self, 
        processed_data: Dict[str, Dict[str, any]]
    ) -> List[List[any]]:
        """
        Форматирование обработанных данных для записи в Google Sheets
        
        Args:
            processed_data: Обработанные данные из DataProcessor
            
        Returns:
            Список списков для записи в таблицу
        """
        # Заголовок
        rows = [
            ["Дата обновления", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            [],
            ["App ID", "Media Source", "Campaign", "Депозиты (af_ftd)"],
        ]
        
        # Данные по каждому приложению
        for app_id, data in processed_data.items():
            rows.append([])  # Пустая строка-разделитель
            rows.append([f"=== {app_id} ==="])
            rows.append([
                f"Всего событий: {data['total_events']}, "
                f"Валидных: {data['valid_events']}"
            ])
            rows.append([])
            
            # Данные по кампаниям
            for item in data['summary']:
                rows.append([
                    app_id,
                    item['Media Source'],
                    item['Campaign'],
                    item['Deposits (af_ftd)']
                ])
        
        return rows
    
    def update_with_processed_data(
        self, 
        processed_data: Dict[str, Dict[str, any]],
        sheet_name: Optional[str] = None
    ):
        """
        Обновление таблицы обработанными данными
        
        Args:
            processed_data: Обработанные данные
            sheet_name: Название листа (если не указано, используется из конфига)
        """
        sheet_name = sheet_name or config.GOOGLE_SHEET_NAME
        
        # Форматируем данные
        rows = self.format_processed_data_for_sheet(processed_data)
        
        # Обновляем таблицу
        self.update_sheet(sheet_name, rows, clear_first=True)
        
        logger.info(f"Данные успешно обновлены в таблице '{sheet_name}'")


