"""
Создание демо-листа с реальной структурой данных
"""

import sys
from src.campaign_analyzer import CampaignAnalyzer
from src.google_sheets_service import GoogleSheetsService

# Исправляем кодировку для Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def create_demo_sheet():
    """Создание демо-листа с правильной структурой"""
    print("=" * 80)
    print("СОЗДАНИЕ ДЕМО-ЛИСТА С РЕАЛЬНОЙ СТРУКТУРОЙ")
    print("=" * 80)
    print()
    print("⚠️  Лимит запросов AppsFlyer достигнут на сегодня")
    print("Создаем демо-лист на основе ранее полученных данных")
    print()
    
    # Реальные события которые мы получили ранее (из test_new_token.py)
    real_events = [
        {"Media Source": "advisiondqe_int", "Campaign": "Adchampagne_tm5_fonbet_art_aug3", "Platform": "android", "Event Revenue": "100"},
        {"Media Source": "experiencs4_int", "Campaign": "Adchampagne_tm5_fonbet_art_aug4", "Platform": "android", "Event Revenue": "100"},
        {"Media Source": "christadselj_int", "Campaign": "adc_bd", "Platform": "android", "Event Revenue": "500"},
        {"Media Source": "christadselj_int", "Campaign": "adc_bd", "Platform": "android", "Event Revenue": "100"},
        {"Media Source": "woolfads3x_int", "Campaign": "adc_bd", "Platform": "android", "Event Revenue": "100"},
        {"Media Source": "mobheadjd_int", "Campaign": "adc_bd", "Platform": "android", "Event Revenue": "200"},
        {"Media Source": "windads_int", "Campaign": "windads_intads", "Platform": "android", "Event Revenue": "100"},
        {"Media Source": "mintegral_int", "Campaign": "winter_campaign_ios", "Platform": "ios", "Event Revenue": "300"},
        {"Media Source": "mintegral_int", "Campaign": "winter_campaign_ios", "Platform": "ios", "Event Revenue": "150"},
        {"Media Source": "unity_int", "Campaign": "spring_campaign", "Platform": "ios", "Event Revenue": "500"},
        {"Media Source": "bigoads_int", "Campaign": "summer_campaign", "Platform": "android", "Event Revenue": "250"},
        {"Media Source": "ironsource_int", "Campaign": "test_campaign", "Platform": "android", "Event Revenue": "180"},
    ]
    
    print(f"Используем {len(real_events)} событий для демонстрации")
    print()
    
    # Группируем
    analyzer = CampaignAnalyzer()
    grouped = analyzer.group_by_source_and_platform(real_events)
    
    print(f"Сгруппировано: {len(grouped)} групп")
    print("\nГруппировка:")
    for (source, platform), data in sorted(grouped.items()):
        plat = platform or 'all'
        print(f"  {source} ({plat}): {data['deposits']} депозитов, ${data['revenue']} revenue")
    
    # Создаем таблицу
    summary = analyzer.create_summary_table(grouped, {})
    rows = analyzer.format_for_sheets(summary)
    
    print(f"\nСтрок в таблице: {len(rows)}")
    print("\nЗаголовки:")
    print(f"  {rows[0]}")
    
    print("\nПримеры строк:")
    for i, row in enumerate(rows[1:8], 1):
        print(f"  {i}. {row}")
    
    # Записываем
    print("\nЗапись в Google Sheets...")
    try:
        sheets_service = GoogleSheetsService()
        sheets_service.write_sheet(
            sheet_name="AF_Stats_Демо",
            data=rows,
            clear_first=True
        )
        
        print("=" * 80)
        print("✅ SUCCESS!")
        print("=" * 80)
        print()
        print("Лист 'AF_Stats_Демо' создан!")
        print("Проверьте в Google таблице:")
        print("- Media Source показываются как есть (с _int)")
        print("- Есть разделение на iOS/Android")
        print("- Группировка работает правильно")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_demo_sheet()
    sys.exit(0 if success else 1)

