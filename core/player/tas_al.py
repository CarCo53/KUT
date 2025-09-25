# core/player/tas_al.py
from log import logger
from core.tile import Tile
from .el_sirala import el_sirala 

@logger.log_function
def tas_al(oyuncu, tas: Tile):
    """
    Oyuncunun eline bir taş ekler ve elini sıralar.
    """
    oyuncu.el.append(tas)
    # is_cift_gorevi parametresini geçir
    el_sirala(oyuncu, is_cift_gorevi=oyuncu.is_cift_gorevi)