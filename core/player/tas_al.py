# core/player/tas_al.py
from log import logger
from core.tile import Tile

@logger.log_function
def tas_al(oyuncu, tas: Tile):
    """
    Oyuncunun eline bir taş ekler ve elini sıralar.
    """
    oyuncu.el.append(tas)
    oyuncu.el_sirala()