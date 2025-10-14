# gui/event_handlers/per_sec.py

from log import logger

@logger.log_function
def per_sec(arayuz, oyuncu_index, per_index):
    if len(arayuz.secili_tas_idler) != 1:
        # Joker değiştirme mantığı kaldırıldı, sadece işleme yapmak kalıyor.
        arayuz.statusbar.guncelle("İşleme yapmak için elinizden 1 taş seçmelisiniz.")
        return

    secili_tas_id = arayuz.secili_tas_idler[0]
    
    sonuc_islem = arayuz.oyun.islem_yap(0, oyuncu_index, per_index, secili_tas_id)
    
    if sonuc_islem:
        arayuz.secili_tas_idler = []
        arayuz.statusbar.guncelle("Taş başarıyla işlendi!")
    else:
        # İşleme başarısız olduysa hata mesajı gösterilir.
        hata_mesaji = "İşleme başarısız oldu. Seçilen taş per'e uygun değil, per zaten dolu veya bu per'e işleme yapılamaz."
        arayuz.statusbar.guncelle(hata_mesaji)

    arayuz.arayuzu_guncelle()