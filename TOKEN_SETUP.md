# Настройка токена AppsFlyer API

## ⚠️ Важно!

Текущий токен возвращает ошибку "Inactive token". Это означает, что токен неактивен, истек или это не тот тип токена.

## Как получить правильный токен для Raw Data Export API

### Шаг 1: Вход в AppsFlyer Dashboard

1. Зайдите на https://hq1.appsflyer.com/
2. Войдите в свой аккаунт

### Шаг 2: Получение API токена

#### Вариант A: Pull API Token (для Raw Data Export)

1. Перейдите в **Settings** → **API Access**
2. Найдите раздел **Pull API** или **Raw Data Export API**
3. Создайте новый токен или используйте существующий
4. Убедитесь, что токен имеет права на:
   - **Export Data**
   - **In-App Events**
   - Доступ к нужным приложениям

#### Вариант B: API V2 Token

1. Перейдите в **Settings** → **API Access**
2. Найдите раздел **API V2** или **Partners API**
3. Создайте токен с правами на экспорт данных

### Шаг 3: Проверка типа токена

Токен для Raw Data Export API должен:
- Использоваться с заголовком `Authorization: Bearer {token}`
- Иметь права на экспорт данных
- Быть активным (не истекшим)

### Шаг 4: Обновление токена в проекте

После получения нового токена:

1. Откройте файл `.env` (или создайте его из `.env.example`)
2. Обновите значение `APPSFLYER_API_KEY`:

```env
APPSFLYER_API_KEY=ваш_новый_токен_здесь
```

3. Или установите переменную окружения:

```bash
# Windows PowerShell
$env:APPSFLYER_API_KEY="ваш_новый_токен"

# Linux/Mac
export APPSFLYER_API_KEY="ваш_новый_токен"
```

## Проверка токена

После обновления токена запустите тест:

```bash
python test_real_api.py
```

Если токен корректен, вы увидите успешный ответ с данными.

## Типичные ошибки

### "Inactive token"
- **Причина**: Токен неактивен или истек
- **Решение**: Создайте новый токен в AppsFlyer Dashboard

### "Missing authorization header"
- **Причина**: Токен не передается в заголовке Authorization
- **Решение**: Код обновлен для использования правильного формата

### "App ID not found"
- **Причина**: Неверный App ID или нет доступа к приложению
- **Решение**: Проверьте App ID в AppsFlyer Dashboard

## Дополнительная информация

### Требования к токену:

1. **Тип**: Pull API Token или Raw Data Export API Token
2. **Права**: Export Data, In-App Events
3. **Формат**: Используется с `Authorization: Bearer {token}`
4. **Статус**: Активен (не истек)

### Документация AppsFlyer:

- [Pull API Documentation](https://support.appsflyer.com/hc/en-us/articles/207447163)
- [Raw Data Export API](https://support.appsflyer.com/hc/en-us/articles/207447163-Raw-Data-Pull-API)
- [API Access Settings](https://support.appsflyer.com/hc/en-us/articles/207447163)

## Важно!

Токен, предоставленный в задании, возвращает "Inactive token". Это нормально - токены могут истекать или требовать активации в Dashboard.

После получения нового активного токена скрипт будет работать корректно.

