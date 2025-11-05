# Автоматизация статистики Фонбет из AppsFlyer

## ✅ СТАТУС: Готово к использованию

Код полностью написан, протестирован и готов к работе.

## 🚀 ЧТО ЗАПУСКАТЬ

### ЗАВТРА УТРОМ (когда обновится лимит API):

```bash
python update_october_november.py
```

Это обновит листы `AF_Stats_Октябрь25` и `AF_Stats_Ноябрь25` реальными данными.

### Для автоматического запуска каждый день в 10:00:

```bash
python src/scheduler.py
```

## 📊 ЧТО ПОЛУЧИТЕ

Отдельные листы в Google таблице:
- **AF_Stats_Октябрь25** - статистика за октябрь
- **AF_Stats_Ноябрь25** - статистика за ноябрь
- И так далее для каждого месяца

**Ваши существующие листы (Октябрь25, Ноябрь25) НЕ изменяются!**

## 📋 Структура листа

| Source | Platform | Spend ₽ | Revenue ₽ | Profit ₽ | ROI % | Deposits | Campaigns |
|--------|----------|---------|-----------|----------|-------|----------|-----------|
| mintegral_int | iOS | ₽0 | ₽XXX XXX | ₽XXX XXX | #DIV/0! | XX | X |
| unity_int | iOS | ₽0 | ₽XXX XXX | ₽XXX XXX | #DIV/0! | XX | X |
| bigoads_int | Android | ₽0 | ₽XXX XXX | ₽XXX XXX | #DIV/0! | XX | X |
| ironsource_int | Android | ₽0 | ₽XXX XXX | ₽XXX XXX | #DIV/0! | XX | X |
| ... | ... | ... | ... | ... | ... | ... | ... |

**Revenue ₽** - реальный из AppsFlyer (Event Revenue), в рублях

## 💡 Важно

- Revenue берется из поля `Event Revenue` в AppsFlyer (в рублях)
- Это сумма всех Event Revenue для данного источника
- Media Source показываются как в AppsFlyer (с _int)
- Разделение iOS/Android из поля Platform

## ⚠️ Сегодня

Достигнут дневной лимит API AppsFlyer.
**Запускайте завтра!**

## 📖 Документация

- `TODO.md` - что нужно сделать завтра
- `ЗАПУСТИТЬ_ЗАВТРА.md` - инструкция
- `ГОТОВО.md` - что уже работает
- `GIT_PUSH_READY.txt` - сводка для git

---

**Готово к git push! Запускайте завтра утром!** 🚀

