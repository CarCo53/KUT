# core/deck/karistir.py
import random
from log import logger

@logger.log_function
def karistir(deste):
    """
    Destedeki taşları rastgele karıştırır.
    """
    random.shuffle(deste.taslar)