"""
Чтение ставок из существующего листа Октябрь25
"""

import sys
from src.google_sheets_service import GoogleSheetsService

# Исправляем кодировку для Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def read_october_rates():
    """Читаем ставки из Октябрь25"""
    print("=" * 80)
    print("ЧТЕНИЕ СТАВОК ИЗ ЛИСТА ОКТЯБРЬ25")
    print("=" * 80)
    print()
    
    sheets = GoogleSheetsService()
    
    # Читаем лист Октябрь25
    try:
        data = sheets.read_sheet("Октябрь25")
        print(f"Прочитано строк: {len(data)}")
        print()
        
        # Показываем первые строки
        print("Первые 10 строк:")
        for i, row in enumerate(data[:10], 1):
            print(f"{i}. {row}")
        
        print()
        print("=" * 80)
        print("ПАРСИНГ СТАВОК")
        print("=" * 80)
        print()
        
        rates = {}
        ios_section = False
        android_section = False
        
        for row in data:
            if not row:
                continue
            
            # Определяем секции
            if len(row) > 0:
                first_cell = str(row[0]).strip().lower()
                
                if first_cell == 'ios':
                    ios_section = True
                    android_section = False
                    print("Найдена секция iOS")
                    continue
                elif first_cell == 'android':
                    android_section = True
                    ios_section = False
                    print("Найдена секция Android")
                    continue
                elif first_cell in ['adchampagne', 'факт', '']:
                    continue
                
                # Парсим источник и ставку
                source = first_cell
                
                # Ищем ставку (обычно в 3-4 колонке)
                rate = None
                for cell in row[1:5]:
                    try:
                        cell_str = str(cell).strip().replace(' ', '').replace(',', '').replace('\xa0', '')
                        if cell_str and cell_str.replace('.', '').isdigit():
                            rate = float(cell_str)
                            if rate > 100:  # Это похоже на ставку
                                break
                    except:
                        pass
                
                if rate and source and source not in ['total', 'налог']:
                    platform = 'ios' if ios_section else ('android' if android_section else None)
                    key = (source, platform)
                    rates[key] = rate
                    print(f"  {source} ({platform}): {rate} руб")
        
        print()
        print(f"Всего найдено ставок: {len(rates)}")
        return rates
        
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return {}

if __name__ == "__main__":
    rates = read_october_rates()
    
    if rates:
        print("\n" + "=" * 80)
        print("ИТОГО")
        print("=" * 80)
        print("\nСтавки успешно прочитаны:")
        for (source, platform), rate in sorted(rates.items()):
            plat = platform or 'all'
            print(f"  {source} ({plat}): {rate} руб")

