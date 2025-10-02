from core.tile import Tile
from log import logger

from .olustur import olustur
from .karistir import karistir
from .tas_cek import tas_cek
from .tas_ekle import tas_ekle

class Deck:
    @logger.log_function
    def __init__(self):
        self.taslar = []

    def olustur(self):
        return olustur(self)

    def karistir(self):
        return karistir(self)

    def tas_cek(self):
        if self.taslar:
            return self.taslar.pop(0)
        return None

    def tas_ekle(self, tas):
        return tas_ekle(self, tas)

    def __len__(self):
        return len(self.taslar)