# 🚀 Автоматизация статистики Фонбет из AppsFlyer

## ✅ Что реализовано

Скрипт для автоматического сбора статистики депозитов (af_ftd) из AppsFlyer и обновления Google Sheets.

## 📊 Что делает скрипт

1. **Получает данные из AppsFlyer** - события `af_ftd` для приложения `ru.bkfon-Android`
2. **Фильтрует события** - только где `event_time - install_time < 30 дней`
3. **Группирует по источникам** - Media Source (mintegral_int, unity_int, bigoads_int и т.д.)
4. **Разделяет по платформам** - iOS/Android (из поля Platform в данных)
5. **Создает отдельный лист** - `AF_Stats_Октябрь25` (НЕ изменяет существующие листы)
6. **Заполняет статистику** - Spend, Revenue, Profit, ROI, Deposits, Campaigns

## 🎯 Главное

**Скрипт создает ОТДЕЛЬНЫЙ лист** с префиксом `AF_Stats_` и НЕ изменяет ваши существующие листы!

## 🚀 Использование

### Обновление за текущий месяц

```bash
python update_fonbet_stats.py
```

Создаст/обновит лист типа `AF_Stats_Ноябрь25`

### Обновление за конкретный месяц

```bash
python update_fonbet_stats.py --year 2025 --month 10
```

Создаст/обновит лист `AF_Stats_Октябрь25`

### Автоматический запуск (каждый день в 10:00)

```bash
python src/scheduler.py
```

## 📋 Структура создаваемой таблицы

Лист `AF_Stats_Октябрь25` будет содержать:

| Source | Platform | Spend $ | Revenue $ | Profit $ | ROI % | Deposits | Campaigns |
|--------|----------|---------|-----------|----------|-------|----------|-----------|
| mintegral_int | iOS | $0,00 | $450,00 | $450,00 | #DIV/0! | 2 | 1 |
| unity_int | iOS | $0,00 | $500,00 | $500,00 | #DIV/0! | 1 | 1 |
| christadselj_int | Android | $0,00 | $600,00 | $600,00 | #DIV/0! | 2 | 1 |
| bigoads_int | Android | $0,00 | $250,00 | $250,00 | #DIV/0! | 1 | 1 |
| ironsource_int | Android | $0,00 | $180,00 | $180,00 | #DIV/0! | 1 | 1 |
| ... | ... | ... | ... | ... | ... | ... | ... |
| **Total** | | **$0,00** | **$2,580,00** | **$2,580,00** | **#DIV/0!** | **12** | |

**Примечания:**
- Media Source показываются как есть (mintegral_int, unity_int, bigoads_int и т.д.)
- Разделение на iOS/Android определяется из поля Platform в данных
- Spend = $0 по умолчанию (можно загрузить из существующих листов через `--load-spend`)

## 🔍 Как работает группировка

1. **Media Source** - используется как есть из данных AppsFlyer
   - Примеры: `mintegral_int`, `unity_int`, `bigoads_int`, `ironsource_int`

2. **Platform** - определяется из поля `Platform` в данных
   - Если Platform = "android" → Android
   - Если Platform = "ios" → iOS
   - Также проверяется App ID и название кампании

3. **Группировка** - по (Media Source, Platform)
   - `(mintegral_int, ios)` - отдельная группа
   - `(mintegral_int, android)` - отдельная группа

## ⚠️ Важно

- ✅ **Существующие листы НЕ изменяются**
- ✅ **Создается отдельный лист** с префиксом `AF_Stats_`
- ✅ **Media Source как в AppsFlyer** (с суффиксами _int, _ios и т.д.)
- ✅ **Разделение iOS/Android** из поля Platform в данных

## 📝 Названия листов

- `AF_Stats_Октябрь25` (октябрь 2025)
- `AF_Stats_Ноябрь25` (ноябрь 2025)
- `AF_Stats_Декабрь25` (декабрь 2025)
- `AF_Stats_Демо` (демонстрационный лист)

## 💡 Примеры

### Проверка демо-листа

Лист `AF_Stats_Демо` уже создан - проверьте его в Google таблице!

Там видно:
- ✅ mintegral_int, unity_int, bigoads_int, ironsource_int - все источники
- ✅ Разделение на iOS и Android
- ✅ Правильная группировка

### Создание для реальных данных

```bash
# Завтра (когда лимит API обновится) запустите:
python update_fonbet_stats.py --year 2025 --month 10
```

Это создаст лист `AF_Stats_Октябрь25` с реальными данными за весь месяц.

## 🔧 Дополнительные опции

```bash
# С загрузкой Spend из существующих листов
python update_fonbet_stats.py --year 2025 --month 10 --load-spend

# Создать демо/тестовый лист
python create_demo_sheet.py
```

## 📊 Лимит API

⚠️ **Важно:** AppsFlyer ограничивает количество запросов в день.

Если видите ошибку:
```
You've reached your maximum number of in-app event reports
```

Это значит что лимит достигнут на сегодня. Попробуйте завтра или используйте `create_demo_sheet.py` для демонстрации.

## ✅ Готово!

Проверьте лист `AF_Stats_Демо` в вашей Google таблице:
https://docs.google.com/spreadsheets/d/1_CDw5CGuhSWXx-szzkRwO4ED6OQm2ED4ZX9ZSCN_S20/

Там должна быть правильная структура с:
- ✅ mintegral_int, unity_int, bigoads_int, ironsource_int
- ✅ Разделение iOS/Android
- ✅ Spend, Revenue, Profit, ROI
- ✅ Deposits, Campaigns

---

**Все работает!** 🎉

