# core/deck/olustur.py
from core.tile import Tile
from log import logger

@logger.log_function
def olustur(deste):
    """
    Oyunda kullanılacak 106 adet taşı (4 renk x 13 sayı x 2 adet + 2 joker) oluşturur.
    """
    deste.taslar = []
    renkler = ["sari", "mavi", "siyah", "kirmizi"]
    for renk in renkler:
        for deger in range(1, 14):
            deste.taslar.append(Tile(renk, deger, f"{renk}_{deger}.png"))
            deste.taslar.append(Tile(renk, deger, f"{renk}_{deger}.png"))
    deste.taslar.append(Tile("joker", 0, "joker.png"))
    deste.taslar.append(Tile("joker", 0, "joker.png"))