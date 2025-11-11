# 🔐 Переменные окружения

Для работы приложения необходимо настроить следующие переменные окружения:

## 📝 Список переменных

### AppsFlyer API Configuration

```bash
# AppsFlyer API Token (обязательно)
APPSFLYER_API_KEY=your_appsflyer_api_token_here

# AppsFlyer App IDs (опционально, по умолчанию используются ID Фонбета)
FONBET_ANDROID_APP_ID=ru.bkfon-Android
FONBET_IOS_APP_ID=id1166619854
```

### Google Sheets Configuration

```bash
# ID Google таблицы (обязательно)
GOOGLE_SPREADSHEET_ID=your_spreadsheet_id_here

# Google Service Account Email (обязательно)
GOOGLE_CLIENT_EMAIL=your-service-account@project-id.iam.gserviceaccount.com

# Google Service Account Private Key (обязательно)
# ВАЖНО: Сохраните переносы строк как \n
GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYour_Private_Key_Here\n-----END PRIVATE KEY-----\n"
```

### Schedule Configuration

```bash
# Время запуска (для локальных тестов, на Heroku жестко задано 8:00 МСК)
SCHEDULE_TIME=08:00
```

### Data Processing Configuration

```bash
# Максимальное количество дней между установкой и событием
MAX_DAYS_BETWEEN_INSTALL_AND_EVENT=30
```

## 🔧 Настройка на Heroku

### Через Heroku CLI:

```bash
# AppsFlyer
heroku config:set APPSFLYER_API_KEY="ваш_токен"

# Google Sheets
heroku config:set GOOGLE_SPREADSHEET_ID="ваш_id_таблицы"
heroku config:set GOOGLE_CLIENT_EMAIL="ваш-email@проект.iam.gserviceaccount.com"
heroku config:set GOOGLE_PRIVATE_KEY="$(cat service-account.json | jq -r .private_key)"
```

### Через Web Dashboard:

1. Откройте ваше приложение на [dashboard.heroku.com](https://dashboard.heroku.com)
2. Перейдите в **Settings** → **Config Vars**
3. Нажмите **Reveal Config Vars**
4. Добавьте каждую переменную:
   - **KEY**: Имя переменной
   - **VALUE**: Значение переменной

## 📋 Локальная разработка

Создайте файл `.env` в корне проекта:

```bash
# .env
APPSFLYER_API_KEY=your_token_here
GOOGLE_SPREADSHEET_ID=your_id_here
GOOGLE_CLIENT_EMAIL=your-email@project.iam.gserviceaccount.com
GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
```

> **Внимание**: Файл `.env` добавлен в `.gitignore` и НЕ должен попадать в git!

## ✅ Проверка настройки

Для проверки переменных на Heroku:

```bash
# Показать все переменные
heroku config

# Показать конкретную переменную
heroku config:get APPSFLYER_API_KEY

# Удалить переменную (если нужно)
heroku config:unset VARIABLE_NAME
```

## 🔐 Безопасность

1. **Никогда** не коммитьте файлы с реальными токенами в git
2. Используйте `.env` только для локальной разработки
3. На Heroku используйте Config Vars
4. Регулярно обновляйте токены и ключи
5. Ограничьте права Service Account только необходимыми (Google Sheets Editor)


