# Инструкция по установке

## Быстрый старт

### 1. Установка зависимостей

```bash
# Создайте виртуальное окружение
python -m venv venv

# Активируйте его
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

### 2. Настройка AppsFlyer API

1. У вас уже есть API ключ (предоставлен в задании)
2. Файл `.env` уже содержит этот ключ
3. Убедитесь, что указаны правильные App IDs в `.env`:
   - `FONBET_IOS_APP_ID` - для iOS приложения (если есть)
   - `FONBET_ANDROID_APP_ID` - для Android приложения (уже указан: ru.bkfon-Android)

### 3. Настройка Google Sheets API

#### Шаг 3.1: Создание проекта в Google Cloud

1. Перейдите на [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект:
   - Нажмите на выпадающий список проектов вверху
   - Выберите "New Project"
   - Введите название: "Fonbet Statistics"
   - Нажмите "Create"

#### Шаг 3.2: Включение Google Sheets API

1. В боковом меню выберите "APIs & Services" > "Library"
2. В поисковой строке введите "Google Sheets API"
3. Нажмите на "Google Sheets API"
4. Нажмите "Enable"

#### Шаг 3.3: Создание OAuth 2.0 credentials

1. Перейдите в "APIs & Services" > "Credentials"
2. Нажмите "Create Credentials" > "OAuth client ID"
3. Если появится предупреждение о consent screen:
   - Нажмите "Configure Consent Screen"
   - Выберите "External"
   - Заполните обязательные поля:
     - App name: "Fonbet Statistics"
     - User support email: ваш email
     - Developer contact: ваш email
   - Нажмите "Save and Continue"
   - В разделе "Scopes" нажмите "Add or Remove Scopes"
   - Найдите и добавьте "./auth/spreadsheets"
   - Нажмите "Save and Continue"
   - В Test users добавьте свой email
   - Нажмите "Save and Continue"
4. Вернитесь к созданию OAuth client ID:
   - Application type: "Desktop app"
   - Name: "Fonbet Desktop Client"
   - Нажмите "Create"
5. Скачайте JSON файл с credentials
6. Переименуйте файл в `credentials.json`
7. Поместите файл в корень проекта (рядом с `requirements.txt`)

#### Шаг 3.4: Проверка настройки

Запустите скрипт проверки:

```bash
python setup_google_credentials.py
```

Этот скрипт проверит наличие необходимых файлов и покажет инструкции, если что-то отсутствует.

### 4. Первый запуск

#### 4.1. Тестовый запуск

```bash
python run_once.py
```

При первом запуске:
1. Откроется браузер
2. Выберите ваш Google аккаунт
3. Предоставьте доступ к Google Sheets
4. После успешной авторизации файл `token.json` будет создан автоматически
5. Скрипт получит данные из AppsFlyer и обновит Google Sheets

#### 4.2. Проверка результатов

Откройте вашу Google таблицу:
https://docs.google.com/spreadsheets/d/12NYiMx_ZqPOPhFf48_HfSSf5QeNFC9mmakuP8_Yh5MU/

Должен появиться новый лист с текущим месяцем и данными.

### 5. Запуск планировщика

После успешного тестового запуска можно запустить планировщик:

```bash
python run_scheduler.py
```

Планировщик будет:
- Работать в фоновом режиме
- Обновлять статистику каждый день в 10:00
- Логировать все операции

Для остановки нажмите `Ctrl+C`.

## Настройка автозапуска

### Windows (Task Scheduler)

1. Откройте Task Scheduler (Планировщик заданий)
2. Нажмите "Create Basic Task"
3. Введите название: "Fonbet Statistics Updater"
4. Триггер: "When the computer starts"
5. Действие: "Start a program"
6. Настройки:
   ```
   Program/script: C:\путь\к\venv\Scripts\python.exe
   Add arguments: run_scheduler.py
   Start in: C:\Users\dk\Desktop\coding\adc-afshit
   ```
7. Установите галочку "Run whether user is logged on or not"
8. Сохраните задачу

### Linux (systemd)

Создайте файл `/etc/systemd/system/fonbet-stats.service`:

```ini
[Unit]
Description=Fonbet Statistics Updater
After=network.target

[Service]
Type=simple
User=ваш_пользователь
WorkingDirectory=/путь/к/adc-afshit
Environment="PATH=/путь/к/venv/bin"
ExecStart=/путь/к/venv/bin/python run_scheduler.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Активируйте сервис:

```bash
sudo systemctl daemon-reload
sudo systemctl enable fonbet-stats
sudo systemctl start fonbet-stats

# Проверка статуса
sudo systemctl status fonbet-stats

# Просмотр логов
journalctl -u fonbet-stats -f
```

## Тестирование

Запуск всех тестов:

```bash
pytest
```

С покрытием кода:

```bash
pytest --cov=src --cov-report=html
```

## Troubleshooting

### Ошибка "No module named 'src'"

Убедитесь, что вы находитесь в корневой директории проекта:
```bash
cd C:\Users\dk\Desktop\coding\adc-afshit
```

### Ошибка "credentials.json not found"

1. Проверьте, что файл `credentials.json` находится в корне проекта
2. Запустите `python setup_google_credentials.py` для проверки

### Ошибка "Invalid API token" от AppsFlyer

1. Проверьте правильность API ключа в файле `.env`
2. Убедитесь, что ключ не содержит лишних пробелов
3. Проверьте срок действия ключа в AppsFlyer

### Ошибка "Permission denied" для Google Sheets

1. Убедитесь, что у вас есть права на редактирование таблицы
2. Проверьте, что Google Sheets API включен в проекте
3. Попробуйте удалить `token.json` и авторизоваться заново

### Пустой отчет от AppsFlyer

1. Проверьте правильность App ID
2. Убедитесь, что события `af_ftd` настроены в AppsFlyer
3. Проверьте, что за указанный период есть события

## Полезные команды

```bash
# Обновление статистики за конкретный месяц
python -m src.main --year 2024 --month 10

# Просмотр версии пакетов
pip list

# Обновление зависимостей
pip install -r requirements.txt --upgrade

# Запуск конкретного теста
pytest tests/test_data_processor.py -v

# Проверка настроек Google Sheets
python setup_google_credentials.py
```

## Следующие шаги

После успешной установки:

1. ✅ Убедитесь, что тестовый запуск работает
2. ✅ Проверьте, что данные корректно обновляются в Google Sheets
3. ✅ Настройте автозапуск планировщика
4. ✅ Настройте мониторинг логов (опционально)

## Получение помощи

При возникновении проблем:
1. Проверьте логи в консоли
2. Запустите тесты для проверки работоспособности компонентов
3. Используйте `setup_google_credentials.py` для диагностики настроек


