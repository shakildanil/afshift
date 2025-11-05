"""
Модуль для работы с Google Sheets через Service Account
"""

import os
import json
import logging
from typing import List, Dict, Optional, Tuple
from datetime import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Scopes для работы с Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class GoogleSheetsService:
    """Класс для работы с Google Sheets через Service Account"""
    
    def __init__(
        self, 
        spreadsheet_id: Optional[str] = None,
        client_email: Optional[str] = None,
        private_key: Optional[str] = None
    ):
        """
        Инициализация клиента Google Sheets
        
        Args:
            spreadsheet_id: ID таблицы Google Sheets
            client_email: Email сервисного аккаунта
            private_key: Приватный ключ сервисного аккаунта
        """
        self.spreadsheet_id = spreadsheet_id or config.GOOGLE_SPREADSHEET_ID
        self.client_email = client_email or config.GOOGLE_CLIENT_EMAIL
        self.private_key = private_key or config.GOOGLE_PRIVATE_KEY
        self.service = None
        
        if not self.private_key:
            raise ValueError("GOOGLE_PRIVATE_KEY не указан в конфигурации")
        
    def authenticate(self):
        """Аутентификация через Service Account"""
        try:
            # Создаем credentials из приватного ключа
            credentials_dict = {
                "type": "service_account",
                "project_id": "gen-lang-client-0873934698",
                "private_key_id": "",
                "private_key": self.private_key,
                "client_email": self.client_email,
                "client_id": "",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{self.client_email}"
            }
            
            credentials = service_account.Credentials.from_service_account_info(
                credentials_dict,
                scopes=SCOPES
            )
            
            self.service = build('sheets', 'v4', credentials=credentials)
            logger.info("Успешная аутентификация через Service Account")
            
        except Exception as e:
            logger.error(f"Ошибка аутентификации: {e}")
            raise
    
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
    
    def read_sheet(self, sheet_name: str, range_name: str = None) -> List[List]:
        """
        Чтение данных из листа
        
        Args:
            sheet_name: Название листа
            range_name: Диапазон (например, "A1:Z100"), если None - весь лист
            
        Returns:
            Список строк с данными
        """
        if not self.service:
            self.authenticate()
        
        try:
            range_full = f"{sheet_name}!{range_name}" if range_name else sheet_name
            
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_full
            ).execute()
            
            return result.get('values', [])
            
        except HttpError as error:
            logger.error(f"Ошибка при чтении листа: {error}")
            raise
    
    def write_sheet(
        self, 
        sheet_name: str, 
        data: List[List], 
        range_name: str = "A1",
        clear_first: bool = False
    ):
        """
        Запись данных в лист
        
        Args:
            sheet_name: Название листа
            data: Данные для записи (список списков)
            range_name: Начальная ячейка (по умолчанию A1)
            clear_first: Очищать ли лист перед записью
        """
        if not self.service:
            self.authenticate()
        
        # Создаем или получаем лист
        self.get_or_create_sheet(sheet_name)
        
        try:
            # Очищаем лист, если нужно
            if clear_first:
                self.service.spreadsheets().values().clear(
                    spreadsheetId=self.spreadsheet_id,
                    range=sheet_name
                ).execute()
            
            # Записываем данные
            body = {
                'values': data
            }
            
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!{range_name}",
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            
            logger.info(
                f"Обновлено {result.get('updatedCells')} ячеек "
                f"в листе '{sheet_name}'"
            )
            
        except HttpError as error:
            logger.error(f"Ошибка при записи в лист: {error}")
            raise
    
    def append_to_sheet(self, sheet_name: str, data: List[List]):
        """
        Добавление данных в конец листа
        
        Args:
            sheet_name: Название листа
            data: Данные для добавления
        """
        if not self.service:
            self.authenticate()
        
        try:
            body = {
                'values': data
            }
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=sheet_name,
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            
            logger.info(f"Добавлено {len(data)} строк в лист '{sheet_name}'")
            
        except HttpError as error:
            logger.error(f"Ошибка при добавлении данных: {error}")
            raise
    
    def get_all_sheets(self) -> List[Dict]:
        """
        Получение списка всех листов в таблице
        
        Returns:
            Список словарей с информацией о листах
        """
        if not self.service:
            self.authenticate()
        
        try:
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            
            sheets = []
            for sheet in spreadsheet.get('sheets', []):
                sheets.append({
                    'id': sheet['properties']['sheetId'],
                    'title': sheet['properties']['title']
                })
            
            return sheets
            
        except HttpError as error:
            logger.error(f"Ошибка при получении списка листов: {error}")
            raise

