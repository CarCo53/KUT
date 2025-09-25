# gui/buttons/el_ac.py
from log import logger

@logger.log_function
def el_ac(arayuz):
    secili_idler = arayuz.secili_tas_idler
    if not secili_idler:
        arayuz.statusbar.guncelle("Lütfen açmak için taş seçin.")
        return
    sonuc = arayuz.oyun.el_ac(0, secili_idler)
    if sonuc.get("status") == "success":
        arayuz.secili_tas_idler = []
        arayuz.statusbar.guncelle("Per başarıyla açıldı!")
    elif sonuc.get("status") == "joker_choice_needed":
        arayuz.joker_secim_penceresi_ac(sonuc["options"], sonuc["joker"], sonuc["secilen_taslar"])
    else:
        arayuz.statusbar.guncelle(sonuc.get("message", "Geçersiz per!"))
    arayuz.arayuzu_guncelle()