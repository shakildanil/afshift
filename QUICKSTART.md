# Быстрый старт

## За 5 минут до первого запуска

### 1. Установка (1 минута)

```bash
# Установите зависимости
pip install -r requirements.txt
```

### 2. Настройка Google Sheets (2 минуты)

```bash
# Проверьте настройки
python setup_google_credentials.py
```

Если `credentials.json` отсутствует:
1. Откройте https://console.cloud.google.com/
2. Создайте проект
3. Включите Google Sheets API
4. Создайте OAuth 2.0 credentials (Desktop app)
5. Скачайте и сохраните как `credentials.json`

### 3. Проверка конфигурации (30 секунд)

Убедитесь, что файл `.env` содержит:
- ✅ `APPSFLYER_API_KEY` - ключ API (уже указан)
- ✅ `FONBET_ANDROID_APP_ID=ru.bkfon-Android` (уже указан)
- ✅ `GOOGLE_SPREADSHEET_ID` - ID таблицы (уже указан)

### 4. Первый запуск (1 минута)

```bash
python run_once.py
```

При первом запуске:
- Откроется браузер → авторизуйтесь в Google
- Скрипт получит данные и обновит таблицу
- Готово! ✅

### 5. Проверка результата (30 секунд)

Откройте таблицу:
```
https://docs.google.com/spreadsheets/d/12NYiMx_ZqPOPhFf48_HfSSf5QeNFC9mmakuP8_Yh5MU/
```

Должен появиться новый лист с данными за текущий месяц.

---

## Автоматический запуск

После успешного тестового запуска:

```bash
python run_scheduler.py
```

Планировщик будет обновлять данные каждый день в 10:00 автоматически.

---

## Основные команды

```bash
# Однократное обновление
python run_once.py

# Обновление за конкретный месяц
python -m src.main --year 2024 --month 10

# Запуск планировщика
python run_scheduler.py

# Проверка настроек Google Sheets
python setup_google_credentials.py

# Запуск тестов
pytest
```

---

## Что делать, если что-то не работает?

### Ошибка: "credentials.json not found"
```bash
# Запустите мастер настройки
python setup_google_credentials.py
```

### Ошибка: "Invalid API token" от AppsFlyer
Проверьте ключ в файле `.env` - убедитесь, что он не содержит лишних пробелов.

### Пустой отчет / 0 событий
- Проверьте правильность App ID
- Убедитесь, что за указанный период есть события af_ftd

### Тесты не проходят
```bash
pip install -r requirements.txt --force-reinstall
pytest
```

---

## Структура проекта (для понимания)

```
adc-afshit/
├── run_once.py              ← Запуск обновления один раз
├── run_scheduler.py         ← Запуск планировщика
├── setup_google_credentials.py  ← Настройка Google API
├── src/
│   ├── appsflyer_client.py  ← Работа с AppsFlyer API
│   ├── data_processor.py    ← Обработка данных
│   ├── google_sheets_updater.py  ← Обновление таблиц
│   ├── scheduler.py         ← Планировщик
│   └── main.py              ← Основная логика
└── tests/                   ← Тесты (41 тест)
```

---

## Полная документация

- 📘 **README.md** - Полное описание проекта
- 📗 **INSTALLATION.md** - Детальная инструкция по установке
- 📕 **USAGE_EXAMPLES.md** - Примеры использования
- 📙 **PROJECT_INFO.md** - Техническая информация

---

## Поддержка

Все работает? Отлично! 🎉

Что-то не так? Проверьте документацию выше или запустите:
```bash
python setup_google_credentials.py  # для диагностики
pytest -v  # для проверки компонентов
```

---

**Версия:** 1.0.0  
**Создано:** 30 октября 2024


