# Примеры использования

## 1. Базовое использование

### Однократное обновление за текущий месяц

```bash
python run_once.py
```

или

```bash
python -m src.main
```

**Что происходит:**
- Получение данных из AppsFlyer за текущий месяц (с 1-го до вчерашнего дня)
- Фильтрация событий (только депозиты с event_time - install_time < 30 дней)
- Обновление Google Sheets

### Обновление за конкретный месяц

```bash
python -m src.main --year 2024 --month 10
```

**Пример вывода:**
```
================================================================================
НАЧАЛО ОБНОВЛЕНИЯ СТАТИСТИКИ ФОНБЕТ
================================================================================

[1/3] Получение данных из AppsFlyer...
INFO:src.appsflyer_client:Запрос данных для app_id=ru.bkfon-Android, период 2024-10-01 - 2024-10-29, событие=af_ftd
INFO:src.appsflyer_client:Получено 150 записей для ru.bkfon-Android
Получено всего событий: 150

[2/3] Обработка данных...
INFO:src.data_processor:Обработка данных для ru.bkfon-Android: 150 событий
INFO:src.data_processor:Отфильтровано событий: 150 -> 120
  ru.bkfon-Android: 150 событий, 120 валидных, 15 уникальных кампаний

[3/3] Обновление Google Sheets...
INFO:src.google_sheets_updater:Успешная аутентификация в Google Sheets API
INFO:src.google_sheets_updater:Обновлено 45 ячеек в листе 'Фонбет_2024_10'

================================================================================
ОБНОВЛЕНИЕ СТАТИСТИКИ ЗАВЕРШЕНО УСПЕШНО
================================================================================
```

## 2. Работа с планировщиком

### Запуск планировщика

```bash
python run_scheduler.py
```

**Вывод:**
```
================================================================================
ЗАПУСК ПЛАНИРОВЩИКА ОБНОВЛЕНИЯ СТАТИСТИКИ ФОНБЕТ
================================================================================

⏰ Планировщик запущен
📅 Обновление будет происходить каждый день в 10:00
⏹️  Для остановки нажмите Ctrl+C

INFO:src.scheduler:Планировщик запущен. Обновление будет происходить каждый день в 10:00
```

### Изменение времени запуска

В файле `.env`:
```env
SCHEDULE_TIME=14:30
```

Планировщик будет запускаться в 14:30 каждый день.

## 3. Программное использование

### Пример 1: Простое обновление

```python
from src.main import update_fonbet_stats

# Обновление за текущий месяц
result = update_fonbet_stats()

print(f"Обработано приложений: {len(result)}")
for app_id, data in result.items():
    print(f"{app_id}: {data['valid_events']} депозитов")
```

### Пример 2: Обновление за конкретный период

```python
from src.main import update_fonbet_stats

# Обновление за октябрь 2024
result = update_fonbet_stats(year=2024, month=10)
```

### Пример 3: Работа с AppsFlyer клиентом

```python
from src.appsflyer_client import AppsFlyerClient
from datetime import datetime

# Создаем клиента
client = AppsFlyerClient()

# Получаем данные за период
from_date = datetime(2024, 10, 1)
to_date = datetime(2024, 10, 31)

events = client.get_in_app_events_report(
    app_id="ru.bkfon-Android",
    from_date=from_date,
    to_date=to_date,
    event_name="af_ftd"
)

print(f"Получено {len(events)} событий")
```

### Пример 4: Обработка данных

```python
from src.data_processor import DataProcessor

# Создаем процессор
processor = DataProcessor(max_days=30)

# Предположим, у нас есть список событий
events = [...]  # список событий от AppsFlyer

# Фильтруем валидные события
valid_events = processor.filter_events(events)

# Группируем по источнику и кампании
grouped = processor.group_by_source_and_campaign(valid_events)

for (source, campaign), count in grouped.items():
    print(f"{source} / {campaign}: {count} депозитов")
```

### Пример 5: Работа с Google Sheets

```python
from src.google_sheets_updater import GoogleSheetsUpdater

# Создаем обновлятор
updater = GoogleSheetsUpdater()

# Аутентификация
updater.authenticate()

# Обновляем таблицу
data = [
    ["Header 1", "Header 2", "Header 3"],
    ["Value 1", "Value 2", "Value 3"],
    ["Value 4", "Value 5", "Value 6"]
]

updater.update_sheet("TestSheet", data, clear_first=True)
```

## 4. Кастомизация

### Изменение максимального количества дней

В файле `.env`:
```env
MAX_DAYS_BETWEEN_INSTALL_AND_EVENT=45
```

Теперь будут учитываться события до 45 дней после установки.

### Использование другого события

В файле `src/config.py` измените:
```python
EVENT_NAME: str = "af_purchase"  # вместо af_ftd
```

### Настройка нескольких приложений

В файле `.env`:
```env
FONBET_IOS_APP_ID=id1234567890
FONBET_ANDROID_APP_ID=ru.bkfon-Android
```

Скрипт автоматически обработает оба приложения.

## 5. Продвинутое использование

### Кастомный планировщик

```python
from src.scheduler import StatisticsScheduler
import schedule

# Создаем планировщик
scheduler = StatisticsScheduler()

# Запускаем сразу при старте
scheduler.run_once()

# Настраиваем дополнительные задачи
schedule.every().monday.at("09:00").do(scheduler.scheduled_job)
schedule.every().friday.at("18:00").do(scheduler.scheduled_job)

# Запускаем
scheduler.run()
```

### Обработка нескольких источников данных

```python
from src.appsflyer_client import AppsFlyerClient
from src.data_processor import DataProcessor

# Клиент для Cupli аккаунта
client_cupli = AppsFlyerClient(api_key="cupli_api_key")

# Клиент для Advertex аккаунта
client_advertex = AppsFlyerClient(api_key="advertex_api_key")

# Получаем данные из обоих аккаунтов
events_cupli = client_cupli.get_monthly_report("ru.bkfon-Android")
events_advertex = client_advertex.get_monthly_report("ru.bkfon-Android")

# Объединяем
all_events = events_cupli + events_advertex

# Обрабатываем
processor = DataProcessor()
result = processor.process_app_data(all_events, "ru.bkfon-Android")
```

### Экспорт в разные форматы

```python
from src.appsflyer_client import AppsFlyerClient
from src.data_processor import DataProcessor
import pandas as pd

# Получаем и обрабатываем данные
client = AppsFlyerClient()
events = client.get_monthly_report("ru.bkfon-Android")

processor = DataProcessor()
result = processor.process_app_data(events, "ru.bkfon-Android")

# Конвертируем в DataFrame
df = pd.DataFrame(result['summary'])

# Экспорт в CSV
df.to_csv('fonbet_stats.csv', index=False)

# Экспорт в Excel
df.to_excel('fonbet_stats.xlsx', index=False)

print(f"Экспортировано {len(df)} записей")
```

## 6. Отладка и мониторинг

### Включение детального логирования

```python
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fonbet_stats.log'),
        logging.StreamHandler()
    ]
)

from src.main import update_fonbet_stats

# Теперь все операции будут детально логироваться
update_fonbet_stats()
```

### Мониторинг успешности обновлений

```python
from src.main import update_fonbet_stats
import smtplib
from email.message import EmailMessage

def send_notification(success, message):
    msg = EmailMessage()
    msg['Subject'] = 'Fonbet Stats Update'
    msg['From'] = 'your@email.com'
    msg['To'] = 'admin@email.com'
    msg.set_content(message)
    
    # Отправка email
    # ... (настройка SMTP)

try:
    result = update_fonbet_stats()
    send_notification(True, f"Обновление успешно: {len(result)} приложений")
except Exception as e:
    send_notification(False, f"Ошибка: {e}")
```

## 7. Анализ данных

### Получение топ кампаний

```python
from src.main import update_fonbet_stats

result = update_fonbet_stats()

for app_id, data in result.items():
    print(f"\n=== {app_id} ===")
    
    # Топ 10 кампаний по депозитам
    top_campaigns = sorted(
        data['summary'][:10],
        key=lambda x: x['Deposits (af_ftd)'],
        reverse=True
    )
    
    for i, campaign in enumerate(top_campaigns, 1):
        print(
            f"{i}. {campaign['Campaign']}: "
            f"{campaign['Deposits (af_ftd)']} депозитов"
        )
```

### Сравнение источников трафика

```python
from collections import defaultdict
from src.main import update_fonbet_stats

result = update_fonbet_stats()

for app_id, data in result.items():
    # Группируем по источникам
    sources = defaultdict(int)
    
    for item in data['summary']:
        sources[item['Media Source']] += item['Deposits (af_ftd)']
    
    print(f"\n=== Статистика по источникам для {app_id} ===")
    for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
        print(f"{source}: {count} депозитов")
```

## 8. Интеграция с другими системами

### Webhook уведомления

```python
import requests
from src.main import update_fonbet_stats

# Обновляем статистику
result = update_fonbet_stats()

# Отправляем в Slack/Discord/Telegram
webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

total_deposits = sum(data['valid_events'] for data in result.values())

message = {
    "text": f"✅ Статистика обновлена! Всего депозитов: {total_deposits}"
}

requests.post(webhook_url, json=message)
```

### API для получения данных

```python
from flask import Flask, jsonify
from src.main import update_fonbet_stats

app = Flask(__name__)

@app.route('/api/update')
def trigger_update():
    try:
        result = update_fonbet_stats()
        return jsonify({
            "status": "success",
            "data": result
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(port=5000)
```

## Заключение

Эти примеры показывают гибкость системы и различные способы её использования. Вы можете комбинировать и адаптировать эти примеры под свои нужды.


