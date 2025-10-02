# ai/strategies/islem_stratejisi/islem_yap_dene.py
from log import logger
from rules.rules_manager import Rules

@logger.log_function
def islem_yap_dene(ai_player, game):
    if not game.acilmis_oyuncular[ai_player.index]: return None
    if game.ilk_el_acan_tur.get(ai_player.index, -1) >= game.tur_numarasi: return None

    # 1. Joker Değiştirme
    for per_sahibi_idx, perler in game.acilan_perler.items():
        for per_idx, per in enumerate(perler):
            joker_tasi = next((t for t in per if t.renk == "joker" and t.joker_yerine_gecen), None)
            if joker_tasi:
                yerine_gecen = joker_tasi.joker_yerine_gecen
                eslesen_tas = next((t for t in ai_player.el if t.renk == yerine_gecen.renk and t.deger == yerine_gecen.deger), None)
                if eslesen_tas:
                    return {"action_type": "joker_degistir", "sahip_idx": per_sahibi_idx, "per_idx": per_idx, "tas_id": eslesen_tas.id}
    
    # 2. İşleme Yapma
    for tas in ai_player.el:
        # Kural: Joker, el açma/oyun bitirme dışında işleme yapılamaz.
        if tas.renk == "joker":
            continue 
        
        for per_sahibi_idx, perler in game.acilan_perler.items():
            for per_idx, per in enumerate(perler):
                if Rules.islem_dogrula(per, tas):
                    return {"action_type": "islem_yap", "sahip_idx": per_sahibi_idx, "per_idx": per_idx, "tas_id": tas.id}
    
    return None