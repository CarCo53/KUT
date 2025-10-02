# gui/event_handlers/per_sec.py

from log import logger

@logger.log_function
def per_sec(arayuz, oyuncu_index, per_index):
    if len(arayuz.secili_tas_idler) != 1:
        arayuz.statusbar.guncelle("Joker almak veya işlemek için elinizden 1 taş seçmelisiniz.")
        return

    secili_tas_id = arayuz.secili_tas_idler[0]
    
    # Adım 1: Joker Değiştirme denemesi yapılır.
    sonuc_joker = arayuz.oyun.joker_degistir(0, oyuncu_index, per_index, secili_tas_id)
    
    if sonuc_joker.get("status") == "success":
        arayuz.secili_tas_idler = []
        arayuz.statusbar.guncelle("Joker başarıyla alındı!")
        arayuz.arayuzu_guncelle()
        return

    # Adım 2: Joker değiştirme BAŞARISIZ olursa, İşleme Yapma denemesi yapılır.
    # Joker'den gelen hata mesajı geçici olarak saklanır.
    joker_hata_mesaji = sonuc_joker.get("message", "Geçersiz hamle! (Joker denemesi)")
    
    sonuc_islem = arayuz.oyun.islem_yap(0, oyuncu_index, per_index, secili_tas_id)
    
    if sonuc_islem:
        arayuz.secili_tas_idler = []
        arayuz.statusbar.guncelle("Taş başarıyla işlendi!")
    else:
        # Hem Joker hem de İşleme başarısız olduysa, daha iyi bir hata mesajı gösterilir.
        # İşleme hatası mesajı her zaman daha öncelikli olmalıdır.
        if "Geçersiz per!" in str(sonuc_islem): # İşleme Yap'tan gelen spesifik hata kontrolü (varsa)
            hata_mesaji = "İşleme başarısız oldu. Seçilen taş per'e uygun değil veya Jokerle işleme yapamazsınız."
        elif "eşleşmiyor" in joker_hata_mesaji: 
            hata_mesaji = "Joker alma ve İşleme başarısız. Taşınız Joker'in temsil ettiği taşla eşleşmiyor ve per'e uymuyor."
        else:
             hata_mesaji = "Geçersiz hamle! (Seçilen per'e taş işlenemez veya joker alınamaz)"
        
        arayuz.statusbar.guncelle(hata_mesaji)

    arayuz.arayuzu_guncelle()