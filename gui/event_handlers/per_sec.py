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
    joker_hata_mesaji = sonuc_joker.get("message", "Geçersiz hamle! (Joker denemesi)")
    
    sonuc_islem = arayuz.oyun.islem_yap(0, oyuncu_index, per_index, secili_tas_id)
    
    if sonuc_islem:
        arayuz.secili_tas_idler = []
        arayuz.statusbar.guncelle("Taş başarıyla işlendi!")
    else:
        # Hem Joker hem de İşleme başarısız olduysa.
        
        # Joker alma hatası ve İşleme hatasının en genel nedeni olan kural dışılığı yansıtan mesaj:
        hata_mesaji = "Joker alma ve İşleme başarısız. Taşınız Joker'in temsil ettiği taşla eşleşmiyor ve per'e uymuyor."
        
        # Eğer motorun döndürdüğü özel kısıtlama mesajı varsa (örneğin aynı turda birden fazla ana hamle)
        if isinstance(sonuc_islem, dict) and sonuc_islem.get("status") == "fail":
             hata_mesaji = sonuc_islem.get("message", hata_mesaji)

        arayuz.statusbar.guncelle(hata_mesaji)

    arayuz.arayuzu_guncelle()