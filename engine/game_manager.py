# engine/game_manager.py

from core.deck import Deck
from core.player import Player
from ai.ai_player import AIPlayer
from core.game_state import GameState
from baslat import baslat_oyun
from rules.rules_manager import Rules
from engine.action_manager import ActionManager
from engine.turn_manager import TurnManager
from log import logger

class Game:
    @logger.log_function
    def __init__(self):
        self.oyuncular = [Player("Oyuncu 1 (Siz)", 0), AIPlayer("AI Oyuncu 2", 1), AIPlayer("AI Oyuncu 3", 2), AIPlayer("AI Oyuncu 4", 3)]
        self.deste = Deck()
        self.atilan_taslar = []
        self.sira_kimde_index = 0
        self.oyun_durumu = GameState.NORMAL_TUR
        self.acilan_perler = {i: [] for i in range(len(self.oyuncular))}
        self.turda_tas_cekildi = [False] * len(self.oyuncular)
        self.atilan_tas_degerlendirici = None
        self.acilmis_oyuncular = [False] * len(self.oyuncular)
        self.mevcut_gorev = None
        self.kazanan_index = None
        self.tur_numarasi = 1
        self.ilk_el_acan_tur = {}
        self.arayuz = None
        self.oyuncu_hamle_yapti = [False] * len(self.oyuncular)
        self.acik_joker_temsilcileri = [] # YENİ: Masada açılan jokerlerin temsil ettiği taşları tutar

    # YENİ METOT: Oyun akışını özel bir etiketle loglar
    def _log_game_flow(self, message):
        logger.info(f"[GAME_FLOW] {message}")

    @logger.log_function
    def baslat(self, gorev=None):
        self._log_game_flow(f"Oyun Başladı. Görev: {self.mevcut_gorev}")
        return baslat_oyun(self, gorev)
    
    @logger.log_function
    def el_ac(self, oyuncu_index, tas_id_list):
        return ActionManager.el_ac(self, oyuncu_index, tas_id_list)

    @logger.log_function
    def joker_degistir(self, degistiren_oyuncu_idx, per_sahibi_idx, per_idx, tas_id): # HATA DÜZELTMEK İÇİN EKLENDİ
        self._log_game_flow(f"Joker Değiştirme (Lokal): {self.oyuncular[degistiren_oyuncu_idx].isim} per {per_sahibi_idx}-{per_idx}'deki jokeri değiştiriyor.")
        return ActionManager.joker_degistir(self, degistiren_oyuncu_idx, per_sahibi_idx, per_idx, tas_id)
        
    @logger.log_function
    def islem_yap(self, isleyen_oyuncu_idx, per_sahibi_idx, per_idx, tas_id):
        return ActionManager.islem_yap(self, isleyen_oyuncu_idx, per_sahibi_idx, per_idx, tas_id)
        
    @logger.log_function
    def joker_degistir_global(self, degistiren_oyuncu_idx, temsilci_tas): # GÜNCEL METOT
        return ActionManager.joker_degistir_global(self, degistiren_oyuncu_idx, temsilci_tas)

    @logger.log_function
    def tas_at(self, oyuncu_index, tas_id):
        result = TurnManager.tas_at(self, oyuncu_index, tas_id)
        if result:
            oyuncu_adi = self.oyuncular[oyuncu_index].isim
            atilan_tas = self.atilan_taslar[-1]
            self._log_game_flow(f"Taş Atıldı: {oyuncu_adi} -> {atilan_tas.renk}_{atilan_tas.deger} ({atilan_tas.id})") 
        return result

    @logger.log_function
    def desteden_cek(self, oyuncu_index):
        result = TurnManager.desteden_cek(self, oyuncu_index)
        if result:
             oyuncu_adi = self.oyuncular[oyuncu_index].isim
             self._log_game_flow(f"Taş Çekildi: {oyuncu_adi} desteden çekti.")
        return result

    @logger.log_function
    def atilan_tasi_al(self, oyuncu_index):
        return TurnManager.atilan_tasi_al(self, oyuncu_index)

    @logger.log_function
    def atilan_tasi_gecti(self):
        return TurnManager.atilan_tasi_gecti(self)

    @logger.log_function
    def el_ac_joker_ile(self, oyuncu_index, secilen_taslar, joker, secilen_deger):
        joker.joker_yerine_gecen = secilen_deger
        result = ActionManager._eli_ac_ve_isle(self, oyuncu_index, secilen_taslar)
        
        # YENİ MANTIK: Joker temsilcisini takip et
        if result.get("status") == "success":
             self._log_game_flow(f"El Açıldı: {self.oyuncular[oyuncu_index].isim} görevi başarıyla tamamladı.")
             self.acik_joker_temsilcileri.append(secilen_deger)

        return result

    @logger.log_function
    def _sira_ilerlet(self, yeni_index):
        if yeni_index < self.sira_kimde_index:
            self.tur_numarasi += 1
            logger.info(f"Yeni tura geçildi: Tur {self.tur_numarasi}")
            self._log_game_flow(f"Yeni Tur: Tur {self.tur_numarasi}")
        self.sira_kimde_index = yeni_index
        yeni_oyuncu_adi = self.oyuncular[yeni_index].isim
        self._log_game_flow(f"Sıra Değişti: Sıra -> {yeni_oyuncu_adi}")
        
    @logger.log_function
    def _per_sirala(self, per):
        if not per: return
        is_seri = Rules._per_seri_mu(per)
        if not is_seri:
            per.sort(key=lambda t: (t.joker_yerine_gecen or t).deger or 0)
        else:
            sayilar = sorted([(t.joker_yerine_gecen or t).deger for t in per if t.joker_yerine_gecen or t.renk != 'joker'])
            if 1 in sayilar and 13 in sayilar:
                per.sort(key=lambda t: 14 if (t.joker_yerine_gecen or t).deger == 1 else (t.joker_yerine_gecen or t).deger or 0)
            else:
                per.sort(key=lambda t: (t.joker_yerine_gecen or t).deger or 0)
    
    def oyun_bitti_mi(self):
        # KRİTİK DÜZELTME: Eğer deste boşsa ve durum BITIS değilse, durumu BITIS'e geçir.
        if not self.deste.taslar and self.oyun_durumu != GameState.BITIS:
            self.oyun_durumu = GameState.BITIS
            self.kazanan_index = None
            logger.info("Oyun durumu, deste boş olduğu için BITIS olarak güncellendi.")
            
        return self.oyun_durumu == GameState.BITIS or not self.deste.taslar # <-- Bu satır teknik olarak BITIS kontrolünü yapar.