# ai/strategies/islem_stratejisi/islem_yap_dene.py
from log import logger
from rules.rules_manager import Rules

@logger.log_function
def islem_yap_dene(ai_player, game):
    if not game.acilmis_oyuncular[ai_player.index]: return None
    if game.ilk_el_acan_tur.get(ai_player.index, -1) >= game.tur_numarasi: return None

    # 1. Joker Değiştirme (SADECE GLOBAL YAKLAŞIM) - Yüksek Öncelik
    for temsilci_tas in game.acik_joker_temsilcileri:
        # Oyuncunun elinde bu temsili taşı var mı?
        eslesen_tas = next((t for t in ai_player.el if t.renk == temsilci_tas.renk and t.deger == temsilci_tas.deger), None)
        
        # Eğer oyuncu bu taşı tutuyorsa, bu Joker'i alabilir.
        if eslesen_tas:
            # AI'a, bu temsilci taş üzerinden global değişim yapması gerektiğini bildir
            return {"action_type": "joker_degistir_global", "temsilci_tas": temsilci_tas, "tas_id": eslesen_tas.id}
    
    # 2. İşleme Yapma (Orijinal Mantık)
    for tas in ai_player.el:
        # Kural: Joker, el açma/oyun bitirme dışında işleme yapılamaz.
        if tas.renk == "joker":
            continue 
        
        for per_sahibi_idx, perler in game.acilan_perler.items():
            for per_idx, per in enumerate(perler):
                if Rules.islem_dogrula(per, tas):
                    return {"action_type": "islem_yap", "sahip_idx": per_sahibi_idx, "per_idx": per_idx, "tas_id": tas.id}
    
    return None