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
        "1_CDw5CGuhSWXx-szzkRwO4ED6OQm2ED4ZX9ZSCN_S20"
    )
    GOOGLE_SHEET_NAME: str = os.getenv("GOOGLE_SHEET_NAME", "Sheet1")
    GOOGLE_CREDENTIALS_FILE: str = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
    GOOGLE_TOKEN_FILE: str = os.getenv("GOOGLE_TOKEN_FILE", "token.json")
    
    # Google Service Account Configuration
    GOOGLE_CLIENT_EMAIL: str = os.getenv(
        "GOOGLE_CLIENT_EMAIL",
        "financials@gen-lang-client-0873934698.iam.gserviceaccount.com"
    )
    GOOGLE_PRIVATE_KEY: str = os.getenv(
        "GOOGLE_PRIVATE_KEY",
        '-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDgqVWQhQhLB2JH\n7QwpSkUvmzM9jWudmw3dn8xrmftVwDxwckQYjqOUb5LsHAgYmmEOjAsdDWTDoeQs\nAYMAmyfuxxGZ0fzMsuofuGQVO1MumSFe9b50pOttkvesHPGXg6xog0oKpvmHXQ6X\nT6PeEmZFsPY5covoMHp1n3CDnhtBGt/QaxShqhsDcMfn3JbjRYDW5keP7w437sSq\nOIFiOyZdrG6MPsBEGM25SQNy7BgcReC2XtNPvfkNuWD6AeVfVvizcQwahIdG+tJy\nDtS0mUpPbFwNrlrFdiE9HXoz+ycgqmqcjckYj6LYb0baijnq659UxwWp6FDtJIt9\n0wZUiKCvAgMBAAECggEAR8aR6aw27BGd2rDnM8HgvMbu5flqql3BXk8Rdkcpv0m9\nhYdcLiRUKrZC0GBcTc/0tjsTyeJfkQkF5vFMs0LezTCYdPZbt+JpXl0AzK+5cafG\nu5nzkTynYsiTjE9q+Cc/S9y2KRUTn6WhZcIx7l8egaF56PypqjLizPV1cvduaavd\nG4EqU1bC6PZbTpgYOgle/8PBxda/aQEK76yeC6tyBzgWF1ht3PFzDdZwTVB7DMCD\nZx5utNq/7YSlV7KhZ3EpUU6Ihch18jkKYDM7QLTY16D3SzZWK76gfSHQ7Ktzq3HM\nga5ITmpodrvT4NJEIKX+w7Svykz++xPC/kfy6K1IUQKBgQDxhEqqjUYZ/rf5PF0a\nVbDgY6WhHcTGIDNK27Wm+yPH7s4NazImV9PiuFg7jtNtW1C6iWhLlJeLMtJFGonW\n5rzTLFQDLpSyD1YZvOi1gCTpzsiot6x6cIs9S6F5kiV9pgRGIBhyuxo1AI0e8WFa\nRmajVuV2NaGeTkepVbPm2382xQKBgQDuIkiw10TY/fUUvbLNvGOJYIMeltapOUCG\nr0o5GzHnfB7xs/tY1hk+pGQ/M2/vkwP3QSnPgn+yr/sA0tO3yKeirFt9gqduMBmN\nJDIJikivSON8zaL7LiZIxD4JmbxsFzqfZOA44/d8D6IOhT4J1m1Fn7G8ddsjGqj3\n8ackKP/Q4wKBgESFxjFxd6w0aroZ+Ehae56OZxW5PnT/+c2JXJaNtm8pP+jquwXJ\n8WHn75CmSzJBsDvcdGzNMdnah3H3v5frSzOW5hcpBiMm2sTeph+oxdBYTPIhepwa\nhkbTyHKXlm95xMionocesqbLCz72OSrFwqUhKGVLfhlOGGLg3/Pl3sgJAoGAXrDr\nTsaK7e4uIk08aGrc+aeS+/rm6OuHKQdS8FpMAcxtUZdL/wtDhpE/+5GslQtUrGER\nCx7NQHSRzsYGwjHb1ufKiaIGid4+is01yG1gcbL+IoZypIa5Wn4OXSrwrdqeyPsH\n3hdoNcDRpAx/mtHVKbZSqqoCtXbIca950vsqnhkCgYEAsqJx8vdmMr1hNZKo5vlD\nq4wOaVroCU9S8esLtzbiuXSDWmrOghtTFuaF475y2691QZa4Yj0EGr7fGc8Mx3AE\nrmL2k3Ci97XcsjO8svfStZWizLp5HekzmE1gGulglaDIY7DCDFLrxUSGEETehB4i\n1/DLthwAU6MWKZ5ooFOkGgs=\n-----END PRIVATE KEY-----\n'
    )
    
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


