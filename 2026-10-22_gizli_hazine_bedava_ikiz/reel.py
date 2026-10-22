"""Reel No.007 (22.10.2026 19:00) — gizli_hazine() ★ ilk bölüm: ücretli uygulamaların bedava ikizi (3→1 geri sayım).
KOYU kapak. Ses: İrem (ElevenLabs, Speko üzerinden). Müzik: lo-fi. HAZİNE → DM."""
import json, math, subprocess, sys
sys.path.insert(0, "/home/claude/sablon")
from siber_v2 import *  # noqa
from muzik_uretici import make_music
from PIL import Image, ImageDraw

OUT = "/home/claude/reel7"
NO, DATE, SERIES = 7, "22.10.2026", "gizli_hazine()"
N = " "
PLAN = json.load(open(f"{OUT}/ses/plan.json"))
DURS = [q["dur"] for q in PLAN]
DURS[-1] += 0.6
STARTS = [sum(DURS[:i]) for i in range(len(DURS))]
DUR = sum(DURS)


def _words(i):
    q = PLAN[i]; ws = q["text"].split(" ")
    w8 = [max(2, len(w.strip(".,?!:"))) + 1.5 for w in ws]; tot = sum(w8)
    t0, out = STARTS[i] + q["lead"], []
    for w, k in zip(ws, w8):
        d = q["speech"] * k / tot; out.append((w, t0, t0 + d * 0.95)); t0 += d
    return out


WORDS = [w for i in range(len(PLAN)) for w in _words(i)]
_base = base_frame(NO, DATE, SERIES)


def quote_card():
    """BentoPDF'in kendi sayfasındaki cümlenin birebir dizgisi (logo/arayüz taklidi yok)."""
    w, h = 800, 250
    im = Image.new("RGB", (w, h), (246, 244, 238))
    d = ImageDraw.Draw(im)
    d.text((34, 26), "bentopdf.com  ·  SSS", font=FM(24, True), fill=(110, 110, 110))
    f = FI(38, 600)
    for k, ln in enumerate(["“100% client-side, your files", "never leave your device.”"]):
        d.text((34, 80 + k * 54), ln, font=f, fill=(30, 30, 34))
    tw = d.textlength("never leave your device.”", font=f)
    d.line([34, 80 + 54 + 46, 34 + tw, 80 + 54 + 46], fill=(230, 180, 0), width=5)
    return im


_QUOTE = quote_card()


def count_head(d, k, label, a):
    """Sol üstte geri sayım rakamı + küçük etiket."""
    big_number(d, X0 - 6, 300, str(k), size=260, col=YEL, a=a)
    d.text((X0 + 175, 400), label, font=FM(28, True), fill=mix(MUTED, a))


def reveal_name(d, y, name, lt, size=170, seed=5):
    """Fosforlu şerit soldan sağa çizilirken isim belirir."""
    f = FI(size, 850)
    tw = track_len(d, name, f, -0.04)
    a = ease(lt / 0.45)
    marker(d, (X0 - 14, y + size * 0.16, X0 + tw + 18, y + size * 1.22), seed=seed, a=a)
    # isim yalnızca şeridin geçtiği kısımda görünür
    cut = X0 - 14 + (tw + 32) * a
    x = X0
    for i, ch in enumerate(name):
        cw = d.textlength(ch, font=f)
        if x + cw * 0.5 <= cut:
            d.text((x, y), ch, font=f, fill=BG)
        x += cw + (-0.04) * f.size
    return y + size * 1.3


def badges(d, y, items, lt, col=YEL):
    x = X0
    for k, txt in enumerate(items):
        b = ease((lt - k * 0.15) / 0.25)
        if b <= 0:
            continue
        w = d.textlength(txt, font=FM(26, True)) + 36
        if x + w > X0 + MAXW:
            x, y = X0, y + 70
        x = badge(d, x, y, txt, col=mix(col if k == 0 else FG, b)) + 16
    return y + 70


# ---------------- sahneler ----------------
def s1(img, d, lt):
    d.text((X0, 330), "3 ÜCRETSİZ ARAÇ  ·  SONUNCUSU İNANILMAZ", font=FM(27, True), fill=mix(MUTED, ease(lt / 0.2)))
    headline(d, X0, 400, [("Ücretli", False), ("uygulamaların", False), (f"bedava{N}ikizi.", True)], size=112,
             t=lt, mark_a=ease((lt - 0.55) / 0.3))
    for k, n in enumerate(["3", "2", "1"]):
        a = ease((lt - 1.0 - k * 0.18) / 0.25)
        if a <= 0:
            continue
        x = X0 + k * 290
        d.rounded_rectangle([x, 800, x + 260, 960], radius=18, outline=mix(RULE if k < 2 else YEL, a), width=3)
        d.text((x + 30, 830), n, font=FM(34, True), fill=mix(MUTED, a))
        d.text((x + 130, 900), "?", font=FI(80, 800), fill=mix(YEL if k == 2 else FG, a), anchor="mm")


def s2(img, d, lt):
    count_head(d, 3, "DERT", ease(lt / 0.2))
    para(d, X0, 640, "Telefondaki fotoğrafı bilgisayara atmak için…", size=52, w=600,
         col=mix(FG, ease((lt - 0.2) / 0.25)))
    a = ease((lt - 0.7) / 0.3)
    if a > 0:
        # kendine mesaj balonu (genel çizim, uygulama arayüzü taklidi yok)
        y = 820 + (1 - a) * 20
        d.text((X0, y), "Kendine not", font=FM(26, True), fill=mix(MUTED, a))
        d.rounded_rectangle([X0 + 200, y + 50, X0 + MAXW, y + 170], radius=26, fill=mix(GRN_BG, a))
        d.text((X0 + 240, y + 110), "IMG_4821.HEIC  ·  3,2 MB", font=FM(30, True), fill=mix(FG, a, GRN_BG), anchor="lm")
        d.text((X0 + MAXW - 30, y + 200), "kendine mesaj mı?", font=FI(40, 700), fill=mix(YEL, ease((lt - 1.3) / 0.3)),
               anchor="rs")


def s3(img, d, lt):
    d.text((X0, 330), "3  ·  AIRDROP'UN HER CİHAZDA ÇALIŞAN İKİZİ", font=FM(27, True), fill=mix(MUTED, ease(lt / 0.2)))
    y = reveal_name(d, 380, "LocalSend", lt - 0.1, seed=5)
    para(d, X0, y + 10, "Aynı Wi-Fi'daki telefon ve bilgisayar arasında dosya gönderir. İnternet yok, hesap yok.",
         size=46, w=500, col=mix(FG, ease((lt - 0.8) / 0.3)))
    y2 = badges(d, y + 210, ["ÜCRETSİZ", "AÇIK KAYNAK", "TELEFONDA DA ÇALIŞIR"], lt - 1.3)
    c = ease((lt - 2.0) / 0.3)
    if c > 0:
        d.text((X0, y2 + 30), "Windows · Mac · Linux · Android · iOS", font=FM(26), fill=mix(MUTED, c))


def s4(img, d, lt):
    count_head(d, 2, "DERT", ease(lt / 0.2))
    headline(d, X0, 630, [("Maaş", False), ("bordronu", False), ("nereye", False), (f"yüklüyorsun?", True)], size=84,
             t=lt - 0.15, mark_a=ease((lt - 0.7) / 0.3))
    a = ease((lt - 1.0) / 0.3)
    if a > 0:
        y = 900
        d.rounded_rectangle([X0, y, X0 + 330, y + 110], radius=14, fill=mix(PANEL, a))
        d.text((X0 + 26, y + 55), "bordro.pdf", font=FM(32, True), fill=mix(FG, a, PANEL), anchor="lm")
        p = ease((lt - 1.3) / 0.5)
        x1 = X0 + 350 + 160 * p
        d.line([X0 + 350, y + 55, x1, y + 55], fill=mix(RED, a), width=5)
        if p > 0.9:
            d.polygon([(x1, y + 40), (x1 + 22, y + 55), (x1, y + 70)], fill=RED)
        b = ease((lt - 1.7) / 0.3)
        if b > 0:
            d.rounded_rectangle([X0 + 540, y, X0 + MAXW, y + 110], radius=14, outline=mix(RED, b), width=3)
            d.text((X0 + 700, y + 55), "bilinmeyen sunucu", font=FM(26, True), fill=mix(RED, b), anchor="mm")


def s5(img, d, lt):
    d.text((X0, 330), "2  ·  PDF ARAÇLARININ BEDAVA İKİZİ", font=FM(27, True), fill=mix(MUTED, ease(lt / 0.2)))
    y = reveal_name(d, 380, "BentoPDF", lt - 0.1, seed=9)
    para(d, X0, y + 5, "Birleştir, böl, sıkıştır, dönüştür: 100'den fazla araç, tarayıcıda.", size=44, w=500,
         col=mix(FG, ease((lt - 0.7) / 0.3)))
    a = ease((lt - 1.2) / 0.35)
    evidence_card(img, _QUOTE, (W / 2 - 10, y + 300 + (1 - a) * 20), width=780, tilt=-1.5, a=a,
                  tag="BentoPDF'in kendi açıklaması · 2026")
    d = ImageDraw.Draw(img)
    badges(d, y + 520, ["ÜYELİK YOK", "TÜRKÇE ARAYÜZ", "TELEFONDA DA"], lt - 2.0)


def s6(img, d, lt):
    count_head(d, 1, "EN İYİSİ SONDA", ease(lt / 0.2))
    para(d, X0, 640, "Mail, ödev, rapor, açıklama…", size=54, w=700, col=mix(FG, ease((lt - 0.15) / 0.25)))
    a = ease((lt - 0.5) / 0.25)
    if a > 0:
        y = 780
        d.rounded_rectangle([X0, y, X0 + MAXW, y + 200], radius=16, outline=mix(RULE, a), width=2)
        txt = "Merhaba hocam, ödevi ekte gönderiyorum."
        n = int(max(0, lt - 0.6) * 18)
        shown = txt[:n]
        f = FI(40, 500)
        para(d, X0 + 34, y + 36, shown, size=40, w=500, col=mix(FG, a), maxw=MAXW - 70)
        if int(lt * 3) % 2 == 0:
            lines = shown.split(" ")
            d.rectangle([X0 + 34, y + 150, X0 + 38, y + 186], fill=YEL) if not shown else None
    b = ease((lt - 1.6) / 0.3)
    if b > 0:
        d.text((X0, 1050), "hâlâ tek tek mi yazıyorsun?", font=FI(50, 800), fill=mix(YEL, b))


def wave(d, x, y, w, lt, a):
    for k in range(34):
        hgt = 10 + 46 * abs(math.sin(k * 0.7 + lt * 7)) * (0.5 + 0.5 * math.sin(k * 0.31 + lt * 3))
        xx = x + k * (w / 34)
        d.rounded_rectangle([xx, y - hgt / 2, xx + 10, y + hgt / 2], radius=5, fill=mix(YEL, a))


def s7(img, d, lt):
    d.text((X0, 330), "1  ·  KONUŞ, O YAZSIN", font=FM(27, True), fill=mix(MUTED, ease(lt / 0.2)))
    y = reveal_name(d, 380, "Handy", lt - 0.1, seed=13)
    para(d, X0, y + 5, "Kısayola bas, konuş: söylediğin, yazdığın yere metin olarak düşer.", size=44, w=500,
         col=mix(FG, ease((lt - 0.6) / 0.3)))
    a = ease((lt - 1.0) / 0.3)
    if a > 0:
        wave(d, X0, y + 200, 400, lt, a)
        d.text((X0 + 440, y + 200), "→  “Merhaba hocam…”", font=FI(40, 700), fill=mix(FG, a), anchor="lm")
    yb = badges(d, y + 270, ["İNTERNETSİZ", "AÇIK KAYNAK", "SES CİHAZDAN ÇIKMAZ"], lt - 1.5)
    c = ease((lt - 2.2) / 0.3)
    if c > 0:
        d.text((X0, yb + 25), f"İpucu: Türkçe için ayarlardan Whisper modelini seç.", font=FI(36, 600), fill=mix(MUTED, c))


def s8(img, d, lt):
    d.text((X0, 330), "LİNKLER + BONUS 4. ARAÇ", font=FM(28, True), fill=MUTED)
    para(d, X0, 400, "Yorumlara", size=80, w=800, col=mix(FG, ease(lt / 0.2)))
    a = ease((lt - 0.25) / 0.3)
    f = FI(210, 850)
    tw = track_len(d, "HAZİNE", f, -0.045)
    marker(d, (X0 - 10, 520, X0 + tw + 20, 770), seed=21, a=a)
    big_number(d, X0, 500, "HAZİNE", size=210, col=BG if a > 0.6 else FG, a=1)
    b = ease((lt - 0.9) / 0.3)
    para(d, X0, 830, "yaz; 3 linki ve bonus aracı DM'den atayım.", size=50, w=600, col=mix(FG, b))


def s9(img, d, lt):
    headline(d, X0, 330, [("Hangisini", False), (f"bilmiyordun?", True)], size=104, t=lt,
             mark_a=ease((lt - 0.4) / 0.3))
    for k, (n, name) in enumerate([("1", "Handy"), ("2", "BentoPDF"), ("3", "LocalSend")]):
        a = ease((lt - 0.7 - k * 0.15) / 0.25)
        if a <= 0:
            continue
        yy = 600 + k * 120
        d.rounded_rectangle([X0, yy, X0 + MAXW, yy + 96], radius=16, outline=mix(YEL if k == 0 else RULE, a), width=3)
        d.text((X0 + 34, yy + 48), n, font=FM(42, True), fill=mix(YEL, a), anchor="lm")
        d.text((X0 + 100, yy + 48), name, font=FI(46, 800), fill=mix(FG, a), anchor="lm")
    c = ease((lt - 1.5) / 0.3)
    if c > 0:
        d.text((X0, 990), "Dosyayla boğuşan birine gönder.", font=FI(44, 700), fill=mix(FG, c))
        d.text((X0, 1080), "gizli_hazine()  ·  her perşembe yeni bölüm  ·  takip et", font=FM(25, True),
               fill=mix(MUTED, c))


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
_OFF = {}


def offset(i):
    if i not in _OFF:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        SCENES[i](lay, ImageDraw.Draw(lay), DURS[i] + 3)
        _, top, _, bot = lay.getbbox()
        _OFF[i] = int(max(300 - top, min(1290 - bot, 800 - (top + bot) / 2)))
    return _OFF[i]


def frame(t):
    i = max(k for k in range(len(SCENES)) if STARTS[k] <= t + 1e-9)
    img = _base.copy()
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    SCENES[i](lay, ImageDraw.Draw(lay), t - STARTS[i])
    img.paste(lay, (0, offset(i)), lay)
    img = vignette(camera(img, t, t - STARTS[i], seed=71 + i))
    subtitles(ImageDraw.Draw(img), WORDS, t)
    img = apply_grain(img, t, strength=5)
    for b in STARTS[1:]:
        if b - 0.125 <= t <= b + 0.125:
            img = wipe(img, (t - (b - 0.125)) / 0.25)
    return img


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    if mode == "stills":
        for k in range(len(SCENES)):
            frame(STARTS[k] + DURS[k] - 0.15).save(f"{OUT}/kare_{k + 1}.png")
        frame(1.0).save(f"{OUT}/kare_0_1sn.png")
        sys.exit()
    if mode == "cover":
        cover_v2(f"{OUT}/kapak.jpg", NO, DATE, SERIES,
                 [("Ücretli uygulamaların", False), (f"bedava{N}ikizi", True)], theme="dark",
                 sub=f"3 ücretsiz araç. Sonuncusu konuştuğunu{N}yazıyor.")
        sys.exit()
    vid = f"{OUT}/video_sessiz.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                           "-preset", "medium", vid], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        ff.stdin.write(frame(i / FPS).tobytes())
    ff.stdin.close(); ff.wait()
    rms, style, desc = make_music(f"{OUT}/muzik.wav", DUR, drop=STARTS[1], arp_start=STARTS[2], cta=STARTS[7],
                                  style="lofi", seed="2026-10-22 gizli_hazine bedava ikiz", voice=f"{OUT}/ses/ses.wav",
                                  whooshes=(STARTS[2], STARTS[6]),
                                  events=[("ping", 0.15), ("chime", STARTS[2] + 0.35), ("chime", STARTS[4] + 0.35),
                                          ("type", STARTS[5] + 0.6, 9), ("chime", STARTS[6] + 0.35),
                                          ("success", STARTS[8] + 0.7)])
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", f"{OUT}/muzik.wav", "-c:v", "libx264",
                    "-crf", "22", "-maxrate", "14M", "-bufsize", "28M", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
                    "-shortest", "-movflags", "+faststart", f"{OUT}/reel.mp4"], check=True)
    print("ok", round(DUR, 2), round(rms, 1), desc)
