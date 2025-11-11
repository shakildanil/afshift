# ✅ ВСЁ ГОТОВО ДЛЯ HEROKU!

## 🎉 Что сделано

### 1. Созданы все файлы для Heroku
- ✅ `Procfile` - запускает worker
- ✅ `runtime.txt` - Python 3.11.6
- ✅ `worker.py` - главный скрипт (запуск каждый день в 8:00 МСК, кроме ВС)
- ✅ `app.json` - настройки приложения

### 2. Убраны все демо/тестовые листы
- ✅ Удален `create_demo_sheet.py`
- ✅ Из кода убран тестовый режим
- ✅ Теперь работает **только с реальными данными текущего месяца**

### 3. Создана документация
- 📖 `HEROKU_QUICKSTART.md` - быстрый старт (5 минут)
- 📖 `HEROKU_DEPLOY.md` - подробная инструкция
- 📖 `HEROKU_CHECKLIST.md` - чеклист для проверки
- 📖 `ENV_VARIABLES.md` - описание переменных
- 📖 `README_HEROKU.md` - обзор проекта

## 🚀 Как запустить (кратко)

### 1. Создайте приложение
```bash
heroku login
heroku create fonbet-stats-updater
```

### 2. Установите переменные
```bash
heroku config:set APPSFLYER_API_KEY="ваш_токен"
heroku config:set GOOGLE_SPREADSHEET_ID="id_таблицы"
heroku config:set GOOGLE_CLIENT_EMAIL="service-account@project.iam.gserviceaccount.com"
heroku config:set GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----..."
```

### 3. Загрузите код
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
- 🕗 Каждый день в **8:00 МСК**
- 🚫 Кроме **воскресенья**
- 📊 Обновляет лист **текущего месяца** (`AF_Stats_Ноябрь25`, и т.д.)

## 📖 Документация

Начните с быстрого старта:
**→ [HEROKU_QUICKSTART.md](./HEROKU_QUICKSTART.md)**

Или используйте чеклист:
**→ [HEROKU_CHECKLIST.md](./HEROKU_CHECKLIST.md)**

Подробная инструкция:
**→ [HEROKU_DEPLOY.md](./HEROKU_DEPLOY.md)**

## 🔑 Что нужно

1. **AppsFlyer API Token** - из AppsFlyer Dashboard
2. **Google Service Account** - создать в Google Cloud Console
3. **Google Spreadsheet ID** - из URL таблицы
4. **Добавить Service Account в таблицу** (Share → Editor)

## 💰 Стоимость

~$5-7/месяц за Eco/Hobby dyno (worker работает 24/7)

Или используйте **Heroku Scheduler** (бесплатный addon) - см. инструкцию.

## 🎊 Успехов с деплоем!

Все готово - можно деплоить! 🚀


