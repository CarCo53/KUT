# gui/buttons/yeni_oyun.py

from log import logger
# Hard Reset için gerekli sabit importlar (Dairesel içeri aktarma riski düşük olanlar)
import tkinter as tk 
from engine.game_manager import Game 
from gui.status import StatusBar 
from gui.layout._layout_olustur import _layout_olustur 

@logger.log_function
def yeni_oyun(arayuz):
    # Fonksiyon içinde import ederek dairesel bağımlılığı çözelim
    # Çünkü gui.buttons.__init__ bu dosyayı, bu dosya da gui.buttons'u import ediyor.
    from gui.buttons import ButtonManager 
    
    # --- HARD RESET İŞLEMLERİ BAŞLANGIÇ ---
    
    for widget in arayuz.pencere.winfo_children():
        widget.destroy()
    
    yeni_oyun_nesnesi = Game()
    yeni_oyun_nesnesi.arayuz = arayuz
    yeni_oyun_nesnesi.baslat() 

    arayuz.oyun = yeni_oyun_nesnesi
    
    # UI yöneticilerini ve temel durumları yeniden oluştur
    # Burada ButtonManager sınıfı artık fonksiyon içinde içeri aktarıldığı için sorun yaşanmaz.
    arayuz.statusbar = StatusBar(arayuz) 
    arayuz.button_manager = ButtonManager(arayuz) 
    arayuz.secili_tas_idler = []
    arayuz.alanlar = {}
    
    _layout_olustur(arayuz) 
    
    # --- HARD RESET İŞLEMLERİ SONU ---
    
    arayuz.arayuzu_guncelle()