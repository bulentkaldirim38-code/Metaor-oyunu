import pygame
import random
import sys

# --- AYARLAR VE BAŞLATMA ---
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KIRMIZI = (255, 0, 0)
YESIL = (0, 255, 0)

def gorsel_hazirla(dosya_adi, g, y):
    try:
        img = pygame.image.load(dosya_adi).convert_alpha()
        return pygame.transform.scale(img, (g, y))
    except Exception as e:
        print(f"Gorsel yukleme hatasi ({dosya_adi}): {e}", file=sys.stderr)
        s = pygame.Surface((g, y))
        s.fill((random.randint(50, 200), random.randint(50, 200), 255))
        return s

def oyunu_sifirla(ekran_genislik, ekran_yukseklik):
    return {
        "gemi_x": ekran_genislik // 2 - 70,
        "gemi_y": ekran_yukseklik - 200, 
        "lazerler": [],
        "meteorlar": [],
        "puan": 0,
        "durum": "OYUN",
        "lazer_sirasi": 0,
        "lazer_bekleme": 0
    }

def main():
    pygame.init()
    pygame.display.init()
    pygame.font.init()

    # Mobil uyumlu ekran ayarları
    ekran_genislik = 720
    ekran_yukseklik = 1280
    ekran = pygame.display.set_mode((ekran_genislik, ekran_yukseklik))
    pygame.display.set_caption("Meteor Hunter")

    def font_getir(size, bold=False):
        try:
            return pygame.font.SysFont("Arial", size, bold=bold)
        except:
            return pygame.font.Font(None, size)

    font_puan = font_getir(50)
    font_mesaj = font_getir(100, bold=True)
    font_buton = font_getir(60)

    # Görseller
    GEMI_RESMI = gorsel_hazirla("gemi.png", 140, 140)
    LAZER_TIPLERI = [
        gorsel_hazirla("lazer1.png", 40, 80),
        gorsel_hazirla("lazer2.png", 40, 80),
        gorsel_hazirla("lazer3.png", 40, 80)
    ]
    METEOR_GORSELLERI = [
        {"resim": gorsel_hazirla("meteor1.png", 120, 120), "puan": 10},
        {"resim": gorsel_hazirla("meteor2.png", 100, 100), "puan": 20},
        {"resim": gorsel_hazirla("meteor3.png", 80, 80), "puan": 30},
        {"resim": gorsel_hazirla("meteor4.png", 60, 60), "puan": 40}
    ]

    oyun = oyunu_sifirla(ekran_genislik, ekran_yukseklik)
    saat = pygame.time.Clock()

    while True:
        ekran.fill(SIYAH)
        fare_pos = pygame.mouse.get_pos()
        fare_tuslari = pygame.mouse.get_pressed()
        tiklandi = False

        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
            if olay.type == pygame.MOUSEBUTTONDOWN:
                tiklandi = True

        if oyun["durum"] == "OYUN":
            # Gemi Hareketi (Parmak takibi)
            oyun["gemi_x"] = fare_pos[0] - 70
            oyun["gemi_x"] = max(0, min(oyun["gemi_x"], ekran_genislik - 140))
            gemi_rect = pygame.Rect(oyun["gemi_x"], oyun["gemi_y"], 140, 140)

            # Ateşleme
            if (fare_tuslari[0]) and oyun["lazer_bekleme"] == 0:
                lazer_index = oyun["lazer_sirasi"] % 3
                secilen_lazer = LAZER_TIPLERI[lazer_index]
                l_x = oyun["gemi_x"] + 70 - (secilen_lazer.get_width() // 2)
                l_y = oyun["gemi_y"] - 20
                oyun["lazerler"].append({
                    "rect": pygame.Rect(l_x, l_y, secilen_lazer.get_width(), secilen_lazer.get_height()),
                    "resim": secilen_lazer
                })
                oyun["lazer_sirasi"] += 1
                oyun["lazer_bekleme"] = 10 

            if oyun["lazer_bekleme"] > 0:
                oyun["lazer_bekleme"] -= 1

            # Meteor Oluşturma
            if random.randint(1, 20) == 1:
                tip = random.choice(METEOR_GORSELLERI)
                mx = random.randint(0, ekran_genislik - 100)
                oyun["meteorlar"].append({
                    "rect": pygame.Rect(mx, -150, tip["resim"].get_width(), tip["resim"].get_height()),
                    "resim": tip["resim"],
                    "puan": tip["puan"],
                    "hiz_y": random.randint(7, 14),
                    "hiz_x": random.randint(-2, 2),
                    "aci": 0,
                    "donus": random.randint(3, 8)
                })

            # Lazer Güncelleme
            for l in oyun["lazerler"][:]:
                l["rect"].y -= 25
                ekran.blit(l["resim"], l["rect"])
                if l["rect"].bottom < 0: oyun["lazerler"].remove(l)

            # Meteor Güncelleme ve Çarpışma
            for m in oyun["meteorlar"][:]:
                m["rect"].y += m["hiz_y"]
                m["rect"].x += m["hiz_x"]
                m["aci"] = (m["aci"] + m["donus"]) % 360

                d_resim = pygame.transform.rotate(m["resim"], m["aci"])
                d_rect = d_resim.get_rect(center=m["rect"].center)
                ekran.blit(d_resim, d_rect)

                # Lazer vurdu mu?
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
            puan_txt = font_puan.render(f"Puan: {oyun['puan']}", True, BEYAZ)
            ekran.blit(puan_txt, (30, 30))

        elif oyun["durum"] == "BITTI":
            # Metinleri Hazırla
            go_txt = font_mesaj.render("GAME OVER", True, KIRMIZI)
            skor_txt = font_puan.render(f"TOPLAM SKOR: {oyun['puan']}", True, BEYAZ)
            restart_txt = font_buton.render("TEKRAR OYNA", True, YESIL)

            # Ekrana Ortala
            go_rect = go_txt.get_rect(center=(ekran_genislik//2, ekran_yukseklik//2 - 100))
            skor_rect = skor_txt.get_rect(center=(ekran_genislik//2, ekran_yukseklik//2))
            res_rect = restart_txt.get_rect(center=(ekran_genislik//2, ekran_yukseklik//2 + 150))

            ekran.blit(go_txt, go_rect)
            ekran.blit(skor_txt, skor_rect)
            ekran.blit(restart_txt, res_rect)

            if tiklandi:
                oyun = oyunu_sifirla(ekran_genislik, ekran_yukseklik)

        pygame.display.flip()
        saat.tick(60)

if __name__ == "__main__":
    main()
