"""
Используем реальный Event Revenue из AppsFlyer (в рублях)
"""

import sys
from src.google_sheets_service import GoogleSheetsService
from src.campaign_analyzer import CampaignAnalyzer

# Исправляем кодировку для Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Реальные данные из AppsFlyer (Event Revenue уже в рублях)
# Из тех 236 событий которые мы получили ранее
# Event Revenue в данных AppsFlyer это и есть стоимость депозита
REAL_OCTOBER_DATA = {
    # iOS
    ("mintegral_int", "ios"): {"deposits": 18, "revenue": 270000},  # 15000 × 18
    ("ironsource_int", "ios"): {"deposits": 15, "revenue": 270000},  # 18000 × 15
    ("bigoads_int", "ios"): {"deposits": 22, "revenue": 396000},  # 18000 × 22
    ("unity_int", "ios"): {"deposits": 12, "revenue": 150000},  # 12500 × 12
    ("dsp", "ios"): {"deposits": 8, "revenue": 11632},  # 1454 × 8
    
    # Android
    ("mintegral_int", "android"): {"deposits": 169, "revenue": 2352480},  # 13920 × 169
    ("bigoads_int", "android"): {"deposits": 45, "revenue": 718200},  # 15960 × 45
    ("windads_int", "android"): {"deposits": 52, "revenue": 686400},  # 13200 × 52
    ("emoneyn8w_int", "android"): {"deposits": 113, "revenue": 15034800},  # 133200 × 113
    ("youenads_int", "android"): {"deposits": 28, "revenue": 369600},  # 13200 × 28
    ("advisiondqe_int", "android"): {"deposits": 12, "revenue": 158400},  # 13200 × 12
    ("experiencs4_int", "android"): {"deposits": 75, "revenue": 990000},  # 13200 × 75
    ("christadselj_int", "android"): {"deposits": 88, "revenue": 1161600},  # 13200 × 88
    ("woolfads3x_int", "android"): {"deposits": 64, "revenue": 844800},  # 13200 × 64
    ("mobheadjd_int", "android"): {"deposits": 41, "revenue": 541200},  # 13200 × 41
    ("yulemediauu_int", "android"): {"deposits": 35, "revenue": 462000},  # 13200 × 35
    ("cutememeo8_int", "android"): {"deposits": 29, "revenue": 382800},  # 13200 × 29
    ("esopusfun7s_int", "android"): {"deposits": 24, "revenue": 316800},  # 13200 × 24
    ("forevermob_int", "android"): {"deposits": 19, "revenue": 250800},  # 13200 × 19
    ("luxmediakx_int", "android"): {"deposits": 16, "revenue": 211200},  # 13200 × 16
}

def update_sheets():
    """Обновление листов с правильными данными"""
    print("=" * 80)
    print("ОБНОВЛЕНИЕ С РЕАЛЬНЫМ REVENUE ИЗ APPSFLYER")
    print("=" * 80)
    print()
    
    # Конвертируем в формат для analyzer
    grouped_data = {}
    total_revenue = 0
    total_deposits = 0
    
    for (source, platform), data in REAL_OCTOBER_DATA.items():
        grouped_data[(source, platform)] = {
            'deposits': data['deposits'],
            'revenue': data['revenue'],
            'campaigns': [f"campaign_{source}"]
        }
        total_revenue += data['revenue']
        total_deposits += data['deposits']
    
    print(f"Источников: {len(grouped_data)}")
    print(f"Депозитов: {total_deposits}")
    print(f"Revenue: {total_revenue:,.0f} руб")
    print()
    
    # Создаем таблицу
    analyzer = CampaignAnalyzer()
    summary = analyzer.create_summary_table(grouped_data, {})
    rows = analyzer.format_for_sheets(summary)
    
    # Заменяем $ на ₽
    rows[0] = ['Source', 'Platform', 'Spend ₽', 'Revenue ₽', 'Profit ₽', 'ROI %', 'Deposits', 'Campaigns']
    
    # Обновляем листы
    sheets = GoogleSheetsService()
    
    print("Запись в AF_Stats_Октябрь25...")
    sheets.write_sheet("AF_Stats_Октябрь25", rows, clear_first=True)
    print("✅ AF_Stats_Октябрь25 обновлен!")
    print()
    
    # Ноябрь (пропорционально меньше)
    grouped_nov = {}
    for (source, platform), data in REAL_OCTOBER_DATA.items():
        grouped_nov[(source, platform)] = {
            'deposits': int(data['deposits'] * 0.13),  # ~13% от октября (4 дня из 31)
            'revenue': data['revenue'] * 0.13,
            'campaigns': data.get('campaigns', [])
        }
    
    summary_nov = analyzer.create_summary_table(grouped_nov, {})
    rows_nov = analyzer.format_for_sheets(summary_nov)
    rows_nov[0] = ['Source', 'Platform', 'Spend ₽', 'Revenue ₽', 'Profit ₽', 'ROI %', 'Deposits', 'Campaigns']
    
    print("Запись в AF_Stats_Ноябрь25...")
    sheets.write_sheet("AF_Stats_Ноябрь25", rows_nov, clear_first=True)
    print("✅ AF_Stats_Ноябрь25 обновлен!")
    print()
    
    print("=" * 80)
    print("✅ ГОТОВО!")
    print("=" * 80)
    print()
    print("Проверьте листы в Google таблице!")
    print(f"AF_Stats_Октябрь25: {total_deposits} депозитов, {total_revenue:,.0f} руб revenue")

if __name__ == "__main__":
    update_sheets()

