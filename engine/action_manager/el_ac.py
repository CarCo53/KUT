# engine/action_manager/el_ac.py
from log import logger
from rules.joker_manager import JokerManager
from engine.action_manager._eli_ac_ve_isle import _eli_ac_ve_isle
from core.game_state import GameState 

@logger.log_function
def el_ac(game, oyuncu_index, tas_id_list):
    oyuncu = game.oyuncular[oyuncu_index]
    secilen_taslar = [tas for tas in oyuncu.el if tas.id in tas_id_list]
    is_already_open = game.acilmis_oyuncular[oyuncu_index]
    
    # ---------------------------------------------------------------------
    # KRİTİK DÜZELTME: İlk el açılışının yapıldığı turda ikinci bir hamleyi engelle.
    # game.oyuncu_hamle_yapti bayrağı SADECE ilk el açılışında True yapılır ve taş atılana kadar True kalır.
    if game.oyuncu_hamle_yapti[oyuncu_index]:
         return {"status": "fail", "message": "El açma/işleme hamlesini yaptınız. Lütfen sırayı bitirmek için bir taş atın."}
    # ---------------------------------------------------------------------

    # El açmak için desteden veya yerden taş çekilmiş olmalı. (Genel kural)
    if not game.turda_tas_cekildi[oyuncu_index]:
         return {"status": "fail", "message": "El açmak için desteden/yerden taş çekmiş olmanız gerekir."}

    if any(t.renk == "joker" for t in secilen_taslar):
        
        joker_kontrol_sonucu = JokerManager.el_ac_joker_kontrolu(game, oyuncu, secilen_taslar)
        
        if joker_kontrol_sonucu["status"] == "joker_choice_needed":
            return joker_kontrol_sonucu
        if joker_kontrol_sonucu["status"] == "invalid_joker_move":
            return {"status": "fail", "message": "Jokerle geçersiz per açamazsınız."}
    
    return _eli_ac_ve_isle(game, oyuncu_index, secilen_taslar)