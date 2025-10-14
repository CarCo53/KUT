# gui/buttons/__init__.py

import tkinter as tk
from core.game_state import GameState
from log import logger

# Ayırdığımız fonksiyonları import et
from gui.buttons.yerden_al import yerden_al
from gui.buttons.gec import gec
from gui.buttons.desteden_cek import desteden_cek
from gui.buttons.el_ac import el_ac
from gui.buttons.tas_at import tas_at
from gui.buttons.yeni_oyun import yeni_oyun
from gui.buttons.joker_al import joker_al # YENİ IMPORT

class ButtonManager:
    @logger.log_function
    def __init__(self, arayuz):
        self.arayuz = arayuz
        self.butonlar = {}

    def ekle_butonlar(self, parent):
        frame = tk.Frame(parent)
        frame.pack(pady=10)
        self.butonlar["yerden_al"] = tk.Button(frame, text="Yerden Al", command=self.yerden_al)
        self.butonlar["gec"] = tk.Button(frame, text="Geç", command=self.gec)
        self.butonlar["desteden_cek"] = tk.Button(frame, text="Desteden Çek", command=self.desteden_cek)
        self.butonlar["el_ac"] = tk.Button(frame, text="Elini Aç", command=self.el_ac)
        self.butonlar["tas_at"] = tk.Button(frame, text="Taş At", command=self.tas_at)
        self.butonlar["joker_al"] = tk.Button(frame, text="Joker Al", command=self.joker_al) # YENİ BUTON
        self.butonlar["yeni_oyun"] = tk.Button(frame, text="Yeni Oyun", command=self.yeni_oyun)
        
        for btn in self.butonlar.values():
            btn.pack(side=tk.LEFT, padx=8)

    
    def butonlari_guncelle(self, oyun_durumu):
        for btn in self.butonlar.values():
            btn.config(state=tk.DISABLED)
        
        if oyun_durumu == GameState.BITIS:
             self.butonlar["yeni_oyun"].config(state=tk.NORMAL)
             return
             
        oyun = self.arayuz.oyun
        sira_bende = oyun.sira_kimde_index == 0
        
        if oyun_durumu == GameState.ILK_TUR and sira_bende:
            self.butonlar["tas_at"].config(state=tk.NORMAL)
        elif oyun_durumu == GameState.NORMAL_TUR and sira_bende:
            self.butonlar["el_ac"].config(state=tk.NORMAL)
            self.butonlar["desteden_cek"].config(state=tk.NORMAL)
            # Eğer masada joker varsa, alım butonu aktif edilmeli
            if oyun.acik_joker_temsilcileri: 
                 self.butonlar["joker_al"].config(state=tk.NORMAL)
                 
        elif oyun_durumu == GameState.NORMAL_TAS_ATMA and sira_bende:
            self.butonlar["tas_at"].config(state=tk.NORMAL)
            self.butonlar["el_ac"].config(state=tk.NORMAL)
            # Eğer masada joker varsa, alım butonu aktif edilmeli
            if oyun.acik_joker_temsilcileri: 
                 self.butonlar["joker_al"].config(state=tk.NORMAL)
                 
        elif oyun_durumu == GameState.ATILAN_TAS_DEGERLENDIRME:
            degerlendiren_ben_miyim = oyun.atilan_tas_degerlendirici and oyun.atilan_tas_degerlendirici.siradaki() == 0
            if degerlendiren_ben_miyim:
                self.butonlar["yerden_al"].config(state=tk.NORMAL)
                self.butonlar["gec"].config(state=tk.NORMAL)

    def yerden_al(self):
        yerden_al(self.arayuz)

    @logger.log_function
    def gec(self):
        gec(self.arayuz)

    @logger.log_function
    def desteden_cek(self):
        desteden_cek(self.arayuz)

    @logger.log_function
    def el_ac(self):
        el_ac(self.arayuz)

    @logger.log_function
    def tas_at(self):
        tas_at(self.arayuz)
        
    # EKSİK OLAN VE ŞİMDİ EKLENEN METOT:
    @logger.log_function
    def joker_al(self):
        joker_al(self.arayuz) 

    @logger.log_function
    def yeni_oyun(self):
        yeni_oyun(self.arayuz)