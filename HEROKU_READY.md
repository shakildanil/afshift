# ✅ Проект готов к деплою на Heroku!

## 🎉 Что было сделано

### 1. Созданы файлы для Heroku

✅ **Procfile** - конфигурация для запуска worker'а  
✅ **runtime.txt** - указана версия Python (3.11.6)  
✅ **worker.py** - главный скрипт с расписанием 8:00 МСК (кроме воскресенья)  
✅ **app.json** - метаданные для деплоя одной кнопкой  

### 2. Обновлена конфигурация

✅ **requirements.txt** - зависимости актуальны  
✅ **src/config.py** - уже настроен для работы через переменные окружения  
✅ **src/google_sheets_service.py** - работает с Service Account через env vars  

### 3. Удалены демо/тестовые компоненты

✅ **create_demo_sheet.py** - удален  
✅ **src/fonbet_stats_updater.py** - убран параметр `test_mode`  
✅ Теперь работает только с реальными данными текущего месяца  

### 4. Создана документация

✅ **HEROKU_DEPLOY.md** - полная инструкция по деплою  
✅ **HEROKU_QUICKSTART.md** - быстрый старт за 5 минут  
✅ **HEROKU_CHECKLIST.md** - чеклист для проверки  
✅ **README_HEROKU.md** - обзор проекта для Heroku  
✅ **ENV_VARIABLES.md** - описание переменных окружения  

## 🚀 Как запустить

### Вариант 1: Быстрый старт (5 минут)

Следуйте инструкции: **[HEROKU_QUICKSTART.md](./HEROKU_QUICKSTART.md)**

```bash
heroku create your-app-name
heroku config:set APPSFLYER_API_KEY="..." GOOGLE_SPREADSHEET_ID="..." ...
git push heroku master
heroku ps:scale worker=1
```

### Вариант 2: Подробная инструкция

Следуйте инструкции: **[HEROKU_DEPLOY.md](./HEROKU_DEPLOY.md)**

Содержит:
- Подробное описание каждого шага
- Как получить все необходимые ключи
- Troubleshooting
- Альтернативные варианты (Heroku Scheduler)

### Вариант 3: Использовать чеклист

Следуйте инструкции: **[HEROKU_CHECKLIST.md](./HEROKU_CHECKLIST.md)**

Пошаговый чеклист с галочками ✅ для отметки выполненных пунктов.

## 📊 Как работает

### Расписание
- ⏰ **Запуск**: Каждый день в 8:00 МСК
- 🚫 **Исключение**: Воскресенье (не запускается)
- 📅 **Автоматически**: Worker работает 24/7 и следит за расписанием

### Обновление данных
1. Подключается к AppsFlyer API
2. Получает события `af_ftd` за текущий месяц
3. Обрабатывает и группирует данные
4. Обновляет Google Sheets

### Листы в Google Sheets
- Создает/обновляет только лист **текущего месяца**
- Формат названия: `AF_Stats_Ноябрь25`, `AF_Stats_Декабрь25`
- **НЕ трогает** листы за предыдущие месяцы
- **НЕ создает** демо/тестовые листы

## 🔑 Необходимые ключи

### 1. AppsFlyer API Token
- Получите в AppsFlyer Dashboard → Settings → API Access
- Сохраните в `APPSFLYER_API_KEY`

### 2. Google Service Account
- Создайте в Google Cloud Console
- Включите Google Sheets API
- Скачайте JSON ключ
- Используйте `client_email` и `private_key`

### 3. Google Spreadsheet ID
- Из URL таблицы: `https://docs.google.com/spreadsheets/d/[ID]/edit`
- **Важно**: Добавьте Service Account в таблицу (Share → Editor)

## 📁 Структура проекта для Heroku

```
adc-afshit/
├── Procfile                      # Worker для Heroku ✅
├── runtime.txt                   # Python 3.11.6 ✅
├── requirements.txt              # Зависимости ✅
├── worker.py                     # Главный скрипт ✅
├── app.json                      # Метаданные ✅
│
├── src/                          # Исходный код
│   ├── fonbet_stats_updater.py  # Основная логика (БЕЗ test_mode) ✅
│   ├── appsflyer_client.py      # Клиент AppsFlyer API
│   ├── google_sheets_service.py # Service Account auth ✅
│   ├── campaign_analyzer.py     # Анализ кампаний
│   ├── data_processor.py        # Обработка данных
│   └── config.py                # Конфигурация через env vars ✅
│
└── docs/                         # Документация Heroku
    ├── HEROKU_DEPLOY.md         # Полная инструкция ✅
    ├── HEROKU_QUICKSTART.md     # Быстрый старт ✅
    ├── HEROKU_CHECKLIST.md      # Чеклист ✅
    ├── README_HEROKU.md         # Обзор ✅
    └── ENV_VARIABLES.md         # Переменные окружения ✅
```

## ⚙️ Технические детали

### Часовой пояс
- Worker использует UTC на Heroku
- Автоматически конвертирует в МСК (UTC+3)
- Расписание: `05:00 UTC` = `08:00 МСК`

### Проверка дня недели
- Функция `should_run_today()` проверяет день недели в МСК
- Воскресенье (`weekday == 6`) пропускается автоматически

### Аутентификация Google
- Использует Service Account (не OAuth)
- Credentials передаются через переменные окружения
- Не требует интерактивной авторизации

### Обработка ошибок
- Worker продолжает работу даже при ошибках
- Все ошибки логируются в Heroku logs
- Не падает при проблемах с API

## 💰 Стоимость на Heroku

### Worker (24/7)
- **Eco dyno**: ~$5/месяц
- **Hobby dyno**: ~$7/месяц
- **Free tier**: Ограниченные бесплатные часы

### Альтернатива: Heroku Scheduler
- **Addon бесплатный**
- Не требует постоянно работающего worker'а
- См. инструкцию в [HEROKU_DEPLOY.md](./HEROKU_DEPLOY.md#-альтернатива-heroku-scheduler)

## 🔍 Мониторинг

### Логи
```bash
heroku logs --tail
```

### Статус
```bash
heroku ps
```

### Переменные
```bash
heroku config
```

### Тестовый запуск
```bash
heroku run python -c "from worker import run_update; run_update()"
```

## ❗ Важные замечания

### ✅ Что изменилось
- ❌ **Удалено**: `create_demo_sheet.py`
- ❌ **Убрано**: `test_mode` из `fonbet_stats_updater.py`
- ✅ **Добавлено**: `worker.py` для Heroku
- ✅ **Добавлено**: Полная документация для деплоя
- ✅ **Настроено**: Расписание 8:00 МСК (кроме ВС)

### ⚠️ Что нужно помнить
- Никаких демо/тестовых листов!
- Работаем только с текущим месяцем
- Service Account должен иметь доступ к таблице
- Worker работает 24/7 и стоит денег (или используйте Scheduler)

## 📞 Что делать дальше?

### 1. Прочитайте быстрый старт
**[HEROKU_QUICKSTART.md](./HEROKU_QUICKSTART.md)** - 5 минут

### 2. Соберите все ключи
- AppsFlyer API Token
- Google Service Account (email + private key)
- Google Spreadsheet ID

### 3. Задеплойте
Следуйте инструкции шаг за шагом

### 4. Проверьте
- Логи: `heroku logs --tail`
- Google Sheets: лист с текущим месяцем создан
- Ждите первого автоматического запуска в 8:00 МСК

## 🎊 Готово!

Проект полностью готов к деплою на Heroku.

**Все документы созданы, код обновлен, демо-листы удалены!**

Удачного деплоя! 🚀

---

**Дата подготовки**: 2025-11-11  
**Версия**: 1.0 - Ready for Heroku  
**Статус**: ✅ Production Ready


