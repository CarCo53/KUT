# gui/event_handlers/joker_secim_penceresi_ac.py
import tkinter as tk
from log import logger

@logger.log_function
def joker_secim_penceresi_ac(arayuz, secenekler, joker, secilen_taslar):
    secim_penceresi = tk.Toplevel(arayuz.pencere)
    secim_penceresi.title("Joker Seçimi")
    secim_penceresi.geometry("300x150")
    secim_penceresi.transient(arayuz.pencere)
    secim_penceresi.grab_set()
    tk.Label(secim_penceresi, text="Joker'i hangi taş yerine kullanmak istersiniz?").pack(pady=10)
    buttons_frame = tk.Frame(secim_penceresi)
    buttons_frame.pack(pady=10)
    for tas_secenek in secenekler:
        img = arayuz.visuals.tas_resimleri.get(tas_secenek.imaj_adi)
        if img:
            b = tk.Button(buttons_frame, image=img,
                          command=lambda s=tas_secenek: arayuz.joker_secildi(s, joker, secilen_taslar, secim_penceresi))
            b.pack(side=tk.LEFT, padx=5)