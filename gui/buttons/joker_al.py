# gui/buttons/joker_al.py
from log import logger
from core.game_state import GameState

@logger.log_function
def joker_al(arayuz):
    oyun = arayuz.oyun
    
    if oyun.sira_kimde_index != 0:
        arayuz.statusbar.guncelle("Joker almak için sıranızın gelmesini beklemelisiniz.")
        return

    # Kural: Joker değişimi, desteden/yerden taş çekildikten sonra yapılır.
    if oyun.oyun_durumu != GameState.NORMAL_TAS_ATMA:
        arayuz.statusbar.guncelle("Joker değiştirmek için desteden/yerden taş çekmiş olmalısınız.")
        return
        
    if not oyun.acik_joker_temsilcileri:
         arayuz.statusbar.guncelle("Masada alınabilecek açık joker yok.")
         return

    # Oyuncunun elindeki seçili taşı al (joker alma eylemi tek bir taşla yapılır)
    if len(arayuz.secili_tas_idler) != 1:
        arayuz.statusbar.guncelle("Joker almak için elinizden bir taş seçmelisiniz.")
        return
    
    # Seçili taşın bilgileri
    secili_tas_id = arayuz.secili_tas_idler[0]
    secili_tas = next((t for t in oyun.oyuncular[0].el if t.id == secili_tas_id), None)
    
    if not secili_tas:
        arayuz.statusbar.guncelle("Seçilen taş elinizde bulunamadı.")
        return

    # 1. Seçilen taşın temsil ettiği jokeri masada ara
    temsilci_tas = None
    for t in oyun.acik_joker_temsilcileri:
        if t.renk == secili_tas.renk and t.deger == secili_tas.deger:
            temsilci_tas = t
            break

    if not temsilci_tas:
        arayuz.statusbar.guncelle(f"Seçtiğiniz {secili_tas.renk.capitalize()} {secili_tas.deger} masadaki açık jokerin temsil ettiği taşla eşleşmiyor.")
        return

    # 2. Global Joker Değiştirme işlemini başlat
    # NOT: joker_degistir_global fonskiyonu, per içindeki jokeri bulma, takas etme ve 
    # acik_joker_temsilcileri listesinden silme işlemlerini zaten yapıyor.
    sonuc = oyun.joker_degistir_global(0, temsilci_tas)

    if sonuc.get("status") == "success":
        arayuz.secili_tas_idler = []
        arayuz.statusbar.guncelle(sonuc["message"])
    else:
        arayuz.statusbar.guncelle(sonuc.get("message", "Joker alma işleminde bilinmeyen bir hata oluştu."))
        
    arayuz.arayuzu_guncelle()