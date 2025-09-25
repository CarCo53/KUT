# gui/__init__.py
import tkinter as tk
from gui.visuals import Visuals
from gui.buttons import ButtonManager
from gui.status import StatusBar
from engine.game_manager import Game
from log import logger

# Ayırdığımız fonksiyonları içe aktar
from .arayuzguncelle.arayuzu_guncelle import arayuzu_guncelle
from .layout._layout_olustur import _layout_olustur
from .layout._oyuncu_alani_olustur import _oyuncu_alani_olustur
from .event_handlers.tas_sec import tas_sec
from .event_handlers.per_sec import per_sec
from .event_handlers.joker_secim_penceresi_ac import joker_secim_penceresi_ac
from .event_handlers.joker_secildi import joker_secildi
from .game_loop.ai_oynat import ai_oynat

class Arayuz:
    @logger.log_function
    def __init__(self, oyun: Game):
        self.oyun = oyun
        self.oyun.arayuz = self
        self.pencere = tk.Tk()
        self.pencere.title("Okey Oyunu")
        self.pencere.geometry("1400x900")
        self.visuals = Visuals()
        self.visuals.yukle()
        self.statusbar = StatusBar(self)
        self.button_manager = ButtonManager(self)
        self.secili_tas_idler = []
        self.alanlar = {}
        self._layout_olustur() # Sınıf metodu yerine alttaki fonksiyon çağrılıyor
        self.arayuzu_guncelle()

    @logger.log_function
    def _layout_olustur(self):
        return _layout_olustur(self)
    
    @logger.log_function
    def arayuzu_guncelle(self):
        okey_tasi = self.oyun.deste.okey_tasi
        if okey_tasi:
            okey_gorseli = self.visuals.tas_resimleri.get("joker.png")
            temsilci_gorseli = self.visuals.tas_resimleri.get(okey_tasi.imaj_adi)
            self.okey_tasi_label.config(image=okey_gorseli)
            self.okey_tasi_label.image = okey_gorseli
            self.okey_temsilci_label.config(image=temsilci_gorseli)
            self.okey_temsilci_label.image = temsilci_gorseli
        else:
            self.okey_tasi_label.config(image=None, text="Joker", borderwidth=2, relief="groove")
            self.okey_temsilci_label.config(image=None, text="", borderwidth=0)
            self.ok_label.config(text="")
        return arayuzu_guncelle(self)
        
    @logger.log_function
    def tas_sec(self, tas_id):
        return tas_sec(self, tas_id)

    @logger.log_function
    def per_sec(self, oyuncu_index, per_index):
        return per_sec(self, oyuncu_index, per_index)

    @logger.log_function
    def joker_secim_penceresi_ac(self, secenekler, joker, secilen_taslar):
        return joker_secim_penceresi_ac(self, secenekler, joker, secilen_taslar)

    @logger.log_function
    def joker_secildi(self, secilen_deger, joker, secilen_taslar, pencere):
        return joker_secildi(self, secilen_deger, joker, secilen_taslar, pencere)

    def ai_oynat(self):
        return ai_oynat(self)
        
    @logger.log_function
    def baslat(self):
        self.pencere.mainloop()