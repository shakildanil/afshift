"""
Конфигурация приложения
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


class Config:
    """Класс конфигурации для приложения"""
    
    # AppsFlyer Configuration
    APPSFLYER_API_KEY: str = os.getenv(
        "APPSFLYER_API_KEY",
        "eyJhbGciOiJBMjU2S1ciLCJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwidHlwIjoiSldUIiwiemlwIjoiREVGIn0.Rx_EtUeaRa2TikH0PzjFx9644SJmaxtYu2Fdv0pOuRtJb_y5Z7n9Dw.nUFaGRl9LW3ChFDm.J-NBMA5lN3mArAIvpHmoR-_dgSMBUc8k3kmP3wRy5BC3vlx4wj8KCuFGajwUDMPUIJT8URiRKNBvcnw-TKtdnhnWvjT3novRhZWMLQZc6NVq4MJImDPTmptzix8zLwKNzjCm9gMJdVSKjEvdGHtG4F9MRBbMRfXMyenoSNd4B8K7lj0P7K3uBN-K22PVEc9S8bLZlypmxX78SiYiq64dh4eqoLa4kQ0xV_I1J8GwgSy9whascOyDzaV5LWt72X9Ax_i6vWQxu7eswAybQDtXNEuGsFCwnZtYjO0g-uQ90yLJOrmL2nVTNkyDlvlGeCCzd6uGb5nb_qSp6yK5TzU8GMrfVw.fRN7ZNEAHxuGeNeLgEPH7g"
    )
    
    APPSFLYER_BASE_URL: str = "https://hq1.appsflyer.com/api/raw-data/export/app"
    
    # App IDs
    FONBET_IOS_APP_ID: str = os.getenv("FONBET_IOS_APP_ID", "")
    FONBET_ANDROID_APP_ID: str = os.getenv("FONBET_ANDROID_APP_ID", "ru.bkfon-Android")
    
    # Google Sheets Configuration
    GOOGLE_SPREADSHEET_ID: str = os.getenv(
        "GOOGLE_SPREADSHEET_ID", 
        "12NYiMx_ZqPOPhFf48_HfSSf5QeNFC9mmakuP8_Yh5MU"
    )
    GOOGLE_SHEET_NAME: str = os.getenv("GOOGLE_SHEET_NAME", "Sheet1")
    GOOGLE_CREDENTIALS_FILE: str = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
    GOOGLE_TOKEN_FILE: str = os.getenv("GOOGLE_TOKEN_FILE", "token.json")
    
    # Schedule Configuration
    SCHEDULE_TIME: str = os.getenv("SCHEDULE_TIME", "10:00")
    
    # Data Processing Configuration
    MAX_DAYS_BETWEEN_INSTALL_AND_EVENT: int = int(
        os.getenv("MAX_DAYS_BETWEEN_INSTALL_AND_EVENT", "30")
    )
    
    # Event name to track
    EVENT_NAME: str = "af_ftd"
    
    @classmethod
    def validate(cls) -> bool:
        """Проверка наличия всех необходимых конфигурационных параметров"""
        required_fields = [
            cls.APPSFLYER_API_KEY,
            cls.FONBET_ANDROID_APP_ID,
            cls.GOOGLE_SPREADSHEET_ID,
        ]
        return all(required_fields)
    
    @classmethod
    def get_app_ids(cls) -> list[str]:
        """Возвращает список App IDs для обработки"""
        app_ids = [cls.FONBET_ANDROID_APP_ID]
        if cls.FONBET_IOS_APP_ID:
            app_ids.append(cls.FONBET_IOS_APP_ID)
        return app_ids


# Создаем глобальный экземпляр конфигурации
config = Config()


