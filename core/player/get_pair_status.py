# core/player/get_pair_status.py
from collections import defaultdict
from log import logger

@logger.log_function
def get_pair_status(el):
    """
    Eldeki her taşı, bir çifte ait olup olmadığı bilgisiyle etiketler.
    Döndürülen: {tas_id: is_in_pair (bool)}
    """
    tas_gruplari = defaultdict(list)
    for tas in el:
        if tas.renk != 'joker':
            anahtar = (tas.renk, tas.deger)
            tas_gruplari[anahtar].append(tas)
            
    pair_tiles = set()
    
    # Gerçek çiftleri bul
    for tas_listesi in tas_gruplari.values():
        cift_sayisi = len(tas_listesi) // 2
        for i in range(cift_sayisi):
            # Bir çiftin iki elemanını da set'e ekle
            pair_tiles.add(tas_listesi[i*2].id)
            pair_tiles.add(tas_listesi[i*2+1].id)
            
    # Jokerler bu sıralamada hep tek kabul edilir.
    return {t.id: (t.id in pair_tiles) for t in el}