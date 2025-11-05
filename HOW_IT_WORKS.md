# Как это работает

## 🔄 Рабочий процесс

### Ежедневное обновление (автоматический режим)

```
10:00 → Планировщик запускается
   ↓
Получение данных из AppsFlyer
   ↓
Фильтрация и обработка
   ↓
Обновление Google Sheets
   ↓
Готово! ✅
```

### Детальный процесс

#### 1. Инициализация (1 сек)

```python
# Загружаются конфигурационные параметры:
- AppsFlyer API ключ
- App IDs (iOS + Android)
- Google Sheets ID
- Параметры фильтрации (30 дней)
```

#### 2. Получение данных из AppsFlyer (5-30 сек)

```python
# Для каждого приложения:
1. Формируется HTTP запрос к AppsFlyer API
   URL: https://hq1.appsflyer.com/api/raw-data/export/app/{app_id}/in_app_events_report/v5
   
2. Параметры запроса:
   - api_token: ваш_ключ
   - from: 2024-10-01  (первое число месяца)
   - to: 2024-10-29    (вчерашний день)
   - event_name: af_ftd
   - timezone: UTC
   
3. AppsFlyer возвращает CSV файл:
   Event Time,Install Time,Media Source,Campaign,Event Name
   2024-10-15 10:00:00,2024-10-10 09:00:00,mintegral_int,campaign_1,af_ftd
   2024-10-15 11:00:00,2024-10-05 08:00:00,unity_int,campaign_2,af_ftd
   ...
   
4. CSV парсится в список словарей Python
```

#### 3. Обработка данных (<1 сек)

```python
# Для каждого события:

# Шаг 3.1: Фильтрация по времени
event_time = datetime("2024-10-15 10:00:00")
install_time = datetime("2024-10-10 09:00:00")
days_diff = (event_time - install_time).days  # = 5 дней

if days_diff < 30:
    # Событие валидно ✅
    valid_events.append(event)
else:
    # Событие невалидно ❌ (установка была более 30 дней назад)
    pass

# Шаг 3.2: Группировка
# Ключ = (Media Source, Campaign)
# Значение = количество депозитов

grouped = {
    ("mintegral_int", "campaign_1"): 15,  # 15 депозитов
    ("unity_int", "campaign_2"): 23,      # 23 депозита
    ...
}

# Шаг 3.3: Создание сводного отчета
summary = [
    {
        "Media Source": "mintegral_int",
        "Campaign": "campaign_1",
        "Deposits (af_ftd)": 15
    },
    ...
]
```

#### 4. Обновление Google Sheets (2-5 сек)

```python
# Шаг 4.1: Аутентификация
# - Проверяется наличие token.json
# - Если токен валиден, используется он
# - Если токен истек, обновляется автоматически

# Шаг 4.2: Формирование данных для таблицы
rows = [
    ["Дата обновления", "2024-10-30 10:00:00"],
    [],
    ["App ID", "Media Source", "Campaign", "Депозиты (af_ftd)"],
    ["ru.bkfon-Android", "mintegral_int", "campaign_1", 15],
    ["ru.bkfon-Android", "unity_int", "campaign_2", 23],
    ...
]

# Шаг 4.3: Создание или обновление листа
sheet_name = "Фонбет_2024_10"  # Год_Месяц

# Шаг 4.4: Очистка старых данных
clear_sheet(sheet_name)

# Шаг 4.5: Запись новых данных
update_sheet(sheet_name, rows)
```

## 🧮 Пример расчета

### Входные данные (CSV от AppsFlyer)

```csv
Event Time,Install Time,Media Source,Campaign,Event Name
2024-10-15 10:00:00,2024-10-10 09:00:00,mintegral_int,winter_campaign,af_ftd
2024-10-15 11:00:00,2024-10-10 09:00:00,mintegral_int,winter_campaign,af_ftd
2024-10-15 12:00:00,2024-10-05 08:00:00,unity_int,winter_campaign,af_ftd
2024-10-15 13:00:00,2023-09-10 07:00:00,ironSource_int,old_campaign,af_ftd
```

### Шаг 1: Фильтрация

```python
# Событие 1:
days = (2024-10-15 - 2024-10-10).days = 5 дней → ✅ ВАЛИДНО

# Событие 2:
days = (2024-10-15 - 2024-10-10).days = 5 дней → ✅ ВАЛИДНО

# Событие 3:
days = (2024-10-15 - 2024-10-05).days = 10 дней → ✅ ВАЛИДНО

# Событие 4:
days = (2024-10-15 - 2023-09-10).days = 400+ дней → ❌ НЕВАЛИДНО
```

### Шаг 2: Группировка

```python
grouped = {
    ("mintegral_int", "winter_campaign"): 2,  # 2 депозита
    ("unity_int", "winter_campaign"): 1,      # 1 депозит
}

# Событие 4 не учитывается, так как > 30 дней
```

### Шаг 3: Вывод в Google Sheets

```
| App ID           | Media Source   | Campaign        | Депозиты |
|------------------|----------------|-----------------|----------|
| ru.bkfon-Android | mintegral_int  | winter_campaign | 2        |
| ru.bkfon-Android | unity_int      | winter_campaign | 1        |
```

## 🔍 Детали реализации

### Почему фильтр < 30 дней?

```python
# Бизнес-логика:
# Мы хотим учитывать только "свежие" депозиты от новых пользователей
# Если пользователь установил приложение 2 месяца назад и только сейчас
# сделал депозит - это не считается результатом текущей кампании

# Пример:
Install: 2024-08-01
Deposit: 2024-10-15
Difference: 75 дней → НЕ засчитывается ❌

Install: 2024-10-01
Deposit: 2024-10-15
Difference: 14 дней → Засчитывается ✅
```

### Почему каждая строка = 1 депозит?

```python
# В AppsFlyer Raw Data Export:
# - Каждая строка = одно событие af_ftd
# - af_ftd = First Time Deposit (первый депозит)
# - Следовательно, каждая строка = 1 депозит

# Пример:
# 100 строк в CSV → 100 депозитов
# Если у одной кампании 15 строк → 15 депозитов в этой кампании
```

### Почему обновление за весь месяц?

```python
# Причины:
1. Данные в AppsFlyer могут обновляться с задержкой
   - События могут приходить не сразу
   - Атрибуция может измениться

2. Нужна актуальная картина
   - Полное обновление гарантирует актуальность
   - Нет риска пропустить какие-то события

3. Google Sheets
   - Проще полностью перезаписать, чем делать инкрементальное обновление
   - Нет проблем с дубликатами

# Производительность:
# Даже для 10000 событий обновление занимает < 10 секунд
```

## 🔧 Технические детали

### API лимиты

**AppsFlyer:**
- Зависит от вашего плана
- Обычно: 100-1000 запросов в час
- Наш случай: 2 запроса в день (iOS + Android)
- Проблем не будет ✅

**Google Sheets:**
- 100 запросов в 100 секунд на пользователя
- 500 запросов в 100 секунд на проект
- Наш случай: 2-3 запроса в день
- Проблем не будет ✅

### Обработка ошибок

```python
# Что может пойти не так:

1. AppsFlyer API недоступен
   → Повтор через 5 минут
   → Логирование ошибки
   → Уведомление (если настроено)

2. Google Sheets API недоступен
   → Сохранение данных локально
   → Повтор при следующем запуске

3. Токен истек
   → Автоматическое обновление
   → Если не получается - требуется повторная авторизация

4. Нет данных
   → Просто логируем
   → Это нормально (может не быть событий)
```

### Логирование

```python
# Все операции логируются:

INFO: "Запрос данных для app_id=ru.bkfon-Android"
INFO: "Получено 150 записей"
INFO: "Отфильтровано событий: 150 -> 120"
INFO: "Обновлено 45 ячеек в листе 'Фонбет_2024_10'"
INFO: "Обновление завершено успешно"

# При ошибках:
ERROR: "Ошибка при запросе к AppsFlyer API: 401 Unauthorized"
ERROR: "Ошибка при обновлении Google Sheets: Permission denied"
```

## 🎓 Советы по использованию

### Для разработчиков

```python
# Тестирование отдельных компонентов:

# 1. Тест AppsFlyer клиента
from src.appsflyer_client import AppsFlyerClient
client = AppsFlyerClient()
events = client.get_monthly_report("ru.bkfon-Android")
print(f"Получено {len(events)} событий")

# 2. Тест обработки данных
from src.data_processor import DataProcessor
processor = DataProcessor()
result = processor.process_app_data(events, "ru.bkfon-Android")
print(f"Валидных: {result['valid_events']}")

# 3. Тест Google Sheets (без реального обновления)
formatted = updater.format_processed_data_for_sheet({...})
print(formatted)  # Просмотр перед записью
```

### Для аналитиков

```python
# Получение данных программно:

from src.main import update_fonbet_stats

# Обновляем и получаем результат
result = update_fonbet_stats()

# Анализируем
for app_id, data in result.items():
    print(f"\n=== {app_id} ===")
    print(f"Всего депозитов: {data['valid_events']}")
    
    # Топ-5 кампаний
    top5 = sorted(data['summary'], 
                  key=lambda x: x['Deposits (af_ftd)'], 
                  reverse=True)[:5]
    
    for i, item in enumerate(top5, 1):
        print(f"{i}. {item['Campaign']}: {item['Deposits (af_ftd)']}")
```

## 📊 Мониторинг

### Что отслеживать

1. **Успешность обновлений**
   - Проверяйте логи ежедневно
   - Убедитесь, что данные обновляются

2. **Объем данных**
   - Если резкое изменение → возможна проблема
   - Следите за трендами

3. **Время выполнения**
   - Обычно 10-40 секунд
   - Если больше минуты → проверьте производительность

4. **Ошибки API**
   - AppsFlyer 401 → проверьте ключ
   - Google Sheets 403 → проверьте права

---

**Вопросы?** Проверьте другую документацию:
- [QUICKSTART.md](QUICKSTART.md) - быстрый старт
- [INSTALLATION.md](INSTALLATION.md) - установка
- [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - примеры


