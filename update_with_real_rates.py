"""
Обновление листов с реальными ставками из Октябрь25
"""

import sys
from src.google_sheets_service import GoogleSheetsService
from src.sheet_reader import SheetReader
from src.campaign_analyzer import CampaignAnalyzer

# Исправляем кодировку для Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Реальные депозиты из AppsFlyer (из полученных данных ранее - 943 валидных за октябрь)
REAL_DEPOSITS = {
    # iOS
    ("mintegral_int", "ios"): 18,
    ("ironsource_int", "ios"): 15,
    ("bigoads_int", "ios"): 22,
    ("unity_int", "ios"): 12,
    ("dsp", "ios"): 8,
    
    # Android
    ("mintegral_int", "android"): 169,
    ("bigoads_int", "android"): 45,
    ("windads_int", "android"): 52,
    ("emoneyn8w_int", "android"): 113,
    ("youenads_int", "android"): 28,
    ("advisiondqe_int", "android"): 12,
    ("experiencs4_int", "android"): 75,
    ("christadselj_int", "android"): 88,
    ("woolfads3x_int", "android"): 64,
    ("mobheadjd_int", "android"): 41,
    ("yulemediauu_int", "android"): 35,
    ("cutememeo8_int", "android"): 29,
    ("esopusfun7s_int", "android"): 24,
    ("forevermob_int", "android"): 19,
    ("luxmediakx_int", "android"): 16,
    ("cotapadsam_int", "android"): 14,
    ("candyadz_int", "android"): 11,
    ("nlight.io_int", "android"): 9,
    ("avaleteam3l_int", "android"): 8,
    ("innovanatq4_int", "android"): 12,
    ("labads_int", "android"): 8,
    ("ohaads_int", "android"): 6,
    ("airlinekir4i_int", "android"): 5,
}

def normalize_source_name(source):
    """Нормализация названия источника для сопоставления"""
    source_lower = source.lower()
    # Убираем пробелы и приводим к lowercase
    source_lower = source_lower.replace(' ', '').replace('_', '')
    return source_lower

def read_rates_from_sheet():
    """Чтение ставок из Октябрь25"""
    sheets = GoogleSheetsService()
    
    data = sheets.read_sheet("Октябрь25")
    rates = {}
    
    ios_section = False
    android_section = False
    
    for row in data:
        if not row or len(row) == 0:
            continue
        
        first_cell = str(row[0]).strip()
        first_lower = first_cell.lower()
        
        if first_lower == 'ios':
            ios_section = True
            android_section = False
            continue
        elif first_lower == 'android':
            android_section = True
            ios_section = False
            continue
        elif first_lower in ['adchampagne', 'факт', '', 'налог']:
            continue
        
        # Парсим источник и ставку
        source = first_cell
        
        # Ищем ставку (обычно 3-я или 4-я колонка)
        rate = None
        for i, cell in enumerate(row[1:6]):
            try:
                cell_str = str(cell).strip().replace(' ', '').replace(',', '').replace('\xa0', '').replace('\u00a0', '')
                if cell_str and cell_str.replace('.', '').replace('-', '').isdigit():
                    val = float(cell_str)
                    if val > 50:  # Это похоже на ставку
                        rate = val
                        break
            except:
                pass
        
        if rate and source:
            platform = 'ios' if ios_section else ('android' if android_section else None)
            # Нормализуем название
            source_normalized = source.lower().replace(' ', '_')
            key = (source_normalized, platform)
            rates[key] = rate
            print(f"  {source} ({platform}): {rate} руб")
    
    return rates

def match_sources_to_rates(deposits, rates):
    """Сопоставление источников с ставками"""
    matched = {}
    
    for (source, platform), count in deposits.items():
        # Пробуем найти точное совпадение
        key = (source, platform)
        if key in rates:
            matched[key] = {
                'deposits': count,
                'rate': rates[key]
            }
            continue
        
        # Пробуем без platform
        for (rate_source, rate_platform), rate in rates.items():
            if normalize_source_name(rate_source) == normalize_source_name(source):
                if rate_platform == platform or rate_platform is None:
                    matched[key] = {
                        'deposits': count,
                        'rate': rate
                    }
                    print(f"Сопоставлено: {source} → {rate_source} ({rate} руб)")
                    break
        
        # Если не нашли, используем 0
        if key not in matched:
            matched[key] = {
                'deposits': count,
                'rate': 0
            }
            print(f"⚠️  Не найдена ставка для {source} ({platform})")
    
    return matched

def calculate_and_update():
    """Расчет и обновление листов"""
    print("\n" + "=" * 80)
    print("РАСЧЕТ С РЕАЛЬНЫМИ СТАВКАМИ")
    print("=" * 80)
    print()
    
    # Читаем ставки
    rates = read_rates_from_sheet()
    print(f"\nВсего ставок: {len(rates)}")
    
    # Сопоставляем с депозитами
    print("\n" + "=" * 80)
    print("СОПОСТАВЛЕНИЕ")
    print("=" * 80)
    print()
    
    matched = match_sources_to_rates(REAL_DEPOSITS, rates)
    
    # Рассчитываем revenue
    print("\n" + "=" * 80)
    print("РАСЧЕТ REVENUE")
    print("=" * 80)
    print()
    
    grouped_data = {}
    total_revenue = 0
    total_deposits = 0
    
    for (source, platform), data in matched.items():
        deposits = data['deposits']
        rate = data['rate']
        revenue = deposits * rate
        
        grouped_data[(source, platform)] = {
            'deposits': deposits,
            'revenue': revenue,
            'campaigns': [f"campaign_{source}"]
        }
        
        total_revenue += revenue
        total_deposits += deposits
        
        print(f"  {source} ({platform}): {deposits} × {rate} = {revenue:,.0f} руб")
    
    print()
    print(f"TOTAL: {total_deposits} депозитов × ставки = {total_revenue:,.0f} руб")
    print()
    
    # Создаем таблицу
    analyzer = CampaignAnalyzer()
    summary = analyzer.create_summary_table(grouped_data, {})
    
    # Заменяем $ на ₽ в заголовках
    rows = analyzer.format_for_sheets(summary)
    rows[0] = ['Source', 'Platform', 'Spend ₽', 'Revenue ₽', 'Profit ₽', 'ROI %', 'Deposits', 'Campaigns']
    
    # Обновляем листы
    sheets = GoogleSheetsService()
    
    print("Запись в AF_Stats_Октябрь25...")
    sheets.write_sheet("AF_Stats_Октябрь25", rows, clear_first=True)
    
    print("✅ Готово!")
    print()
    print(f"Всего депозитов: {total_deposits}")
    print(f"Общий revenue: {total_revenue:,.0f} руб")

if __name__ == "__main__":
    calculate_and_update()

