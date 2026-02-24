import pygame
import random
import sys

# --- 1. AYARLAR VE BAŞLATMA ---
pygame.init()
ekran_genislik = 720
ekran_yukseklik = 1680 # 1680 çok uzun olabilir, standart 1280 idealdir
ekran = pygame.display.set_mode((ekran_genislik, ekran_yukseklik))

SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KIRMIZI = (255, 0, 0)
YESIL = (0, 255, 0)

font_puan = pygame.font.SysFont("Arial", 50)
font_mesaj = pygame.font.SysFont("Arial", 90, bold=True)

def gorsel_hazirla(dosya_adi, g, y):
    try:
        img = pygame.image.load(dosya_adi).convert_alpha()
        return pygame.transform.scale(img, (g, y))
    except:
        s = pygame.Surface((g, y))
        s.fill((random.randint(0,255), random.randint(0,255), 255))
        return s

GEMI_RESMI = gorsel_hazirla("gemi.png", 170, 170)

LAZER_TIPLERI = [
    gorsel_hazirla("lazer1.png", 100, 100),
    gorsel_hazirla("lazer2.png", 60, 60),
    gorsel_hazirla("lazer3.png", 60, 60)
]

METEOR_GÖRSELLERİ = [
    {"resim": gorsel_hazirla("meteor1.png", 120, 120), "puan": 10},
    {"resim": gorsel_hazirla("meteor2.png", 100, 100), "puan": 20},
    {"resim": gorsel_hazirla("meteor3.png", 80, 80), "puan": 30},
    {"resim": gorsel_hazirla("meteor4.png", 60, 60), "puan": 40}
]

# --- 3. OYUN MANTIĞI ---
def oyunu_sifirla():
    return {
        "gemi_x": ekran_genislik // 2 - 55,
        "gemi_y": ekran_yukseklik - 100, # Görünür olması için yukarı çekildi
        "lazerler": [],
        "meteorlar": [],
        "puan": 0,
        "durum": "OYUN",
        "lazer_sirasi": 0,
        "lazer_bekleme": 0
    }

oyun = oyunu_sifirla()
saat = pygame.time.Clock()

while True:
    ekran.fill(SIYAH)
    fare_x, fare_y = pygame.mouse.get_pos()
    fare_tuslari = pygame.mouse.get_pressed() # Tuş durumlarını al
    tiklandi = False

    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if olay.type == pygame.MOUSEBUTTONDOWN:
            tiklandi = True

    if oyun["durum"] == "OYUN":
        # GEMİ HAREKETİ
        oyun["gemi_x"] = fare_x - 55
        gemi_rect = pygame.Rect(oyun["gemi_x"], oyun["gemi_y"], 110, 110)

        # ATEŞLEME SİSTEMİ (HEM TIKLAMA HEM BASILI TUTMA)
        if (tiklandi or fare_tuslari[0]) and oyun["lazer_bekleme"] == 0:
            lazer_index = oyun["lazer_sirasi"] % 3
            secilen_lazer = LAZER_TIPLERI[lazer_index]
            
            l_x = oyun["gemi_x"] + 90 - (secilen_lazer.get_width() // 2)
            l_y = oyun["gemi_y"] - 5
            
            oyun["lazerler"].append({
                "rect": pygame.Rect(l_x, l_y, secilen_lazer.get_width(), secilen_lazer.get_height()),
                "resim": secilen_lazer
            })
            oyun["lazer_sirasi"] += 1 
            oyun["lazer_bekleme"] = 10 # Her 10 karede bir ateş eder

        # Bekleme süresini her karede azalt (Ateş etme bloğunun DIŞINDA olmalı)
        if oyun["lazer_bekleme"] > 0:
            oyun["lazer_bekleme"] -= 1

        # METEOR OLUŞTURMA
        if random.randint(1, 20) == 1:
            tip = random.choice(METEOR_GÖRSELLERİ)
            mx = random.randint(0, ekran_genislik - tip["resim"].get_width())
            oyun["meteorlar"].append({
                "rect": pygame.Rect(mx, -150, tip["resim"].get_width(), tip["resim"].get_height()),
                "resim": tip["resim"],
                "puan": tip["puan"],
                "hiz_y": random.randint(7, 15),
                "hiz_x": random.randint(-4, 4),
                "aci": 0,
                "donus": random.randint(3, 9)
            })

        # LAZERLERİ GÜNCELLE
        for l in oyun["lazerler"][:]:
            l["rect"].y -= 25
            ekran.blit(l["resim"], l["rect"])
            if l["rect"].bottom < 0: oyun["lazerler"].remove(l)

        # METEORLARI GÜNCELLE
        for m in oyun["meteorlar"][:]:
            m["rect"].y += m["hiz_y"]
            m["rect"].x += m["hiz_x"]
            m["aci"] = (m["aci"] + m["donus"]) % 360
            
            d_resim = pygame.transform.rotate(m["resim"], m["aci"])
            d_rect = d_resim.get_rect(center=m["rect"].center)
            ekran.blit(d_resim, d_rect)

            for l in oyun["lazerler"][:]:
                if m["rect"].colliderect(l["rect"]):
                    oyun["puan"] += m["puan"]
                    if l in oyun["lazerler"]: oyun["lazerler"].remove(l)
                    if m in oyun["meteorlar"]: oyun["meteorlar"].remove(m)
                    break
            
            if m in oyun["meteorlar"]:
                if m["rect"].colliderect(gemi_rect):
                    oyun["durum"] = "BITTI"
                elif m["rect"].top > ekran_yukseklik:
                    oyun["meteorlar"].remove(m)

        ekran.blit(GEMI_RESMI, gemi_rect)
        puan_txt = font_puan.render(f"Skor: {oyun['puan']}", True, BEYAZ)
        ekran.blit(puan_txt, (20, 20))

    elif oyun["durum"] == "BITTI":
        go_txt = font_puan.render(f"Skor: {oyun['puan']}", True, BEYAZ)
        ekran.blit(go_txt, go_txt.get_rect(topleft=(ekran_genislik//2.5, ekran_yukseklik//2))),
        go_txt = font_mesaj.render("GAME OVER", True, KIRMIZI)
        ekran.blit(go_txt, go_txt.get_rect(topleft=(ekran_genislik//2.5, ekran_yukseklik//1.8)))
        if tiklandi:
            oyun = oyunu_sifirla()

    pygame.display.flip()
    saat.tick(60)
