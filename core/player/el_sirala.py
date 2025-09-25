# core/player/el_sirala.py
from log import logger
from .get_pair_status import get_pair_status

@logger.log_function
def el_sirala(oyuncu, is_cift_gorevi=False):
    """
    Oyuncunun elindeki taşları sıralar.
    is_cift_gorevi=True ise, çift olan taşları teklerden sonra sıralar (Tekler önde).
    """
    
    if is_cift_gorevi:
        # 1. Eldeki taşların çift durumunu hesapla
        pair_status = get_pair_status(oyuncu.el)
        
        # 2. Sıralama anahtarı oluştur:
        # a. is_in_pair: False (tek) = 0, True (çift) = 1. Tekler önde olmalı.
        # b. renk_sira: Varsayılan sıralama.
        # c. deger: Varsayılan sıralama.
        oyuncu.el.sort(key=lambda t: (
            1 if pair_status.get(t.id, False) else 0, # Çiftler (1) en sona gitsin.
            t.renk_sira,                              # 2. Kriter: Renk
            t.deger                                   # 3. Kriter: Değer
        ))
    else:
        # Varsayılan sıralama (renk ve değer)
        oyuncu.el.sort(key=lambda t: (t.renk_sira, t.deger))