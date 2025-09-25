# gui/event_handlers/per_sec.py
from log import logger

@logger.log_function
def per_sec(arayuz, oyuncu_index, per_index):
    if len(arayuz.secili_tas_idler) != 1:
        arayuz.statusbar.guncelle("Joker almak veya işlemek için elinizden 1 taş seçmelisiniz.")
        return

    secili_tas_id = arayuz.secili_tas_idler[0]

    sonuc_joker = arayuz.oyun.joker_degistir(0, oyuncu_index, per_index, secili_tas_id)
    if sonuc_joker.get("status") == "success":
        arayuz.secili_tas_idler = []
        arayuz.statusbar.guncelle("Joker başarıyla alındı!")
        arayuz.arayuzu_guncelle()
        return

    sonuc_islem = arayuz.oyun.islem_yap(0, oyuncu_index, per_index, secili_tas_id)
    if sonuc_islem:
        arayuz.secili_tas_idler = []
        arayuz.statusbar.guncelle("Taş başarıyla işlendi!")
    else:
        hata_mesaji = sonuc_joker.get("message", "Geçersiz hamle!")
        arayuz.statusbar.guncelle(hata_mesaji)

    arayuz.arayuzu_guncelle()