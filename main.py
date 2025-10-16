# main.py

import sys
import os
import argparse
import glob
from engine.game_manager import Game
from gui import Arayuz
from rules.gorevler import GOREV_LISTESI
from log import logger

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def get_next_log_file_name():
    log_files = glob.glob("game*.log")
    if not log_files:
        return "game0001.log"
    
    log_numbers = []
    for f in log_files:
        try:
            log_numbers.append(int(f[4:8]))
        except ValueError:
            continue
    
    if not log_numbers:
        return "game0001.log"

    next_number = max(log_numbers) + 1
    return f"game{next_number:04d}.log"

@logger.log_function
def main():
    parser = argparse.ArgumentParser(description="Okey Oyunu")
    parser.add_argument("-gorev", type=str, choices=GOREV_LISTESI, help="Oyunun başlayacağı özel görevi belirler.")
    args = parser.parse_args()
    
    # KRİTİK LOG DÜZELTMESİ: Dinamik log dosyasını ayarla
    log_file_name = get_next_log_file_name()
    # Log dosyasının mode='w' (üzerine yazma) ayarı log.py'de kaldığı için, 
    # her seferinde yeni bir dosya adı atamak bu sorunu çözer.
    logger.logger.handlers[1].baseFilename = os.path.abspath(log_file_name)

    oyun = Game()
    oyun.baslat(args.gorev)
    gui = Arayuz(oyun)
    gui.baslat()

if __name__ == "__main__":
    main()