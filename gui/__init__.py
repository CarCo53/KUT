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
    # HATA DÜZELTİLDİ: Sadece 'oyun' argümanı almalı. tk.Tk() içeride yaratılmalı.
    def __init__(self, oyun: Game):
        self.oyun = oyun
        self.oyun.arayuz = self
        self.pencere = tk.Tk()
        self.pencere.title("Okey Oyunu")
        self.pencere.geometry("1600x1000+0+0")
        self.visuals = Visuals()
        self.visuals.yukle()
        
        # Bu nesneler yeni oyun butonunda tekrar oluşturulur.
        self.statusbar = StatusBar(self)
        self.button_manager = ButtonManager(self)
        
        self.secili_tas_idler = []
        self.alanlar = {}
        # NOTE: _layout_olustur, yeni iki joker etiketlerini (okey_tasi_label_1, vb.) burada tanımlar.
        self._layout_olustur() 
        self.arayuzu_guncelle()

    @logger.log_function
    def _layout_olustur(self):
        # Bu, layout dosyasından çağrılan dış fonksiyonu sarmalar.
        return _layout_olustur(self)
    
    @logger.log_function
    def arayuzu_guncelle(self):
        # KRİTİK JOKER/OKEY TAŞI GÖSTERİMİ
        # Sadece masada açılmış Jokerlerin temsil ettiği taşları Game objesinden alıyoruz. 
        temsilciler = self.oyun.acik_joker_temsilcileri
        joker_gorseli = self.visuals.tas_resimleri.get("joker.png")
        
        self._guncelle_joker_alani(1, joker_gorseli, temsilciler, 0)
        self._guncelle_joker_alani(2, joker_gorseli, temsilciler, 1)

        # UI'ın geri kalanını güncellemek için ayrı fonksiyona devret
        return arayuzu_guncelle(self)

    @logger.log_function       
    def _guncelle_joker_alani(self, index, joker_gorseli, temsilciler, temsilci_index):
        # UI öğelerini dinamik olarak bul
        joker_label = getattr(self, f"okey_tasi_label_{index}")
        ok_label = getattr(self, f"ok_label_{index}")
        temsilci_label = getattr(self, f"okey_temsilci_label_{index}")

        # 1. Joker görselini sabit olarak göster
        if joker_gorseli:
            joker_label.config(image=joker_gorseli, text="", borderwidth=4, relief="solid")
            joker_label.image = joker_gorseli
        else:
            joker_label.config(image=None, text="Joker", borderwidth=4, relief="solid")
            
        # 2. Temsilci bilgisini göster
        if temsilci_index < len(temsilciler):
            temsilci_tas = temsilciler[temsilci_index]
            temsilci_gorseli = self.visuals.tas_resimleri.get(temsilci_tas.imaj_adi)
            
            ok_label.config(text="=>", font=("Arial", 16, "bold"))
            temsilci_label.config(image=temsilci_gorseli, text="", borderwidth=0)
            temsilci_label.image = temsilci_gorseli
            
            # Tıklama olayı KALDIRILDI ve Unbind çağrısı kaldırıldı.
            temsilci_label.unbind("<Button-1>") 
        else:
            # YENİ OYUN BAŞLANGICINDA/JOKER DEĞİŞTİRİLDİĞİNDE GÖRSELİ SIFIRLAMA
            ok_label.config(text="") 
            # Güvenilir Sıfırlama
            temsilci_label.config(image=None, text="?", font=("Arial", 14)) 
            temsilci_label.image = None
            temsilci_label.unbind("<Button-1>")
            
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