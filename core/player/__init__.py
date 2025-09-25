# core/player/__init__.py
from core.tile import Tile
from log import logger

# Ayırdığımız fonksiyonları aynı paketten içe aktar
from .tas_al import tas_al
from .tas_at import tas_at
from .el_sirala import el_sirala

class Player:
    @logger.log_function
    def __init__(self, isim, index):
        self.isim = isim
        self.el = []
        self.index = index
        self.acilmis_perler = []
    
    # Eski metotları yeni fonksiyonlara çağrı yapacak şekilde yeniden yazın
    def tas_al(self, tas: Tile):
        tas_al(self, tas)

    def tas_at(self, tas_id):
        return tas_at(self, tas_id)

    def el_sirala(self):
        el_sirala(self)