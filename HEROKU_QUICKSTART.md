# ⚡ Быстрый старт для деплоя на Heroku

## 🚀 За 5 минут

### 1. Создайте приложение
```bash
heroku login
heroku create fonbet-stats-updater
```

### 2. Установите переменные окружения
```bash
# AppsFlyer API Token
heroku config:set APPSFLYER_API_KEY="ваш_токен_из_appsflyer"

# Google Spreadsheet ID (из URL таблицы)
heroku config:set GOOGLE_SPREADSHEET_ID="id_вашей_таблицы"

# Google Service Account
heroku config:set GOOGLE_CLIENT_EMAIL="ваш-service-account@проект.iam.gserviceaccount.com"
heroku config:set GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----
... ваш приватный ключ ...
-----END PRIVATE KEY-----"
```

### 3. Задеплойте код
```bash
git push heroku master
```

### 4. Запустите worker
```bash
heroku ps:scale worker=1
heroku logs --tail
```

## ✅ Готово!

Worker будет запускаться:
- 🕗 **Каждый день в 8:00 МСК**
- 🚫 **Кроме воскресенья**
- 📊 **Обновляет лист текущего месяца** (AF_Stats_Ноябрь25, AF_Stats_Декабрь25, и т.д.)

## 📖 Подробная инструкция

Смотрите [HEROKU_DEPLOY.md](./HEROKU_DEPLOY.md) для полной документации.

## 🔑 Где взять ключи?

### AppsFlyer API Token:
1. Зайдите в [AppsFlyer Dashboard](https://hq1.appsflyer.com)
2. Settings → API Access
3. Скопируйте API Token (V2.0)

### Google Service Account:
1. [Google Cloud Console](https://console.cloud.google.com)
2. Создайте Service Account
3. Скачайте JSON ключ
4. Добавьте Service Account email в Google Sheets (Share → Editor)

### Google Spreadsheet ID:
Из URL таблицы:
```
https://docs.google.com/spreadsheets/d/[ВОТ_ЭТОТ_ID]/edit
```

## 🔍 Проверка

```bash
# Статус
heroku ps

# Логи
heroku logs --tail

# Переменные
heroku config

# Тестовый запуск
heroku run python -c "from worker import run_update; run_update()"
```

## 💰 Стоимость

- **~$7/месяц** за Hobby dyno (worker работает 24/7)
- Первые 550 часов бесплатно для новых аккаунтов

## ❗ Важно

✅ **Никаких демо-листов!** Работает только с реальными данными  
✅ **Автоматическое создание листов** по месяцам (AF_Stats_Ноябрь25, и т.д.)  
✅ **Не трогает старые листы** - обновляет только текущий месяц  
✅ **Пропускает воскресенья** автоматически  

## 📞 Помощь

Проблемы? Проверьте:
1. `heroku logs --tail` - логи приложения
2. `heroku config` - переменные окружения
3. Права Service Account в Google Sheets (Editor)
4. Правильность GOOGLE_PRIVATE_KEY (с переносами строк)


