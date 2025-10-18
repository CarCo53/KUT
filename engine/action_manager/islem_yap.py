# engine/action_manager/islem_yap.py
from log import logger
from core.game_state import GameState
from rules.rules_manager import Rules

@logger.log_function
def islem_yap(game, isleyen_oyuncu_idx, per_sahibi_idx, per_idx, tas_id):
    
    # ----------------------------------------------------------------------------------
    # KRİTİK DÜZELTME: İlk el açılışının yapıldığı turda (oyuncu_hamle_yapti=True ise)
    # tekrar işleme hamlesini engelle.
    if game.oyuncu_hamle_yapti[isleyen_oyuncu_idx]:
        return {"status": "fail", "message": "El açma/işleme hamlesini yaptınız. Lütfen sırayı bitirmek için bir taş atın."}
    # ----------------------------------------------------------------------------------
    
    # Sadece eli açmış ve sırası olan oyuncu işlem yapabilir.
    if not game.acilmis_oyuncular[isleyen_oyuncu_idx] or isleyen_oyuncu_idx != game.sira_kimde_index:
        return {"status": "fail", "message": "İşleme yapmak için elinizi açmış olmalı ve sıra sizde olmalıdır."}
        
    oyuncu = game.oyuncular[isleyen_oyuncu_idx]
    tas = next((t for t in oyuncu.el if t.id == tas_id), None)
    if not tas: return False # Bu noktada hala False döndürmek mantıklı, hata kontrolü motor içinde değilse
    
    per = game.acilan_perler[per_sahibi_idx][per_idx]
    
    if Rules.islem_dogrula(per, tas):
        oyuncu.tas_at(tas.id)
        per.append(tas)
        game._per_sirala(per)
        
        # Bu noktada game.oyuncu_hamle_yapti = True ayarlaması YAPILMAZ.
        # Çünkü oyuncu ya ilk açılış turundadır (ve zaten True olmuştur) ya da sonraki turlarda sınırsız hakkı vardır (False kalmalıdır).
        
        game.oyun_durumu = GameState.NORMAL_TAS_ATMA
        if not oyuncu.el:
            game.oyun_durumu = GameState.BITIS
            game.kazanan_index = isleyen_oyuncu_idx
        return True
    return False