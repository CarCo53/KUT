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

    # 2. Hangi per içinde olduğunu bul ve ActionManager.joker_degistir'i çağır.
    sonuc = None
    joker_bulundu = False
    
    for per_sahibi_idx, perler in oyun.acilan_perler.items():
        for per_idx, per in enumerate(perler):
            for i, per_tasi in enumerate(per):
                # Jokerin temsil ettiği taş, temsilci_tas ile tam olarak aynı Tile nesnesi mi?
                if per_tasi.renk == "joker" and per_tasi.joker_yerine_gecen == temsilci_tas:
                    
                    # Jokerin bulunduğu per ve sahibi bulundu, işlemi başlat.
                    # oyun.joker_degistir(degistiren_oyuncu_idx, per_sahibi_idx, per_idx, tas_id)
                    sonuc = oyun.joker_degistir(0, per_sahibi_idx, per_idx, secili_tas_id) 
                    joker_bulundu = True
                    break
            if joker_bulundu:
                break
        if joker_bulundu:
            break

    if joker_bulundu:
        if sonuc and sonuc.get("status") == "success":
            arayuz.secili_tas_idler = []
            # Başarı mesajı: joker_degistir'den gelirse onu kullan, yoksa genel mesajı kullan
            arayuz.statusbar.guncelle(sonuc.get("message", f"Joker başarıyla değiştirildi: {temsilci_tas.renk.capitalize()} {temsilci_tas.deger}!"))
        else:
            arayuz.statusbar.guncelle(sonuc.get("message", "Joker alma işleminde bilinmeyen bir hata oluştu."))
    else:
        # Bu duruma gelmemesi beklenir, çünkü temsilci_tas oyun.acik_joker_temsilcileri içinden bulundu.
        arayuz.statusbar.guncelle("Masada bu temsilciye sahip aktif bir joker bulunamadı.")


    # KRİTİK EKLENTİ: Joker başarıyla değiştirildiğinde arayüzü güncelle
    arayuz.arayuzu_guncelle()