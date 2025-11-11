# 🚀 Автоматическое обновление статистики Фонбет на Heroku

Автоматическое обновление статистики AppsFlyer в Google Sheets каждое утро в 8:00 МСК (кроме воскресенья).

## 📋 Что делает приложение

- ✅ Получает данные из AppsFlyer API (события `af_ftd`)
- ✅ Обрабатывает данные по кампаниям и источникам
- ✅ Обновляет Google Sheets с актуальной статистикой
- ✅ Создает отдельные листы по месяцам (`AF_Stats_Ноябрь25`, `AF_Stats_Декабрь25`, и т.д.)
- ✅ Запускается автоматически каждый день в 8:00 МСК
- ✅ Не работает по воскресеньям

## 🎯 Структура проекта для Heroku

```
├── Procfile                    # Конфигурация Heroku worker
├── runtime.txt                 # Версия Python
├── requirements.txt            # Зависимости
├── worker.py                   # Главный worker для Heroku
├── src/
│   ├── appsflyer_client.py    # Клиент AppsFlyer API
│   ├── data_processor.py      # Обработка данных
│   ├── campaign_analyzer.py   # Анализ кампаний
│   ├── google_sheets_service.py # Работа с Google Sheets
│   ├── fonbet_stats_updater.py # Основная логика обновления
│   └── config.py              # Конфигурация
└── HEROKU_DEPLOY.md           # Полная инструкция
```

## ⚡ Быстрый старт

### 1. Клонируйте и подготовьте
```bash
git clone <your-repo>
cd adc-afshit
```

### 2. Создайте приложение на Heroku
```bash
heroku login
heroku create your-app-name
```

### 3. Настройте переменные окружения
```bash
heroku config:set APPSFLYER_API_KEY="ваш_токен"
heroku config:set GOOGLE_SPREADSHEET_ID="id_таблицы"
heroku config:set GOOGLE_CLIENT_EMAIL="service-account@project.iam.gserviceaccount.com"
heroku config:set GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----..."
```

### 4. Деплой
```bash
git push heroku master
heroku ps:scale worker=1
heroku logs --tail
```

## 📚 Документация

- **[HEROKU_QUICKSTART.md](./HEROKU_QUICKSTART.md)** - Быстрый старт за 5 минут
- **[HEROKU_DEPLOY.md](./HEROKU_DEPLOY.md)** - Подробная инструкция по деплою
- **[ENV_VARIABLES.md](./ENV_VARIABLES.md)** - Описание переменных окружения

## 🔑 Необходимые ключи

### AppsFlyer API Token
Получите в AppsFlyer Dashboard → Settings → API Access

### Google Service Account
1. Создайте в [Google Cloud Console](https://console.cloud.google.com)
2. Включите Google Sheets API
3. Скачайте JSON ключ
4. Добавьте Service Account email в вашу Google таблицу (права Editor)

## 📊 Формат данных в Google Sheets

Приложение создает листы с названиями по месяцам:

```
AF_Stats_Ноябрь25
├── Дата обновления: 2025-11-11 08:05:23
├── 
├── Media Source | Campaign | Platform | Deposits | Revenue | ...
├── advisiondqe_int | Campaign_Name | android | 5 | $500.00 | ...
└── ...
```

## ⏰ Расписание

- **Время**: 8:00 МСК (05:00 UTC)
- **Частота**: Каждый день
- **Исключения**: Воскресенье (не запускается)

## 🔍 Мониторинг

```bash
# Статус worker'а
heroku ps

# Логи в реальном времени
heroku logs --tail

# Проверка переменных
heroku config

# Ручной запуск (для теста)
heroku run python -c "from worker import run_update; run_update()"
```

## 💰 Стоимость

- **Hobby dyno**: ~$7/месяц (worker работает 24/7)
- **Eco dyno**: ~$5/месяц (новый тип от Heroku)
- **Free tier**: Есть бесплатные часы для новых аккаунтов

### Альтернатива: Heroku Scheduler

Чтобы не держать worker постоянно запущенным, можно использовать **Heroku Scheduler**:

```bash
heroku addons:create scheduler:standard
heroku addons:open scheduler
```

Добавьте задачу:
- **Command**: `python -c "from worker import run_update; run_update()"`
- **Frequency**: Daily
- **Time**: 05:00 UTC

## ❗ Важные замечания

1. **Без демо-листов**: Приложение работает только с реальными данными
2. **Один лист на месяц**: Создается/обновляется только лист текущего месяца
3. **Не трогает старые данные**: Листы за прошлые месяцы остаются неизменными
4. **Автоматический пропуск воскресенья**: Проверка встроена в код

## 🛠️ Локальная разработка

Для локального тестирования:

```bash
# Установите зависимости
pip install -r requirements.txt

# Создайте .env файл с переменными
cp ENV_VARIABLES.md .env
# Отредактируйте .env

# Запустите worker локально
python worker.py

# Или однократное обновление
python -c "from worker import run_update; run_update()"
```

## 🔧 Troubleshooting

### Worker не запускается
```bash
heroku ps
heroku logs --tail
```

### Ошибка аутентификации Google
- Проверьте `GOOGLE_PRIVATE_KEY` (должны быть переносы строк `\n`)
- Убедитесь что Service Account добавлен в Google Sheets

### Ошибка AppsFlyer API
- Проверьте `APPSFLYER_API_KEY`
- Проверьте лимиты запросов AppsFlyer

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи: `heroku logs --tail`
2. Проверьте переменные: `heroku config`
3. Проверьте статус: `heroku ps`
4. Смотрите подробную документацию в [HEROKU_DEPLOY.md](./HEROKU_DEPLOY.md)

## 📄 Лицензия

Внутренний проект для автоматизации обновления статистики Фонбет.

---

**Сделано с ❤️ для автоматизации рутинных задач**


