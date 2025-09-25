# core/deck/tas_ekle.py
import random
from log import logger

@logger.log_function
def tas_ekle(deste, tas):
    """
    Desteden bir taş ekler ve desteyi karıştırır.
    """
    deste.taslar.append(tas)
    random.shuffle(deste.taslar)