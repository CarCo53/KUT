# log_simplifier.py
import re
import os
from datetime import datetime

# Oyun loglarının bulunduğu varsayılan dosya adı
LOG_FILE_NAME = 'game.log'

def simplify_log_file(input_filepath):
    """
    Verilen log dosyasını okur, gereksiz logları (CALL/RETURN) temizler
    ve sadece oyuncuyu ilgilendiren önemli olayları döndürür.
    """
    if not os.path.exists(input_filepath):
        return f"HATA: '{input_filepath}' dosyası bulunamadı."

    simplified_lines = []
    
    # Log dosyasını UTF-8 ile açmayı deneyelim
    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return f"HATA: Dosya okuma hatası: {e}"

    
    for line in lines:
        # Örnek Log Formatı: [2025-10-08 09:39:09] INFO: CALL main
        
        # 1. Tarih ve INFO/ERROR kısmını temizle
        match = re.search(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (INFO|ERROR|Kural İhlali Engellendi|AI): (.*)', line)
        if not match:
            # Format dışı çizgileri atla
            continue

        timestamp_str, level, message = match.groups()
        
        # 2. CALL ve RETURN loglarını filtrele (Bunlar sadece debug/tracing içindir)
        if message.startswith("CALL ") or message.startswith("RETURN "):
            continue
        
        # 3. Kural İhlali veya AI aksiyonu gibi önemli mesajları sadeleştir
        
        # AI mesajlarını sadeleştir
        if message.startswith("AI AI Oyuncu"):
            # Örn: AI AI Oyuncu 3 atılan taşı değerlendiriyor. Almadı.
            message = re.sub(r'AI AI Oyuncu (\d+)\s?', r'Oyuncu \1, ', message)
        
        # Kural İhlali mesajlarını sadeleştir
        elif message.startswith("Kural İhlali Engellendi"):
            # Örn: Kural İhlali Engellendi: Joker (105) açılmış pere işlenemez.
            pass
        
        # Diğer önemli olaylar: Yeni tura geçildi, Taş atıldı, Taşı alıyor vb.
        
        # Sadece zaman, seviye ve sadeleştirilmiş mesajı ekle
        
        # Zamanı daha kısa bir formata dönüştür (HH:MM:SS)
        try:
            time_only = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
        except ValueError:
            time_only = "??:??:??" # Zaman formatı hatalıysa
            
        simplified_lines.append(f"[{time_only}] {message.strip()}")

    return "\n".join(simplified_lines)


if __name__ == '__main__':
    # Script çalıştırıldığında sadeleştirilmiş logu doğrudan konsola basar.
    
    # Eğer 'game.log' ana dizinde değilse, yolu ayarlayın.
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), LOG_FILE_NAME)
    
    # Eğer okey-main - Kopya klasöründeyse, yolu şöyle ayarlayın:
    # log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), LOG_FILE_NAME) 

    simplified_log = simplify_log_file(LOG_FILE_NAME)
    
    print("--- OYUN GEÇMİŞİ (SADELEŞTİRİLMİŞ) ---")
    print(simplified_log)
    print("--- SON ---")