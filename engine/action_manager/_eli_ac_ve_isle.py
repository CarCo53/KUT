# engine/action_manager/_eli_ac_ve_isle.py

from log import logger
from core.game_state import GameState
from rules.rules_manager import Rules

@logger.log_function
def _eli_ac_ve_isle(game, oyuncu_index, secilen_taslar):
    oyuncu = game.oyuncular[oyuncu_index]
    is_ilk_acilis = not game.acilmis_oyuncular[oyuncu_index]
    dogrulama_sonucu = False
    
    # İlk el açılışına özel kurallar
    if is_ilk_acilis:
        # "Çift" görevi için özel kontrol
        if game.mevcut_gorev == "Çift" and len(secilen_taslar) != 8:
            return {"status": "fail", "message": "Çift görevi için tam olarak 8 taş (4 çift) açmalısınız."}
        dogrulama_sonucu = Rules.per_dogrula(secilen_taslar, game.mevcut_gorev)
    else:
        # Eli zaten açık oyuncular için genel per doğrulama
        dogrulama_sonucu = Rules.genel_per_dogrula(secilen_taslar)

    if dogrulama_sonucu:
        if is_ilk_acilis:
            game.acilmis_oyuncular[oyuncu_index] = True
            game.ilk_el_acan_tur[oyuncu_index] = game.tur_numarasi
            
            # YENİ MANTIK: GÖREV BAŞARIYLA TAMAMLANDIĞINDA SIRALAMAYI NORMALE DÖNDÜR
            if game.mevcut_gorev == "Çift":
                oyuncu.is_cift_gorevi = False
        
        # Eğer karma per açma durumu varsa
        if isinstance(dogrulama_sonucu, tuple):
            for per in dogrulama_sonucu:
                for tas in per:
                    oyuncu.tas_at(tas.id)
                game._per_sirala(per)
                game.acilan_perler[oyuncu_index].append(list(per))
        else: 
            for tas in secilen_taslar:
                oyuncu.tas_at(tas.id)
            game._per_sirala(secilen_taslar)
            game.acilan_perler[oyuncu_index].append(secilen_taslar)

        # Yeni sıralama ayarı, el_sirala fonksiyonu içinde uygulanacak.
        oyuncu.el_sirala()
        game.oyun_durumu = GameState.NORMAL_TAS_ATMA
        return {"status": "success"}
    else:
        for tas in secilen_taslar:
            if tas.renk == 'joker': tas.joker_yerine_gecen = None
        return {"status": "fail", "message": "Geçersiz per."}