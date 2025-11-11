# ✅ Чеклист деплоя на Heroku

Используйте этот чеклист для проверки перед деплоем.

## 📋 Подготовка (выполните локально)

### 1. Получение ключей и доступов

- [ ] **AppsFlyer API Token получен**
  - Зайдите в [AppsFlyer Dashboard](https://hq1.appsflyer.com)
  - Settings → API Access
  - Скопируйте API Token (V2.0)

- [ ] **Google Service Account создан**
  - Создан в [Google Cloud Console](https://console.cloud.google.com)
  - Google Sheets API включен
  - JSON ключ скачан
  - Скопированы `client_email` и `private_key`

- [ ] **Google Spreadsheet ID получен**
  - Скопирован из URL таблицы: `https://docs.google.com/spreadsheets/d/[ID]/edit`

- [ ] **Service Account добавлен в Google Sheets**
  - Открыта нужная таблица
  - Нажато "Share"
  - Добавлен email Service Account
  - Выданы права "Editor" ✏️

### 2. Проверка кода

- [ ] **Все файлы на месте**
  - `Procfile` существует
  - `runtime.txt` существует
  - `worker.py` существует
  - `requirements.txt` существует
  - `app.json` существует

- [ ] **Удалены демо-файлы**
  - `create_demo_sheet.py` удален ✅
  - Нет файлов с "DEMO" или "Test" в названии

- [ ] **Код закоммичен в git**
  ```bash
  git add .
  git commit -m "Готов к деплою на Heroku"
  ```

## 🚀 Деплой на Heroku

### 3. Создание приложения

- [ ] **Heroku CLI установлен**
  ```bash
  heroku --version
  ```

- [ ] **Вход в Heroku выполнен**
  ```bash
  heroku login
  ```

- [ ] **Приложение создано**
  ```bash
  heroku create fonbet-stats-updater
  ```

### 4. Настройка переменных окружения

- [ ] **APPSFLYER_API_KEY установлен**
  ```bash
  heroku config:set APPSFLYER_API_KEY="ваш_токен"
  ```

- [ ] **GOOGLE_SPREADSHEET_ID установлен**
  ```bash
  heroku config:set GOOGLE_SPREADSHEET_ID="id_таблицы"
  ```

- [ ] **GOOGLE_CLIENT_EMAIL установлен**
  ```bash
  heroku config:set GOOGLE_CLIENT_EMAIL="your-sa@project.iam.gserviceaccount.com"
  ```

- [ ] **GOOGLE_PRIVATE_KEY установлен**
  ```bash
  heroku config:set GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----
  ...
  -----END PRIVATE KEY-----"
  ```
  ⚠️ **Важно**: Сохраните переносы строк как `\n`!

- [ ] **Все переменные проверены**
  ```bash
  heroku config
  ```

### 5. Деплой кода

- [ ] **Код загружен на Heroku**
  ```bash
  git push heroku master
  ```

- [ ] **Build завершился успешно**
  - Проверьте вывод команды
  - Должно быть: "Build succeeded"

### 6. Запуск worker

- [ ] **Worker запущен**
  ```bash
  heroku ps:scale worker=1
  ```

- [ ] **Worker работает**
  ```bash
  heroku ps
  ```
  Должно быть: `worker.1: up`

## 🔍 Проверка работы

### 7. Мониторинг

- [ ] **Логи проверены**
  ```bash
  heroku logs --tail
  ```
  - Нет ошибок
  - Worker запустился
  - Конфигурация валидна

- [ ] **Тестовый запуск выполнен** (опционально)
  ```bash
  heroku run python -c "from worker import run_update; run_update()"
  ```
  - Подключение к AppsFlyer успешно
  - Подключение к Google Sheets успешно
  - Данные обновлены

### 8. Проверка Google Sheets

- [ ] **Лист создан в таблице**
  - Открыта Google Sheets
  - Найден лист `AF_Stats_Ноябрь25` (или текущий месяц)

- [ ] **Данные присутствуют**
  - Есть заголовки
  - Есть строки с данными
  - Дата обновления актуальна

- [ ] **Формат данных правильный**
  - Media Source отображается корректно
  - Deposits подсчитаны
  - Revenue рассчитан

## ⏰ Финальная проверка расписания

### 9. Расписание

- [ ] **Worker настроен на правильное время**
  - Код содержит: `schedule.every().day.at("05:00")` (это 8:00 МСК)
  - Проверка воскресенья работает: `should_run_today()`

- [ ] **Ожидание первого автоматического запуска**
  - Следующий запуск: завтра в 8:00 МСК (если не воскресенье)
  - Логи будут показывать: "Worker работает" каждый час

## 💰 Оплата

### 10. Billing (опционально)

- [ ] **Понимаю стоимость**
  - Eco dyno: ~$5/месяц
  - Hobby dyno: ~$7/месяц
  - Worker работает 24/7

- [ ] **Рассмотрел альтернативу Heroku Scheduler** (опционально)
  - Scheduler addon бесплатный
  - Но нужно изменить подход (не worker, а cron-задача)

## 📝 Документация

### 11. Сохранение информации

- [ ] **Сохранены важные данные**
  - URL приложения Heroku
  - ID Google Spreadsheet
  - Email Service Account

- [ ] **Команда знает как проверять логи**
  ```bash
  heroku logs --tail
  ```

- [ ] **Команда знает как перезапустить**
  ```bash
  heroku ps:restart worker
  ```

## 🎉 Готово!

Если все пункты отмечены ✅, ваше приложение готово к работе!

### Что дальше?

1. **Мониторинг**: Проверяйте логи раз в день первую неделю
2. **Проверка данных**: Сверяйте данные в Google Sheets с AppsFlyer
3. **Оптимизация**: При необходимости настройте расписание

### Полезные команды на каждый день

```bash
# Проверить статус
heroku ps

# Посмотреть логи
heroku logs --tail

# Перезапустить
heroku ps:restart worker

# Проверить переменные
heroku config

# Остановить worker
heroku ps:scale worker=0

# Запустить worker
heroku ps:scale worker=1
```

---

**🚀 Успешного деплоя!**


