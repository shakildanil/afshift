# Автоматизация сбора статистики AppsFlyer для Фонбет

Скрипт для автоматического сбора и обновления статистики депозитов (af_ftd events) из AppsFlyer в Google Sheets.

> 🚀 **[НАЧНИТЕ ЗДЕСЬ!](START_HERE.md)** - Быстрый старт и навигация по проекту

## 📚 Документация

> 💡 **Для краткого обзора читайте [SUMMARY.md](SUMMARY.md)**

- **[📋 SUMMARY.md](SUMMARY.md)** - Краткая сводка проекта
- **[🚀 QUICKSTART.md](QUICKSTART.md)** - Быстрый старт за 5 минут
- **[✅ CHECKLIST.md](CHECKLIST.md)** - Чеклист запуска
- **[📗 INSTALLATION.md](INSTALLATION.md)** - Детальная инструкция по установке
- **[🔄 HOW_IT_WORKS.md](HOW_IT_WORKS.md)** - Подробное объяснение работы
- **[📕 USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)** - Примеры использования
- **[📙 PROJECT_INFO.md](PROJECT_INFO.md)** - Техническая информация и архитектура
- **[📁 FILES_OVERVIEW.md](FILES_OVERVIEW.md)** - Обзор файлов проекта
- **[📝 TODO.md](TODO.md)** - Планы развития

## Возможности

- ✅ Автоматический сбор данных из AppsFlyer API для iOS и Android приложений
- ✅ Фильтрация событий по времени (event_time - install_time < 30 дней)
- ✅ Группировка по Media Source и Campaign с подсчетом депозитов
- ✅ Автоматическое обновление Google Sheets
- ✅ Планировщик для ежедневного запуска в 10:00
- ✅ Покрыто тестами
- ✅ Логирование всех операций

## Установка

### 1. Клонируйте репозиторий

```bash
git clone <url>
cd adc-afshit
```

### 2. Создайте виртуальное окружение

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Настройка конфигурации

#### 4.1. Создайте файл `.env`

Скопируйте `.env.example` в `.env` и заполните параметры:

```bash
cp .env.example .env
```

#### 4.2. Настройте переменные окружения

Отредактируйте файл `.env`:

```env
# AppsFlyer API Configuration
APPSFLYER_API_KEY=ваш_ключ_api

# AppsFlyer App IDs
FONBET_IOS_APP_ID=id_ios_приложения
FONBET_ANDROID_APP_ID=ru.bkfon-Android

# Google Sheets Configuration
GOOGLE_SPREADSHEET_ID=12NYiMx_ZqPOPhFf48_HfSSf5QeNFC9mmakuP8_Yh5MU
GOOGLE_SHEET_NAME=Sheet1

# Schedule Configuration (время запуска в формате HH:MM)
SCHEDULE_TIME=10:00

# Data Processing Configuration
MAX_DAYS_BETWEEN_INSTALL_AND_EVENT=30
```

#### 4.3. Настройка Google Sheets API

1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект или выберите существующий
3. Включите Google Sheets API:
   - Перейдите в "APIs & Services" > "Library"
   - Найдите "Google Sheets API"
   - Нажмите "Enable"
4. Создайте OAuth 2.0 credentials:
   - Перейдите в "APIs & Services" > "Credentials"
   - Нажмите "Create Credentials" > "OAuth client ID"
   - Выберите "Desktop app"
   - Скачайте JSON файл
   - Переименуйте его в `credentials.json` и поместите в корень проекта

## Использование

### Однократный запуск

Для однократного обновления статистики:

```bash
python -m src.main
```

С указанием конкретного месяца:

```bash
python -m src.main --year 2024 --month 10
```

### Автоматический запуск по расписанию

Для запуска планировщика, который будет обновлять статистику каждый день в указанное время:

```bash
python -m src.scheduler
```

Планировщик будет работать в фоновом режиме и обновлять данные каждый день в 10:00 (или в другое время, указанное в `SCHEDULE_TIME`).

### Настройка автозапуска

#### Windows (Task Scheduler)

1. Откройте Task Scheduler
2. Создайте новую задачу
3. Триггер: При запуске системы
4. Действие: Запуск программы
   - Программа: `C:\путь\к\venv\Scripts\python.exe`
   - Аргументы: `-m src.scheduler`
   - Рабочая папка: `C:\путь\к\проекту`

#### Linux (systemd)

Создайте файл `/etc/systemd/system/fonbet-stats.service`:

```ini
[Unit]
Description=Fonbet Statistics Updater
After=network.target

[Service]
Type=simple
User=ваш_пользователь
WorkingDirectory=/путь/к/проекту
Environment="PATH=/путь/к/venv/bin"
ExecStart=/путь/к/venv/bin/python -m src.scheduler
Restart=always

[Install]
WantedBy=multi-user.target
```

Затем:

```bash
sudo systemctl daemon-reload
sudo systemctl enable fonbet-stats
sudo systemctl start fonbet-stats
```

## Запуск тестов

Для запуска всех тестов:

```bash
pytest
```

С покрытием кода:

```bash
pytest --cov=src --cov-report=html
```

Для запуска конкретного теста:

```bash
pytest tests/test_data_processor.py
```

## Структура проекта

```
adc-afshit/
├── src/
│   ├── __init__.py
│   ├── config.py                 # Конфигурация приложения
│   ├── appsflyer_client.py       # Клиент для AppsFlyer API
│   ├── data_processor.py         # Обработка и фильтрация данных
│   ├── google_sheets_updater.py  # Обновление Google Sheets
│   ├── scheduler.py              # Планировщик задач
│   └── main.py                   # Основной скрипт
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Фикстуры для тестов
│   ├── test_config.py
│   ├── test_appsflyer_client.py
│   ├── test_data_processor.py
│   ├── test_google_sheets_updater.py
│   └── test_integration.py
├── requirements.txt              # Зависимости
├── .env.example                  # Пример конфигурации
├── .gitignore
└── README.md
```

## Логика работы

### 1. Получение данных из AppsFlyer

- Скрипт подключается к AppsFlyer Raw Data Export API
- Запрашивает in-app events для указанных приложений
- Фильтрует события по типу `af_ftd` (First Time Deposit)
- Получает данные за текущий месяц (с 1-го числа до вчерашнего дня)

### 2. Обработка данных

- Парсит CSV ответ от AppsFlyer
- Фильтрует события по правилу: `event_time - install_time < 30 дней`
- Группирует по Media Source и Campaign
- Подсчитывает количество депозитов (каждая строка = 1 депозит)

### 3. Обновление Google Sheets

- Форматирует данные в табличный вид
- Создает или обновляет лист в Google Sheets
- Записывает данные с метаданными (дата обновления, статистика)

## Особенности

### Фильтрация по времени

Депозиты засчитываются только если разница между временем события и временем установки приложения **меньше 30 дней**. Это позволяет учитывать только "свежие" депозиты от новых пользователей.

### Media Source и Campaign

Скрипт автоматически извлекает информацию о:
- **Media Source** (источник трафика): mintegral_int, unity_int, и т.д.
- **Campaign** (название кампании): зависит от настроек

Данные группируются по уникальным комбинациям Media Source + Campaign, что позволяет анализировать эффективность каждой кампании отдельно.

### Обработка нескольких приложений

Скрипт автоматически обрабатывает данные для всех указанных App IDs:
- iOS приложение (если указано `FONBET_IOS_APP_ID`)
- Android приложение (`FONBET_ANDROID_APP_ID`)

## Troubleshooting

### Ошибка аутентификации AppsFlyer

**Проблема**: `401 Unauthorized`

**Решение**:
- Проверьте правильность API ключа в `.env`
- Убедитесь, что ключ не истек
- Проверьте права доступа в AppsFlyer

### Ошибка доступа к Google Sheets

**Проблема**: `File not found: credentials.json`

**Решение**:
- Создайте OAuth 2.0 credentials в Google Cloud Console
- Скачайте JSON файл и сохраните как `credentials.json`
- При первом запуске откроется браузер для авторизации

**Проблема**: `Permission denied`

**Решение**:
- Убедитесь, что Google Sheets API включен в проекте
- Проверьте, что у вас есть права на редактирование таблицы

### Нет данных в отчете

**Проблема**: Пустой отчет или 0 событий

**Решение**:
- Проверьте правильность App ID
- Убедитесь, что события `af_ftd` настроены в AppsFlyer
- Проверьте временной диапазон (возможно, за указанный период нет событий)

### Тесты не проходят

**Проблема**: Ошибки при запуске тестов

**Решение**:
```bash
# Переустановите зависимости
pip install -r requirements.txt --force-reinstall

# Очистите кеш pytest
pytest --cache-clear

# Запустите тесты с подробным выводом
pytest -v
```

## Безопасность

⚠️ **Важно**:
- Никогда не коммитьте файлы `.env`, `credentials.json`, `token.json`
- Храните API ключи в безопасности
- Используйте `.gitignore` для исключения чувствительных файлов

## ⚠️ Важно: Настройка токена AppsFlyer

**Токен в проекте возвращает "Inactive token"** - это нормально, токены могут истекать.

### Что делать:

1. **Получите новый активный токен:**
   - Зайдите в AppsFlyer Dashboard
   - Settings → API Access → Pull API или Raw Data Export API
   - Создайте новый токен с правами на Export Data

2. **Обновите токен в проекте:**
   ```bash
   # В файле .env или через переменную окружения
   APPSFLYER_API_KEY=ваш_новый_токен
   ```

3. **Проверьте токен:**
   ```bash
   python test_token_check.py
   ```

📖 **Подробные инструкции:** см. [TOKEN_SETUP.md](TOKEN_SETUP.md)

## Поддержка

При возникновении проблем:
1. Проверьте токен: `python test_token_check.py`
2. Проверьте логи (все операции логируются)
3. Убедитесь, что все зависимости установлены
4. Проверьте конфигурацию в `.env`
5. См. [TOKEN_SETUP.md](TOKEN_SETUP.md) для настройки токена

## Лицензия

Proprietary - для внутреннего использования.

