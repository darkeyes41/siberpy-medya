"""Reel No.009 (23.10.2026 19:00) — kariyer_radar(): "Siber güvenlik ilanları 4 yılın dibinde, ama bir rol %268 arttı."
Veri: CyberSN, Cybersecurity Jobs Report (2026 through September; ABD, Ocak–Eylül, ilan sayısı). KOYU kapak.
Ses: İrem (ElevenLabs, Speko üzerinden). Müzik: 80'ler synthwave. YOL→DM."""
import json, subprocess, sys
sys.path.insert(0, "/home/claude/sablon")
from siber_v2 import *  # noqa
from muzik_uretici import make_music
from PIL import Image, ImageDraw

OUT = "/home/claude/reel9"
NO, DATE, SERIES = 9, "23.10.2026", "kariyer_radar()"
N = " "
PLAN = json.load(open(f"{OUT}/ses/plan.json"))
SUBS = ["Siber güvenlik ilanları 4 yılın dibinde.", "Bir yılda 84 bin ilan kayboldu.",
        "Sızma testi ilanları neredeyse yarıya indi.", "Ama bir rol neredeyse 4 katına çıktı.",
        "Yapay zeka güvenliği. Ama toplamın %1'i.", "Eylülde her 5 ilandan biri yapay zeka istedi.",
        "Öğrenme yolu için yorumlara YOL yaz.", "Sence daralıyor mu, şekil mi değiştiriyor?",
        "Her cuma yeni bölüm. Takip et."]
DURS = [q["dur"] for q in PLAN]
DURS[-1] += 0.9
STARTS = [sum(DURS[:i]) for i in range(len(DURS))]
DUR = sum(DURS)


def _words(i):
    q = PLAN[i]; ws = SUBS[i].split(" ")
    w8 = [max(2, len(w.strip(".,?!:"))) + 1.5 for w in ws]; tot = sum(w8)
    t0, out = STARTS[i] + q["lead"], []
    for w, k in zip(ws, w8):
        d = q["speech"] * k / tot; out.append((w, t0, t0 + d * 0.95)); t0 += d
    return out


WORDS = [w for i in range(len(PLAN)) for w in _words(i)]
_base = base_frame(NO, DATE, SERIES)


def wrap(d, text, f, maxw):
    cur, lines = "", []
    for wd in text.split(" "):
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = wd
    lines.append(cur)
    return lines


def report_card():
    """CyberSN raporundaki cümle ve tablo satırının birebir dizgisi (logo/arayüz taklidi yok)."""
    w, h = 840, 470
    im = Image.new("RGB", (w, h), (246, 244, 238))
    d = ImageDraw.Draw(im)
    d.text((34, 28), "CYBERSN  ·  Cybersecurity Jobs Report  ·  2026", font=FM(22, True), fill=(110, 110, 110))
    f = FI(34, 600)
    y = 78
    for ln in wrap(d, "“235,786 United States cybersecurity job postings, January to September 2026. "
                      "Down 26.4% from 320,210 in the same months of 2025.”", f, w - 68):
        if "Down 26.4%" in ln:
            x0 = 34 + d.textlength(ln.split("Down 26.4%")[0], font=f)
            marker(d, (x0 - 5, y + 4, x0 + d.textlength("Down 26.4%", font=f) + 5, y + 46), seed=4)
        d.text((34, y), ln, font=f, fill=(30, 30, 34))
        y += 46
    y += 22
    d.line([34, y, w - 34, y], fill=(200, 196, 186), width=2)
    fm = FM(22, True)
    d.text((34, y + 18), "ROLE", font=fm, fill=(120, 120, 120))
    d.text((w - 250, y + 18), "POSTINGS", font=fm, fill=(120, 120, 120))
    d.text((w - 34, y + 18), "YoY", font=fm, fill=(120, 120, 120), anchor="ra")
    y += 62
    d.rectangle([24, y - 8, w - 24, y + 52], fill=(255, 236, 150))
    fr = FM(28, True)
    d.text((34, y), "AI Security Engineer", font=fr, fill=(30, 30, 34))
    d.text((w - 250, y), "2,409", font=fr, fill=(30, 30, 34))
    d.text((w - 34, y), "+268.3%", font=fr, fill=(30, 30, 34), anchor="ra")
    return im


_CARD = report_card()


def s1(img, d, lt):
    d.text((X0, 330), "ABD  ·  OCAK–EYLÜL 2026  ·  İLAN SAYISI", font=FM(26, True), fill=mix(MUTED, ease(lt / 0.2)))
    a = ease(lt / 0.25)
    big_number(d, X0 - 10, 360, "−%26", size=300, col=RED, a=a)
    headline(d, X0, 730, [("Siber güvenlik ilanları", False), (f"4{N}yılın{N}dibinde.", True)], size=92,
             t=lt - 0.35, mark_a=ease((lt - 0.95) / 0.3))


YEARS = [("2023", 273498), ("2024", 244911), ("2025", 320210), ("2026", 235786)]


def s2(img, d, lt):
    d.text((X0, 330), "SİBER GÜVENLİK İLANLARI · OCAK–EYLÜL", font=FM(26, True), fill=MUTED)
    for k, (yr, v) in enumerate(YEARS):
        y = 430 + k * 125
        p = ease((lt - 0.1 - k * 0.22) / 0.4)
        last = k == 3
        d.text((X0, y), yr, font=FM(34, True), fill=YEL if last else FG)
        bar(d, X0 + 130, y + 6, 560, (v / 330000) * p, h=34, col=YEL if last else (120, 128, 138))
        if p > 0.05:
            d.text((X0 + 130 + 560 * v / 330000 * p + 16, y + 2), f"{v:,}".replace(",", "."), font=FM(28, True),
                   fill=mix(YEL if last else MUTED, p))
    a = ease((lt - 1.25) / 0.3)
    if a > 0:
        d.rounded_rectangle([X0, 960, X0 + 520, 1060], radius=14, fill=mix(RED_BG, a))
        d.text((X0 + 30, 1010), "−84.424 ilan", font=FI(56, 800), fill=mix(RED, a, RED_BG), anchor="lm")
    source(d, 1130, "CyberSN raporu · Ekim 2026")


ROLES = [("Sızma testi uzmanı", 45.9), ("Güvenlik mühendisi", 32.3), ("Güvenlik analisti", 30.5)]


def s3(img, d, lt):
    d.text((X0, 330), "EN ÇOK DARALANLAR · YILLIK", font=FM(26, True), fill=RED)
    headline(d, X0, 380, [("Sızma testi", False), (f"yarıya{N}iniyor.", True)], size=96, t=lt,
             mark_a=ease((lt - 0.4) / 0.3))
    for k, (r, v) in enumerate(ROLES):
        a = ease((lt - 0.6 - k * 0.25) / 0.3)
        if a <= 0:
            continue
        y = 640 + k * 130
        d.text((X0, y), r, font=FI(48, 700), fill=mix(FG, a))
        d.text((X0 + MAXW, y), f"−%{str(v).replace('.', ',')}", font=FM(44, True), fill=mix(RED, a), anchor="ra")
        bar(d, X0, y + 74, MAXW, v / 100 * a, h=12, col=RED)


def s4(img, d, lt):
    d.text((X0, 330), "AMA", font=FI(70, 850), fill=mix(YEL, ease(lt / 0.15)))
    a = ease((lt - 0.15) / 0.25)
    big_number(d, X0 - 12, 430, "+%268", size=245, col=GRN, a=a)
    b = ease((lt - 0.7) / 0.3)
    if b > 0:
        para(d, X0, 790, "Tek bir rolün ilanları bir yılda neredeyse 4 katına çıktı.", size=54, w=700,
             col=mix(FG, b))


def s5(img, d, lt):
    a = ease(lt / 0.3)
    evidence_card(img, _CARD, (W / 2, 560 + (1 - a) * 24), width=860, tilt=-1.5, a=a,
                  tag="CyberSN raporu · veri 07.10.2026")
    d = ImageDraw.Draw(img)
    b = ease((lt - 0.7) / 0.3)
    if b > 0:
        headline(d, X0, 870, [(f"Yapay{N}zeka güvenlik{N}mühendisi", True)], size=74, t=9, mark_a=b, seed=11)
    c = ease((lt - 1.6) / 0.3)
    if c > 0:
        para(d, X0, 1080, "2.409 ilan ≈ toplamın %1'i. Taban küçük, büyüme hızlı.", size=42, w=500,
             col=mix(MUTED, c))


def s6(img, d, lt):
    d.text((X0, 330), "EYLÜL 2026 İLANLARI", font=FM(26, True), fill=MUTED)
    for k in range(5):
        a = ease((lt - 0.1 - k * 0.12) / 0.25)
        x = X0 + k * 172
        col = YEL if k == 0 else (90, 98, 108)
        d.rounded_rectangle([x, 400 + (1 - a) * 20, x + 150, 640 + (1 - a) * 20], radius=18,
                            fill=mix(col, a) if k == 0 else None, outline=mix(col, a), width=3)
        if k == 0 and a > 0.5:
            d.text((x + 75, 520), "AI", font=FI(72, 850), fill=BG, anchor="mm")
    headline(d, X0, 700, [("Her 5 ilandan", False), (f"biri{N}yapay{N}zeka", True), ("istiyor.", False)], size=86,
             t=lt - 0.7, mark_a=ease((lt - 1.3) / 0.3), seed=21)
    c = ease((lt - 1.8) / 0.3)
    if c > 0:
        source(d, 1110, "CyberSN · ilanların %20'si AI/ML terimi içeriyor")


def s7(img, d, lt):
    d.text((X0, 330), "ÜCRETSİZ ÖĞRENME YOLU · 5 RESMÎ KAYNAK", font=FM(26, True), fill=MUTED)
    para(d, X0, 400, "Yorumlara", size=80, w=800, col=mix(FG, ease(lt / 0.2)))
    a = ease((lt - 0.25) / 0.3)
    f = FI(220, 850)
    tw = track_len(d, "YOL", f, -0.045)
    marker(d, (X0 - 10, 525, X0 + tw + 24, 780), seed=13, a=a)
    big_number(d, X0, 505, "YOL", size=220, col=BG if a > 0.6 else FG, a=1)
    b = ease((lt - 0.8) / 0.3)
    para(d, X0, 830, "yaz, kaynak listesini DM'den atayım.", size=48, w=600, col=mix(FG, b))
    c = ease((lt - 1.3) / 0.3)
    if c > 0:
        x = badge(d, X0, 960, "OWASP LLM Top 10", col=mix(YEL, c))
        x = badge(d, x + 14, 960, "MITRE ATLAS", col=mix(MUTED, c))
        badge(d, x + 14, 960, "+3", col=mix(MUTED, c))


def s8(img, d, lt):
    headline(d, X0, 330, [("Siber güvenlik", False), (f"işi{N}sence…", True)], size=96, t=lt,
             mark_a=ease((lt - 0.35) / 0.3))
    for k, (lab, txt) in enumerate([("A", "daralıyor"), ("B", "şekil değiştiriyor")]):
        a = ease((lt - 0.6 - k * 0.25) / 0.3)
        if a <= 0:
            continue
        y = 590 + k * 150
        d.rounded_rectangle([X0, y, X0 + MAXW, y + 120], radius=18, outline=mix(FG if k == 0 else YEL, a), width=3)
        d.text((X0 + 40, y + 60), lab, font=FI(72, 850), fill=mix(FG if k == 0 else YEL, a), anchor="lm")
        d.text((X0 + 130, y + 60), txt, font=FI(56, 700), fill=mix(FG, a), anchor="lm")
    c = ease((lt - 1.3) / 0.3)
    if c > 0:
        d.text((X0, 930), "Yorumlara A ya da B yaz.", font=FI(44, 700), fill=mix(FG, c))
        d.text((X0, 1000), "Güvenlikçi bir arkadaşına gönder.", font=FI(40, 500), fill=mix(MUTED, c))


def s9(img, d, lt):
    d.text((X0, 360), "kariyer_radar()", font=FM(64, True), fill=mix(YEL, ease(lt / 0.2)))
    headline(d, X0, 470, [("Her cuma", False), (f"yeni{N}bölüm.", True)], size=104, t=lt - 0.2,
             mark_a=ease((lt - 0.6) / 0.3), seed=31)
    b = ease((lt - 1.0) / 0.3)
    if b > 0:
        para(d, X0, 760, "Yapay zeka işini nasıl değiştiriyor, rakamla. Takip et.", size=48, w=600,
             col=mix(FG, b))


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
    img = vignette(camera(img, t, t - STARTS[i], seed=91 + i, punch=(0.15, 0.6) if i == 3 else None))
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
        sys.exit()
    if mode == "cover":
        cover_v2(f"{OUT}/kapak.jpg", NO, DATE, SERIES,
                 [("Siber güvenlik ilanları düştü. Ama bir rol", False), (f"%268{N}arttı.", True)], theme="dark",
                 sub=f"ABD verisi, Ocak–Eylül 2026. Hangi{N}rol?")
        sys.exit()
    vid = f"{OUT}/video_sessiz.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                           "-preset", "medium", vid], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        ff.stdin.write(frame(i / FPS).tobytes())
    ff.stdin.close(); ff.wait()
    rms, style, desc = make_music(f"{OUT}/muzik.wav", DUR, drop=STARTS[3], arp_start=STARTS[1] + 0.3, cta=STARTS[7],
                                  style="synthwave", seed="2026-10-23 kariyer_radar cybersn ai security",
                                  voice=f"{OUT}/ses/ses.wav", whooshes=(STARTS[3], STARTS[6]),
                                  events=[("ticks", STARTS[1] + 0.1, 8), ("buzz", STARTS[2] + 0.6),
                                          ("ping", STARTS[4] + 0.75), ("success", STARTS[8] + 0.6)])
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", f"{OUT}/muzik.wav", "-c:v", "libx264",
                    "-crf", "24", "-maxrate", "11M", "-bufsize", "22M", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
                    "-shortest", "-movflags", "+faststart", f"{OUT}/reel.mp4"], check=True)
    print("ok", round(DUR, 2), round(rms, 1), desc)
