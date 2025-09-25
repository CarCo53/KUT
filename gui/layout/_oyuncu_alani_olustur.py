# gui/layout/_oyuncu_alani_olustur.py
import tkinter as tk
from log import logger

@logger.log_function
def _oyuncu_alani_olustur(parent, isim):
    frame = tk.LabelFrame(parent, text=isim, padx=5, pady=5)
    frame.pack(pady=2, fill="x")
    return frame