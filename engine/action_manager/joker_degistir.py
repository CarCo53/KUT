# engine/action_manager/joker_degistir.py

from log import logger
from rules.rules_manager import Rules

@logger.log_function
def joker_degistir(game, degistiren_oyuncu_idx, per_sahibi_idx, per_idx, tas_id):
    if not game.acilmis_oyuncular[degistiren_oyuncu_idx]:
        return {"status": "fail", "message": "Elini açmadan joker alamazsınız."}
    
    el_acan_tur = game.ilk_el_acan_tur.get(degistiren_oyuncu_idx)
    if el_acan_tur is not None and game.tur_numarasi <= el_acan_tur:
        return {"status": "fail", "message": "El açtığınız turda joker alamazsınız."}

    oyuncu = game.oyuncular[degistiren_oyuncu_idx]
    degistirilecek_tas = next((t for t in oyuncu.el if t.id == tas_id), None)
    if not degistirilecek_tas:
        return {"status": "fail", "message": "Taş bulunamadı."}

    per = game.acilan_perler[per_sahibi_idx][per_idx]
    
    for i, per_tasi in enumerate(per):
        if per_tasi.renk == "joker" and per_tasi.joker_yerine_gecen:
            yerine_gecen = per_tasi.joker_yerine_gecen
            
            # Değiştirme kontrolü: SERİ/KÜT'te tam eşleşme VEYA ÇİFT'te sembolik alım
            is_valid_swap = False
            if yerine_gecen.renk == degistirilecek_tas.renk and yerine_gecen.deger == degistirilecek_tas.deger:
                 is_valid_swap = True
            elif yerine_gecen.renk == "joker" and degistirilecek_tas.renk != "joker":
                 is_valid_swap = True 
            
            if is_valid_swap:
                
                joker = per.pop(i)
                
                # KRİTİK DÜZELTME: Global temsilciyi listeden KALDIR (Senkronizasyonun Anahtarı)
                # Bu, Joker'in geri alındığında Okey Taşı 2'nin tekrar '?' olmasına neden olur.
                if yerine_gecen in game.acik_joker_temsilcileri:
                    game.acik_joker_temsilcileri.remove(yerine_gecen)
                
                joker.joker_yerine_gecen = None
                
                oyuncu.tas_al(joker)
                oyuncu.tas_at(tas_id)
                
                per.append(degistirilecek_tas)
                
                oyuncu.el_sirala()
                game._per_sirala(per)
                return {"status": "success"}
                
    # KRİTİK HATA MESAJI DÜZELTMESİ
    temsil_edilenler = []
    for t in per:
        if t.renk == "joker" and t.joker_yerine_gecen:
            yerine_gecen = t.joker_yerine_gecen
            if yerine_gecen.renk == "joker":
                 temsil_edilenler.append("Çift Jokeri")
            else:
                 temsil_edilenler.append(f"{yerine_gecen.renk.capitalize()} {yerine_gecen.deger}")

    if temsil_edilenler:
        hata_mesaji = f"Seçilen taş masadaki jokerin temsil ettiği taşla ({', '.join(temsil_edilenler)}) eşleşmiyor."
    else:
        hata_mesaji = "Geçersiz joker değiştirme hamlesi. Seçili per'de alınabilir joker yok."
            
    return {"status": "fail", "message": hata_mesaji}