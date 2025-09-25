# core/player/tas_at.py
from log import logger
from .el_sirala import el_sirala 

@logger.log_function
def tas_at(oyuncu, tas_id):
    """
    Oyuncunun elinden belirtilen ID'deki taşı atar ve döndürür.
    Taş bulunamazsa None döndürür.
    """
    atilan_tas = next((t for t in oyuncu.el if t.id == tas_id), None)
    if atilan_tas:
        oyuncu.el.remove(atilan_tas)
        # is_cift_gorevi parametresini geçir
        el_sirala(oyuncu, is_cift_gorevi=oyuncu.is_cift_gorevi)
        return atilan_tas
    return None