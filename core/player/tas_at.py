# core/player/tas_at.py
from log import logger

@logger.log_function
def tas_at(oyuncu, tas_id):
    """
    Oyuncunun elinden belirtilen ID'deki taşı atar ve döndürür.
    Taş bulunamazsa None döndürür.
    """
    atilan_tas = next((t for t in oyuncu.el if t.id == tas_id), None)
    if atilan_tas:
        oyuncu.el.remove(atilan_tas)
        oyuncu.el_sirala()
        return atilan_tas
    return None