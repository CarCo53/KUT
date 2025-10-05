# engine/action_manager/el_ac.py
from log import logger
from rules.joker_manager import JokerManager
from engine.action_manager._eli_ac_ve_isle import _eli_ac_ve_isle

@logger.log_function
def el_ac(game, oyuncu_index, tas_id_list):
    oyuncu = game.oyuncular[oyuncu_index]
    secilen_taslar = [tas for tas in oyuncu.el if tas.id in tas_id_list]
    
    if any(t.renk == "joker" for t in secilen_taslar):
        
        joker_kontrol_sonucu = JokerManager.el_ac_joker_kontrolu(game, oyuncu, secilen_taslar)
        
        if joker_kontrol_sonucu["status"] == "joker_choice_needed":
            return joker_kontrol_sonucu
        if joker_kontrol_sonucu["status"] == "invalid_joker_move":
            return {"status": "fail", "message": "Jokerle geçersiz per açamazsınız."}
    
    return _eli_ac_ve_isle(game, oyuncu_index, secilen_taslar)