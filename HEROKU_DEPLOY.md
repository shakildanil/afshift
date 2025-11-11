# 🚀 Инструкция по деплою на Heroku

Этот проект настроен для автоматического запуска на Heroku каждое утро в 8:00 МСК (кроме воскресенья).

## 📋 Предварительные требования

1. **Аккаунт на Heroku** - зарегистрируйтесь на [heroku.com](https://heroku.com)
2. **Heroku CLI** - установите с [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git** - убедитесь что git установлен

## 🔑 Подготовка данных

### 1. AppsFlyer API Token

Получите API токен в AppsFlyer:
- Зайдите в AppsFlyer Dashboard
- Settings → API Access
- Скопируйте ваш API Token (V2.0)

### 2. Google Service Account

Создайте Service Account для доступа к Google Sheets:

1. Перейдите в [Google Cloud Console](https://console.cloud.google.com)
2. Создайте новый проект или выберите существующий
3. Включите Google Sheets API
4. Создайте Service Account:
   - IAM & Admin → Service Accounts → Create Service Account
   - Задайте имя, например "heroku-fonbet-stats"
   - Создайте ключ (JSON)
5. Скачайте JSON файл с ключами
6. Откройте JSON файл и найдите:
   - `client_email` - это будет `GOOGLE_CLIENT_EMAIL`
   - `private_key` - это будет `GOOGLE_PRIVATE_KEY`

### 3. Google Spreadsheet ID

1. Откройте вашу таблицу в Google Sheets
2. Из URL скопируйте ID:
   ```
   https://docs.google.com/spreadsheets/d/[ЭТО_ID_ТАБЛИЦЫ]/edit
   ```
3. **ВАЖНО**: Дайте доступ Service Account к таблице:
   - Нажмите "Share" в таблице
   - Добавьте email вашего Service Account (из `client_email`)
   - Дайте права "Editor"

## 🚀 Деплой на Heroku

### Шаг 1: Создание приложения

```bash
# Войдите в Heroku
heroku login

# Создайте новое приложение
heroku create fonbet-stats-updater

# Или используйте свое имя
heroku create your-app-name
```

### Шаг 2: Настройка переменных окружения

```bash
# AppsFlyer API Token
heroku config:set APPSFLYER_API_KEY="your_appsflyer_api_token"

# Google Spreadsheet ID
heroku config:set GOOGLE_SPREADSHEET_ID="your_spreadsheet_id"

# Google Service Account Email
heroku config:set GOOGLE_CLIENT_EMAIL="your-service-account@project-id.iam.gserviceaccount.com"

# Google Private Key (важно сохранить переносы строк \n)
heroku config:set GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG...ваш_ключ_здесь...
-----END PRIVATE KEY-----"

# Или можно указать через файл:
heroku config:set GOOGLE_PRIVATE_KEY="$(cat service-account-key.json | jq -r .private_key)"
```

### Шаг 3: Деплой кода

```bash
# Убедитесь что вы в корне проекта
cd adc-afshit

# Добавьте Heroku remote (если еще не добавлен)
heroku git:remote -a your-app-name

# Коммит и пуш
git add .
git commit -m "Готов к деплою на Heroku"
git push heroku master
```

### Шаг 4: Запуск Worker

```bash
# Включите worker dyno (это платный план, но есть бесплатные часы)
heroku ps:scale worker=1

# Проверьте статус
heroku ps
```

### Шаг 5: Проверка логов

```bash
# Смотрите логи в реальном времени
heroku logs --tail

# Или только логи worker'а
heroku logs --tail --dyno worker
```

## 📅 Расписание работы

Worker настроен на запуск:
- ⏰ **Каждый день в 8:00 по МСК**
- 🚫 **Кроме воскресенья**
- 📊 **Обновляет лист текущего месяца** (например, `AF_Stats_Ноябрь25`)

## 🔍 Проверка работы

### Проверить переменные окружения:
```bash
heroku config
```

### Проверить логи:
```bash
heroku logs --tail
```

### Перезапустить worker:
```bash
heroku ps:restart worker
```

### Запустить обновление вручную (для теста):
```bash
heroku run python -c "from worker import run_update; run_update()"
```

## 💰 Стоимость

- **Hobby dyno ($7/месяц)** - если запущен 24/7
- **Eco dyno ($5/месяц)** - новый тип dyno от Heroku
- **Free dyno часы** - у новых аккаунтов есть бесплатные часы

> **Примечание**: Worker должен работать постоянно, чтобы следить за расписанием.
> Альтернатива - использовать Heroku Scheduler (см. ниже).

## 🔄 Альтернатива: Heroku Scheduler

Если хотите избежать постоянного запуска worker'а, можно использовать Heroku Scheduler:

1. **Установите Scheduler addon:**
   ```bash
   heroku addons:create scheduler:standard
   ```

2. **Откройте настройки:**
   ```bash
   heroku addons:open scheduler
   ```

3. **Добавьте задачу:**
   - Command: `python -c "from worker import run_update; run_update()"`
   - Frequency: Daily
   - Time: 05:00 UTC (это 8:00 МСК)

4. **Измените Procfile:**
   ```
   # Закомментируйте или удалите строку worker
   # worker: python worker.py
   ```

> **Примечание**: Heroku Scheduler не позволяет исключить воскресенье напрямую,
> но это можно сделать в коде (проверка уже есть в `should_run_today()`).

## 🛠️ Полезные команды

```bash
# Посмотреть статус приложения
heroku ps

# Остановить worker
heroku ps:scale worker=0

# Запустить worker
heroku ps:scale worker=1

# Перезапустить приложение
heroku restart

# Открыть dashboard
heroku dashboard

# Удалить приложение
heroku apps:destroy your-app-name
```

## 📝 Структура листов в Google Sheets

Программа автоматически создает/обновляет листы с названиями:
- `AF_Stats_Ноябрь25` - статистика за ноябрь 2025
- `AF_Stats_Декабрь25` - статистика за декабрь 2025
- И т.д. для каждого месяца

**Важно**: Программа НЕ трогает существующие листы за другие месяцы!

## ❗ Troubleshooting

### Ошибка "Authentication failed"
- Проверьте правильность `GOOGLE_PRIVATE_KEY` и `GOOGLE_CLIENT_EMAIL`
- Убедитесь что Service Account имеет доступ к таблице

### Ошибка "Spreadsheet not found"
- Проверьте `GOOGLE_SPREADSHEET_ID`
- Убедитесь что Service Account добавлен в список "Share" таблицы

### Worker не запускается
- Проверьте логи: `heroku logs --tail`
- Проверьте что dyno запущен: `heroku ps`
- Проверьте переменные окружения: `heroku config`

### Время запуска неправильное
- Worker использует часовой пояс Europe/Moscow (МСК)
- Проверьте что `tzdata` установлен в requirements.txt

## 📞 Поддержка

Если возникли проблемы:
1. Проверьте логи: `heroku logs --tail`
2. Проверьте документацию Heroku: [devcenter.heroku.com](https://devcenter.heroku.com)
3. Проверьте что все переменные окружения установлены правильно

## ✅ Checklist перед деплоем

- [ ] Получен AppsFlyer API Token
- [ ] Создан Google Service Account
- [ ] Service Account добавлен в Google Sheets с правами Editor
- [ ] Созданы все переменные окружения на Heroku
- [ ] Код загружен на Heroku (`git push heroku master`)
- [ ] Worker запущен (`heroku ps:scale worker=1`)
- [ ] Проверены логи (первый запуск должен произойти в 8:00 МСК)

---

🎉 **Готово!** Теперь ваша статистика будет обновляться автоматически каждое утро!


