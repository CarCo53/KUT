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
            if yerine_gecen.renk == degistirilecek_tas.renk and yerine_gecen.deger == degistirilecek_tas.deger:
                joker = per.pop(i)
                joker.joker_yerine_gecen = None
                
                oyuncu.tas_al(joker)
                oyuncu.tas_at(tas_id)
                
                per.append(degistirilecek_tas)
                
                oyuncu.el_sirala()
                game._per_sirala(per)
                return {"status": "success"}
                
    return {"status": "fail", "message": "Geçersiz joker değiştirme hamlesi."}