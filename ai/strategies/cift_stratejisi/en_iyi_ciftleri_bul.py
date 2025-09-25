# ai/strategies/cift_stratejisi/en_iyi_ciftleri_bul.py
from log import logger
from rules.per_validators.cift_per_mu import cift_per_mu
from ai.strategies.cift_stratejisi._ciftleri_ve_tekleri_bul import _ciftleri_ve_tekleri_bul

@logger.log_function
def en_iyi_ciftleri_bul(el, gorev):
    if gorev != "Çift":
        return None
    
    jokerler = [t for t in el if t.renk == 'joker']
    ciftler, tekler = _ciftleri_ve_tekleri_bul(el)

    # Elimizdeki toplam çift sayısını hesapla
    potansiyel_cift_sayisi = len(ciftler) + len(jokerler) // 2
    
    # 4 çifte ulaşabiliyorsa, açılış kombinasyonunu oluştur
    if potansiyel_cift_sayisi >= 4:
        acilacak_taslar = []
        cift_sayisi = 0
        kullanilan_jokerler = []
        
        # 1. Gerçek çiftlerden en fazla 4 çifti al (8 taş).
        for cift_grup in ciftler:
            if cift_sayisi < 4:
                acilacak_taslar.extend(cift_grup)
                cift_sayisi += 1
            if cift_sayisi == 4:
                break
        
        # 2. Kalan jokerleri ve tek taşları kullanarak tamamla.
        if cift_sayisi < 4:
            
            # A. Önce 1 joker + 1 tek taş (1 çift) oluşturma.
            joker_index = 0
            tek_index = 0
            while joker_index < len(jokerler) and tek_index < len(tekler) and cift_sayisi < 4:
                joker = jokerler[joker_index]
                tek_tas = tekler[tek_index]
                
                # Jokeri eşleştir (Çiftler için joker, tek taşın yerine geçer)
                joker.joker_yerine_gecen = tek_tas 
                acilacak_taslar.extend([tek_tas, joker])
                kullanilan_jokerler.append(joker)
                
                cift_sayisi += 1
                joker_index += 1
                tek_index += 1
            
            # B. Kalan jokerleri çift olarak kullanma (2 joker = 1 çift).
            kalan_jokerler = [j for j in jokerler if j not in kullanilan_jokerler]
            
            if len(kalan_jokerler) >= 2 and cift_sayisi < 4:
                joker_cifti_sayisi = min(len(kalan_jokerler) // 2, 4 - cift_sayisi)
                
                if joker_cifti_sayisi > 0:
                    joker_ciftleri = kalan_jokerler[:joker_cifti_sayisi * 2]
                    
                    # 2 jokeri de açılışa dahil et
                    acilacak_taslar.extend(joker_ciftleri)
                    cift_sayisi += joker_cifti_sayisi

        # SADECE tam olarak 8 taş (4 çift) bulduysa ve kural geçerliyse döndür.
        if len(acilacak_taslar) == 8:
            # cift_per_mu, jokerlerin tek kalanları tamamlayıp tamamlamadığını kontrol eder.
            if cift_per_mu(acilacak_taslar):
                return acilacak_taslar
        
        # Başarısız olursa, atanan joker yerine geçen değerlerini sıfırla
        for tas in acilacak_taslar:
            if tas.renk == 'joker':
                tas.joker_yerine_gecen = None

    return None