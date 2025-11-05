# Обзор файлов проекта

## 📁 Структура проекта

```
adc-afshit/
├── 📄 Документация
├── 🐍 Исходный код (src/)
├── 🧪 Тесты (tests/)
└── 🔧 Вспомогательные скрипты
```

## 📄 Документация

### Основная документация

| Файл | Назначение | Для кого |
|------|-----------|----------|
| **README.md** | Главное описание проекта | Все |
| **SUMMARY.md** | Краткая сводка проекта | Все (начните здесь!) |
| **QUICKSTART.md** | Быстрый старт за 5 минут | Новые пользователи |
| **INSTALLATION.md** | Детальная инструкция по установке | DevOps, разработчики |
| **HOW_IT_WORKS.md** | Подробное объяснение работы | Аналитики, разработчики |
| **USAGE_EXAMPLES.md** | Примеры использования | Разработчики, аналитики |
| **PROJECT_INFO.md** | Техническая информация | Разработчики |
| **TODO.md** | Планы развития | Product manager |
| **FILES_OVERVIEW.md** | Этот файл | Все |

### Конфигурация

| Файл | Назначение |
|------|-----------|
| **requirements.txt** | Список зависимостей Python |
| **pytest.ini** | Конфигурация тестов |
| **.gitignore** | Игнорируемые файлы Git |

## 🐍 Исходный код (src/)

### Основные модули

| Файл | Строк | Назначение | Основные классы/функции |
|------|-------|-----------|------------------------|
| **config.py** | ~70 | Конфигурация приложения | `Config` |
| **appsflyer_client.py** | ~140 | Клиент AppsFlyer API | `AppsFlyerClient` |
| **data_processor.py** | ~170 | Обработка данных | `DataProcessor` |
| **google_sheets_updater.py** | ~250 | Обновление Google Sheets | `GoogleSheetsUpdater` |
| **scheduler.py** | ~70 | Планировщик задач | `StatisticsScheduler` |
| **main.py** | ~100 | Оркестрация | `update_fonbet_stats()` |
| **__init__.py** | ~5 | Инициализация пакета | `__version__` |

### Детали модулей

#### config.py
```python
class Config:
    APPSFLYER_API_KEY      # API ключ AppsFlyer
    FONBET_IOS_APP_ID      # iOS App ID
    FONBET_ANDROID_APP_ID  # Android App ID
    GOOGLE_SPREADSHEET_ID  # ID таблицы
    SCHEDULE_TIME          # Время запуска (10:00)
    EVENT_NAME             # Название события (af_ftd)
```

#### appsflyer_client.py
```python
class AppsFlyerClient:
    get_in_app_events_report()    # Получение событий за период
    get_monthly_report()          # Получение за месяц
    get_reports_for_all_apps()    # Обработка всех приложений
```

#### data_processor.py
```python
class DataProcessor:
    filter_events()                      # Фильтрация валидных событий
    group_by_source_and_campaign()       # Группировка данных
    process_app_data()                   # Полная обработка
    is_valid_event()                     # Проверка: event_time - install_time < 30
```

#### google_sheets_updater.py
```python
class GoogleSheetsUpdater:
    authenticate()                      # OAuth 2.0 авторизация
    update_sheet()                      # Обновление листа
    format_processed_data_for_sheet()   # Форматирование данных
    get_or_create_sheet()              # Создание листа
```

#### scheduler.py
```python
class StatisticsScheduler:
    run()          # Запуск планировщика
    run_once()     # Однократное выполнение
```

#### main.py
```python
def update_fonbet_stats(year, month):
    # Оркестрация всего процесса:
    # 1. Получение данных из AppsFlyer
    # 2. Обработка данных
    # 3. Обновление Google Sheets
```

## 🧪 Тесты (tests/)

| Файл | Тестов | Покрытие | Что тестирует |
|------|--------|----------|---------------|
| **test_config.py** | 5 | 96% | Конфигурация |
| **test_appsflyer_client.py** | 9 | 93% | AppsFlyer API |
| **test_data_processor.py** | 15 | 95% | Обработка данных |
| **test_google_sheets_updater.py** | 8 | 70% | Google Sheets |
| **test_integration.py** | 4 | - | Интеграционные тесты |
| **conftest.py** | - | - | Фикстуры для тестов |

### Типы тестов

**Unit тесты (32 теста):**
- Тестирование отдельных функций и методов
- Изолированное тестирование компонентов
- Быстрые (< 1 секунды)

**Integration тесты (4 теста):**
- Тестирование взаимодействия компонентов
- Полный pipeline с mock данными
- Средние (~1-2 секунды)

**Mock тесты:**
- Тестирование без внешних зависимостей
- Используется `responses` для HTTP
- Используется `unittest.mock` для Google API

## 🔧 Вспомогательные скрипты

| Файл | Строк | Назначение | Использование |
|------|-------|-----------|---------------|
| **run_once.py** | ~20 | Однократный запуск | `python run_once.py` |
| **run_scheduler.py** | ~25 | Запуск планировщика | `python run_scheduler.py` |
| **setup_google_credentials.py** | ~100 | Настройка Google API | `python setup_google_credentials.py` |

### Детали

#### run_once.py
```python
# Простой запуск обновления статистики
# Полезно для:
# - Тестирования
# - Ручного обновления
# - Отладки
```

#### run_scheduler.py
```python
# Запуск планировщика
# - Работает постоянно
# - Обновление каждый день в 10:00
# - Логирование всех операций
```

#### setup_google_credentials.py
```python
# Мастер настройки Google Sheets API
# - Проверка credentials.json
# - Проверка token.json
# - Инструкции по настройке
# - Тестирование подключения
```

## 📊 Статистика кода

```
Всего файлов:          ~25
Документации:          ~8 файлов, ~3000 строк
Исходного кода:        6 модулей, ~800 строк
Тестов:                6 файлов, ~800 строк
Вспомогательных:       3 скрипта, ~150 строк
```

### По языкам

```
Python:    ~1750 строк
Markdown:  ~3000 строк
Config:    ~50 строк
```

### Покрытие тестами

```
config.py                96% ████████████████████░
appsflyer_client.py      93% ████████████████████░
data_processor.py        95% ████████████████████░
google_sheets_updater    70% ██████████████░░░░░░
main.py                   0% ░░░░░░░░░░░░░░░░░░░░ (точка входа)
scheduler.py              0% ░░░░░░░░░░░░░░░░░░░░ (точка входа)

Общее покрытие:          62% █████████████░░░░░░░
```

## 🔍 Как найти нужное

### Хочу понять, что это за проект
→ **SUMMARY.md** или **README.md**

### Хочу быстро запустить
→ **QUICKSTART.md**

### Нужна детальная установка
→ **INSTALLATION.md**

### Хочу понять, как это работает
→ **HOW_IT_WORKS.md**

### Нужны примеры кода
→ **USAGE_EXAMPLES.md**

### Техническая информация
→ **PROJECT_INFO.md**

### Планы развития
→ **TODO.md**

### Проблемы с Google Sheets
→ `python setup_google_credentials.py`

### Нужно запустить один раз
→ `python run_once.py`

### Нужен автоматический режим
→ `python run_scheduler.py`

### Изменить конфигурацию
→ Редактировать файл `.env` (или создать из `.env.example`)

### Посмотреть код AppsFlyer
→ **src/appsflyer_client.py**

### Посмотреть логику обработки
→ **src/data_processor.py**

### Посмотреть работу с Google Sheets
→ **src/google_sheets_updater.py**

### Запустить тесты
→ `pytest` или `pytest tests/test_*.py`

### Посмотреть примеры тестов
→ **tests/** (любой файл test_*.py)

## 📝 Примеры использования файлов

### Сценарий 1: Новый разработчик

```
1. README.md          → понимание проекта
2. QUICKSTART.md      → быстрый старт
3. run_once.py        → первый запуск
4. PROJECT_INFO.md    → изучение архитектуры
5. src/*.py           → изучение кода
```

### Сценарий 2: DevOps инженер

```
1. SUMMARY.md                    → обзор
2. INSTALLATION.md               → установка на сервере
3. setup_google_credentials.py   → настройка API
4. run_scheduler.py              → автозапуск
5. TODO.md                       → понимание планов
```

### Сценарий 3: Аналитик данных

```
1. QUICKSTART.md         → быстрый старт
2. HOW_IT_WORKS.md       → понимание процесса
3. USAGE_EXAMPLES.md     → примеры работы с данными
4. run_once.py           → получение данных
```

### Сценарий 4: Тестировщик

```
1. PROJECT_INFO.md    → понимание архитектуры
2. tests/conftest.py  → изучение фикстур
3. tests/test_*.py    → изучение тестов
4. pytest             → запуск тестов
```

## 🎯 Ключевые файлы

Если времени мало, изучите эти 5 файлов:

1. **SUMMARY.md** - что это за проект
2. **QUICKSTART.md** - как быстро запустить
3. **src/main.py** - основная логика
4. **src/config.py** - все настройки
5. **run_once.py** - точка входа

## 💡 Советы

### Для чтения кода

Рекомендуемый порядок изучения:
```
1. src/config.py             → понять настройки
2. src/appsflyer_client.py   → как получаем данные
3. src/data_processor.py     → как обрабатываем
4. src/google_sheets_updater.py → как обновляем
5. src/main.py               → как всё связано
6. src/scheduler.py          → как автоматизировано
```

### Для модификации

1. **Изменить время запуска** → `.env` (SCHEDULE_TIME)
2. **Добавить App ID** → `.env` (FONBET_*_APP_ID)
3. **Изменить фильтр** → `.env` (MAX_DAYS_BETWEEN_INSTALL_AND_EVENT)
4. **Изменить событие** → `src/config.py` (EVENT_NAME)
5. **Изменить формат таблицы** → `src/google_sheets_updater.py`

### Для отладки

1. **Проверить конфигурацию** → `python setup_google_credentials.py`
2. **Запустить тесты** → `pytest -v`
3. **Посмотреть логи** → вывод в консоли
4. **Тестовый запуск** → `python run_once.py`

---

**Этот файл** актуален на 30 октября 2024. При добавлении новых файлов обновите его.


