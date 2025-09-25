# core/deck/tas_cek.py
from log import logger

@logger.log_function
def tas_cek(deste):
    """
    Desteden en üstteki taşı çeker ve döndürür.
    Deste boşsa None döndürür.
    """
    if deste.taslar:
        return deste.taslar.pop(0)
    return None