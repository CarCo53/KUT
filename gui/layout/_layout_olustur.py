# gui/layout/_layout_olustur.py
import tkinter as tk
from log import logger
from ._oyuncu_alani_olustur import _oyuncu_alani_olustur

@logger.log_function
def _layout_olustur(arayuz):
    arayuz.statusbar.ekle_status_label(arayuz.pencere)
    oyuncu_cercevesi = tk.Frame(arayuz.pencere)
    oyuncu_cercevesi.pack(pady=5, fill="x")
    arayuz.alanlar['oyuncu_1'] = _oyuncu_alani_olustur(oyuncu_cercevesi, "Oyuncu 1 (Siz)")
    arayuz.alanlar['oyuncu_2'] = _oyuncu_alani_olustur(oyuncu_cercevesi, "AI Oyuncu 2")
    arayuz.alanlar['oyuncu_3'] = _oyuncu_alani_olustur(oyuncu_cercevesi, "AI Oyuncu 3")
    arayuz.alanlar['oyuncu_4'] = _oyuncu_alani_olustur(oyuncu_cercevesi, "AI Oyuncu 4")
    arayuz.masa_frame = tk.LabelFrame(arayuz.pencere, text="Masa (Açılan Perler)", padx=10, pady=10)
    arayuz.masa_frame.pack(pady=10, fill="both", expand=True)

    deste_ve_atilan_cerceve = tk.Frame(arayuz.pencere)
    deste_ve_atilan_cerceve.pack(pady=5)
    
    arayuz.joker_gosterim_frame = tk.LabelFrame(deste_ve_atilan_cerceve, text="Okey Taşı", padx=5, pady=5)
    arayuz.joker_gosterim_frame.pack(side=tk.LEFT, padx=10)

    joker_temsil_frame = tk.Frame(arayuz.joker_gosterim_frame)
    joker_temsil_frame.pack()
    arayuz.okey_tasi_label = tk.Label(joker_temsil_frame, borderwidth=4, relief="solid")
    arayuz.okey_tasi_label.pack(side=tk.LEFT)
    arayuz.ok_label = tk.Label(joker_temsil_frame, text="=>", font=("Arial", 16, "bold"))
    arayuz.ok_label.pack(side=tk.LEFT, padx=5)
    arayuz.okey_temsilci_label = tk.Label(joker_temsil_frame)
    arayuz.okey_temsilci_label.pack(side=tk.LEFT)

    arayuz.deste_frame = tk.LabelFrame(deste_ve_atilan_cerceve, text="Deste", padx=5, pady=5)
    arayuz.deste_frame.pack(side=tk.LEFT, padx=10)
    arayuz.atilan_frame = tk.LabelFrame(deste_ve_atilan_cerceve, text="Atılan Taşlar", padx=5, pady=5)
    arayuz.atilan_frame.pack(side=tk.LEFT, padx=10)
    arayuz.deste_sayisi_label = tk.Label(arayuz.deste_frame, text="", font=("Arial", 12, "bold"))
    arayuz.deste_sayisi_label.pack(side=tk.TOP, pady=2)
    arayuz.button_manager.ekle_butonlar(arayuz.pencere)