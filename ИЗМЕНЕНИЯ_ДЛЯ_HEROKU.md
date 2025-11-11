# 📝 Изменения для деплоя на Heroku

## ✅ Добавленные файлы

### Конфигурация Heroku
1. **`Procfile`** - определяет как запускать worker на Heroku
2. **`runtime.txt`** - указывает версию Python (3.11.6)
3. **`worker.py`** - главный скрипт с расписанием (8:00 МСК, кроме ВС)
4. **`app.json`** - метаданные приложения для Heroku

### Документация
5. **`HEROKU_DEPLOY.md`** - полная инструкция по деплою
6. **`HEROKU_QUICKSTART.md`** - быстрый старт за 5 минут
7. **`HEROKU_CHECKLIST.md`** - чеклист с галочками
8. **`README_HEROKU.md`** - обзор проекта для Heroku
9. **`ENV_VARIABLES.md`** - описание переменных окружения
10. **`HEROKU_READY.md`** - сводка готовности проекта
11. **`ГОТОВО_HEROKU.md`** - краткая инструкция на русском
12. **`ИЗМЕНЕНИЯ_ДЛЯ_HEROKU.md`** - этот файл

## ❌ Удаленные файлы

1. **`create_demo_sheet.py`** - больше не нужен, так как работаем только с реальными данными

## 🔄 Изменённые файлы

### 1. `src/fonbet_stats_updater.py`
**Изменено:**
```python
# БЫЛО:
def update_monthly_stats(
    self, 
    year: Optional[int] = None, 
    month: Optional[int] = None,
    spend_data: Optional[Dict[tuple, float]] = None,
    test_mode: bool = False,  # ← Удалён
    load_spend_from_sheet: bool = False
):
    ...
    if test_mode:
        sheet_name = "AF_Stats_Тест"  # ← Удалено
    else:
        sheet_name = self.get_sheet_name_for_month(year, month)

# СТАЛО:
def update_monthly_stats(
    self, 
    year: Optional[int] = None, 
    month: Optional[int] = None,
    spend_data: Optional[Dict[tuple, float]] = None,
    load_spend_from_sheet: bool = False
):
    ...
    sheet_name = self.get_sheet_name_for_month(year, month)  # Только текущий месяц
```

**Зачем:** Убрали тестовый режим, работаем только с реальными данными текущего месяца.

### 2. `requirements.txt`
**Изменено:** Файл не изменился, все зависимости уже были правильными.

## 🎯 Что теперь делает приложение

### Раньше:
- ❌ Мог создавать демо-листы (`AF_Stats_Демо`)
- ❌ Мог создавать тестовые листы (`AF_Stats_Тест`)
- ⚠️ Требовал ручного запуска

### Теперь:
- ✅ Создает/обновляет **только лист текущего месяца**
- ✅ Формат: `AF_Stats_Ноябрь25`, `AF_Stats_Декабрь25`
- ✅ **Не трогает** листы за предыдущие месяцы
- ✅ Запускается **автоматически** каждый день в 8:00 МСК
- ✅ **Не запускается по воскресеньям**
- ✅ Работает на Heroku без вмешательства

## 📊 Структура листов в Google Sheets

### Автоматически создаваемые листы:
```
Google Spreadsheet
├── AF_Stats_Ноябрь25     ← Обновляется автоматически в ноябре
├── AF_Stats_Декабрь25    ← Будет создан в декабре
├── AF_Stats_Январь26     ← Будет создан в январе
└── ... (и так далее)
```

### НЕ создаются больше:
- ❌ `AF_Stats_Демо`
- ❌ `AF_Stats_Тест`
- ❌ `Test`
- ❌ Любые тестовые/демо листы

## ⏰ Расписание работы

### worker.py - Логика расписания:

```python
# Часовой пояс Москвы (UTC+3)
MOSCOW_OFFSET = timedelta(hours=3)

def get_moscow_time():
    """Получить текущее время в МСК"""
    utc_now = datetime.now(timezone.utc)
    moscow_now = utc_now + MOSCOW_OFFSET
    return moscow_now

def should_run_today():
    """Проверка, нужно ли запускать обновление сегодня"""
    moscow_now = get_moscow_time()
    is_sunday = moscow_now.weekday() == 6  # 6 = воскресенье
    
    if is_sunday:
        logger.info("Сегодня воскресенье - пропускаем обновление")
        return False
    
    return True

# Расписание: 05:00 UTC = 08:00 МСК
schedule.every().day.at("05:00").do(scheduled_job)
```

**Итог:**
- Запуск: Понедельник-Суббота в 8:00 МСК
- Пропуск: Воскресенье

## 🔐 Переменные окружения на Heroku

### Обязательные:
```bash
APPSFLYER_API_KEY          # AppsFlyer API Token
GOOGLE_SPREADSHEET_ID      # ID Google таблицы
GOOGLE_CLIENT_EMAIL        # Email Service Account
GOOGLE_PRIVATE_KEY         # Private Key из JSON файла
```

### Опциональные (уже есть defaults):
```bash
FONBET_ANDROID_APP_ID      # По умолчанию: ru.bkfon-Android
FONBET_IOS_APP_ID          # По умолчанию: id1166619854
MAX_DAYS_BETWEEN_INSTALL_AND_EVENT  # По умолчанию: 30
```

## 🚀 Готовность к деплою

### Проверка файлов:
```
✅ Procfile                  - есть
✅ runtime.txt               - есть
✅ requirements.txt          - есть
✅ worker.py                 - есть
✅ app.json                  - есть
✅ src/fonbet_stats_updater.py - обновлен (без test_mode)
✅ src/google_sheets_service.py - готов (Service Account)
✅ src/config.py             - готов (env vars)
```

### Проверка документации:
```
✅ HEROKU_DEPLOY.md         - полная инструкция
✅ HEROKU_QUICKSTART.md     - быстрый старт
✅ HEROKU_CHECKLIST.md      - чеклист
✅ README_HEROKU.md         - обзор
✅ ENV_VARIABLES.md         - переменные
✅ ГОТОВО_HEROKU.md         - краткая инструкция
```

## 📦 Следующие шаги

1. **Прочитайте** → `HEROKU_QUICKSTART.md` или `ГОТОВО_HEROKU.md`
2. **Соберите ключи** → AppsFlyer Token, Google Service Account
3. **Создайте приложение** → `heroku create`
4. **Настройте env vars** → `heroku config:set ...`
5. **Задеплойте** → `git push heroku master`
6. **Запустите worker** → `heroku ps:scale worker=1`
7. **Проверьте логи** → `heroku logs --tail`

## ✅ Итоговая сводка

### Что имеем:
- ✅ Проект готов к деплою на Heroku
- ✅ Worker работает по расписанию (8:00 МСК, кроме ВС)
- ✅ Обновляет только текущий месяц
- ✅ Никаких демо/тестовых листов
- ✅ Полная документация на русском
- ✅ Production ready

### Что нужно от вас:
1. Получить ключи (AppsFlyer, Google)
2. Создать Heroku app
3. Настроить переменные окружения
4. Задеплоить код
5. Запустить worker

**Время на деплой: ~10-15 минут**

---

🎊 **Всё готово! Можно деплоить на Heroku!** 🚀


