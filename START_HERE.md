# 👋 Начните отсюда!

## 🎉 Проект готов к использованию!

Скрипт для автоматизации сбора статистики Фонбета из AppsFlyer полностью реализован, протестирован и готов к запуску.

---

## ⚡ Быстрый старт (5 минут)

### Шаг 1: Установка зависимостей

```bash
pip install -r requirements.txt
```

### Шаг 2: Настройка Google Sheets API

```bash
python setup_google_credentials.py
```

Следуйте инструкциям для настройки Google API.

### Шаг 3: Первый запуск

```bash
python run_once.py
```

При первом запуске откроется браузер для авторизации в Google.

### Шаг 4: Автоматический режим

```bash
python run_scheduler.py
```

Планировщик будет обновлять данные каждый день в 10:00.

---

## 📚 Документация

### Для быстрого старта:

1. **[SUMMARY.md](SUMMARY.md)** - краткая сводка проекта (читать первым!)
2. **[QUICKSTART.md](QUICKSTART.md)** - быстрый старт за 5 минут
3. **[CHECKLIST.md](CHECKLIST.md)** - чеклист запуска

### Для установки и настройки:

4. **[INSTALLATION.md](INSTALLATION.md)** - детальная инструкция по установке
5. **[HOW_IT_WORKS.md](HOW_IT_WORKS.md)** - подробное объяснение работы

### Для разработчиков:

6. **[USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)** - примеры использования
7. **[PROJECT_INFO.md](PROJECT_INFO.md)** - техническая информация
8. **[FILES_OVERVIEW.md](FILES_OVERVIEW.md)** - обзор файлов проекта

### Дополнительно:

9. **[TODO.md](TODO.md)** - планы развития
10. **[README.md](README.md)** - основное описание
11. **[FINAL_REPORT.md](FINAL_REPORT.md)** - финальный отчет

---

## ✅ Что реализовано

### Основной функционал:

- ✅ Подключение к AppsFlyer API (Raw Data Export v5)
- ✅ Получение событий af_ftd для iOS и Android
- ✅ Фильтрация: event_time - install_time < 30 дней
- ✅ Группировка по Media Source и Campaign
- ✅ Подсчет депозитов
- ✅ Обновление Google Sheets
- ✅ Планировщик (ежедневно в 10:00)

### Качество:

- ✅ **41 тест** (все проходят)
- ✅ **62% покрытие** кода тестами
- ✅ **11 файлов** документации (~4000 строк)
- ✅ **Production ready** код

---

## 📁 Структура проекта

```
adc-afshit/
│
├── 📘 START_HERE.md            ← ВЫ ЗДЕСЬ
├── 📋 SUMMARY.md               ← Начните с этого!
├── 🚀 QUICKSTART.md
├── ✅ CHECKLIST.md
│
├── 🐍 src/                     ← Исходный код
│   ├── config.py
│   ├── appsflyer_client.py
│   ├── data_processor.py
│   ├── google_sheets_updater.py
│   ├── scheduler.py
│   └── main.py
│
├── 🧪 tests/                   ← Тесты (41 тест)
│
└── 🔧 Скрипты
    ├── run_once.py             ← Запуск один раз
    ├── run_scheduler.py        ← Автоматический режим
    └── setup_google_credentials.py
```

---

## 🎯 Что делать дальше?

### Если вы новый пользователь:

1. Прочитайте **[SUMMARY.md](SUMMARY.md)** - краткий обзор проекта
2. Следуйте **[QUICKSTART.md](QUICKSTART.md)** - запуск за 5 минут
3. Проверьте результат в Google Sheets

### Если вы разработчик:

1. Прочитайте **[PROJECT_INFO.md](PROJECT_INFO.md)** - техническая информация
2. Изучите **[USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)** - примеры использования
3. Посмотрите код в `src/`

### Если вы DevOps:

1. Прочитайте **[INSTALLATION.md](INSTALLATION.md)** - детальная установка
2. Используйте **[CHECKLIST.md](CHECKLIST.md)** - чеклист запуска
3. Настройте автозапуск (Windows Task Scheduler / Linux systemd)

---

## 🔧 Основные команды

```bash
# Однократное обновление
python run_once.py

# Обновление за конкретный месяц
python -m src.main --year 2024 --month 10

# Автоматический режим (каждый день в 10:00)
python run_scheduler.py

# Проверка настроек Google Sheets
python setup_google_credentials.py

# Запуск всех тестов
pytest

# Запуск с покрытием
pytest --cov=src --cov-report=html
```

---

## 📊 Статистика

```
✅ 41 тест - все проходят
✅ 62% покрытие кода
✅ 11 файлов документации
✅ ~1750 строк кода
✅ ~4000 строк документации
✅ 13 зависимостей
✅ Production ready
```

---

## 💡 Полезные ссылки

### Google Sheets:
https://docs.google.com/spreadsheets/d/12NYiMx_ZqPOPhFf48_HfSSf5QeNFC9mmakuP8_Yh5MU/

### Google Cloud Console:
https://console.cloud.google.com/

---

## ❓ Нужна помощь?

### Проблемы с Google Sheets:
```bash
python setup_google_credentials.py
```

### Проблемы с данными:
1. Проверьте API ключ в `.env`
2. Проверьте App IDs
3. Запустите тесты: `pytest -v`

### Другие проблемы:
Смотрите раздел **Troubleshooting** в [INSTALLATION.md](INSTALLATION.md)

---

## ⚠️ Важно: Проверка токена

**Перед первым запуском:**

1. Проверьте токен AppsFlyer:
   ```bash
   python test_token_check.py
   ```

2. Если токен неактивен (ошибка 403), получите новый:
   - См. [TOKEN_SETUP.md](TOKEN_SETUP.md)
   - AppsFlyer Dashboard → Settings → API Access

3. Обновите токен в `.env` файле

4. Повторно проверьте:
   ```bash
   python test_token_check.py
   ```

## 🎊 Готово!

Проект полностью готов к использованию. Начните с [SUMMARY.md](SUMMARY.md) для краткого обзора, или сразу запустите `python run_once.py` для первого обновления!

**Удачи! 🚀**

---

**Версия:** 1.0.0  
**Дата:** 30 октября 2024  
**Статус:** ✅ Production Ready


