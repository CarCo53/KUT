# core/player/el_sirala.py
from log import logger

@logger.log_function
def el_sirala(oyuncu):
    """
    Oyuncunun elindeki taşları renk ve sayı sırasına göre sıralar.
    """
    oyuncu.el.sort(key=lambda t: (t.renk_sira, t.deger))