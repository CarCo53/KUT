# core/player/__init__.py
from core.tile import Tile
from log import logger

# Ayırdığımız fonksiyonları içe aktar
from .tas_al import tas_al
from .tas_at import tas_at
from .el_sirala import el_sirala
# Yeni fonksiyonu import et
from .get_pair_status import get_pair_status 

class Player:
    @logger.log_function
    def __init__(self, isim, index):
        self.isim = isim
        self.el = []
        self.index = index
        self.acilmis_perler = []
        # YENİ EKLENEN BAYRAK: Çift görevinde olup olmadığını tutar
        self.is_cift_gorevi = False
    
    # ... (tas_al, tas_at metotları alt adımlarda güncellenir)
    def tas_al(self, tas: Tile):
        tas_al(self, tas)

    def tas_at(self, tas_id):
        return tas_at(self, tas_id)

    def el_sirala(self):
        # Bu fonksiyon, diğer fonksiyonlar tarafından çağrılmaya devam edecek
        el_sirala(self, is_cift_gorevi=self.is_cift_gorevi)