"""Reel No.006 (EK, 22.10.2026 12:30) — ne_yapmali(): PHP2Shell 2. açı, WordPress/hazır hosting sahibi ne yapmalı.
SARI kapak. Ses: Ec (ElevenLabs, Speko üzerinden). Müzik: gerilimli elektronik."""
import json, subprocess, sys
sys.path.insert(0, "/home/claude/sablon")
from siber_v2 import *  # noqa
from muzik_uretici import make_music
from PIL import Image, ImageDraw

OUT = "/home/claude/reel_ek6"
NO, DATE, SERIES = 6, "22.10.2026", "ne_yapmali()"
N = " "
PLAN = json.load(open(f"{OUT}/ses/plan.json"))
DURS = [q["dur"] for q in PLAN]
DURS[-1] += 0.9
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


def advisory_card():
    """php.net duyurusunun ilk cümlesinin birebir dizgisi (logo/arayüz taklidi yok)."""
    w, h = 820, 380
    im = Image.new("RGB", (w, h), (246, 244, 238))
    d = ImageDraw.Draw(im)
    d.text((36, 30), "PHP SECURITY UPDATE  ·  21 Oct 2026", font=FM(24, True), fill=(110, 110, 110))
    body = ("PHP 8.5.12, 8.4.27, 8.3.36 and 8.2.35 fix two critical vulnerabilities that can "
            "allow unauthenticated remote code execution. All PHP users are strongly encouraged "
            "to update immediately.")
    f = FI(36, 600)
    cur, lines = "", []
    for wd in body.split(" "):
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=f) <= w - 72:
            cur = t
        else:
            lines.append(cur); cur = wd
    lines.append(cur)
    y = 84
    for ln in lines:
        d.text((36, y), ln, font=f, fill=(30, 30, 34))
        y += 48
    # fosforlu vurgu: "update immediately" satırı
    return im


_CARD = advisory_card()


def step(d, y, k, a):
    d.text((X0, y), f"ADIM {k}/3", font=FM(28, True), fill=mix(YEL, a))


def s1(img, d, lt):
    d.text((X0, 330), "PHP2Shell  ·  2. GÜN", font=FM(28, True), fill=RED)
    para(d, X0, 385, "Siten WordPress'te ya da hazır hostingde mi?", size=50, w=600, col=mix(FG, ease(lt / 0.25)))
    headline(d, X0, 540, [("Güncellemek", False), (f"bu{N}sefer{N}yetmiyor.", True)], size=104, t=lt - 0.25,
             mark_a=ease((lt - 0.8) / 0.3))
    a = ease((lt - 1.3) / 0.3)
    if a > 0:
        badge(d, X0, 860, "KRİTİK  ·  9,2 / 10", col=mix(RED, a))


def s2(img, d, lt):
    d.text((X0, 330), "AÇIK NEREDE?", font=FM(28, True), fill=MUTED)
    f = FI(64, 800)
    a1 = ease(lt / 0.3)
    d.rounded_rectangle([X0, 400, X0 + MAXW, 530], radius=16, fill=mix(RED_BG, a1))
    d.text((X0 + 40, 465), "WordPress / eklenti", font=f, fill=mix(FG, a1, RED_BG), anchor="lm")
    s = ease((lt - 0.5) / 0.35)
    if s > 0:
        tw = d.textlength("WordPress / eklenti", font=f)
        d.line([X0 + 30, 468, X0 + 30 + (tw + 20) * s, 462], fill=RED, width=8)
    a2 = ease((lt - 1.2) / 0.3)
    if a2 > 0:
        d.text((X0 + 20, 575), "↓", font=FI(70, 800), fill=mix(MUTED, a2))
        d.rounded_rectangle([X0, 680, X0 + MAXW, 810], radius=16, fill=mix(GRN_BG, a2))
        d.text((X0 + 40, 745), "Sunucudaki PHP", font=f, fill=mix(FG, a2, GRN_BG), anchor="lm")
    a3 = ease((lt - 1.9) / 0.3)
    if a3 > 0:
        para(d, X0, 870, "WordPress'i güncellemek bu açığı kapatmıyor.", size=44, w=500, col=mix(FG, a3))
        source(d, 1010, "PHP güvenlik ekibi · 21.10.2026")


def path_row(d, y, head, txt, a):
    if a <= 0:
        return
    d.text((X0, y + (1 - a) * 14), head, font=FM(26, True), fill=mix(MUTED, a))
    d.rounded_rectangle([X0, y + 44, X0 + MAXW, y + 124], radius=12, outline=mix(RULE, a), width=2)
    d.text((X0 + 28, y + 84), txt, font=FM(32, True), fill=mix(FG, a), anchor="lm")


def s3(img, d, lt):
    step(d, 330, 1, ease(lt / 0.2))
    headline(d, X0, 380, [("Sitenin", False), (f"PHP{N}sürümüne", True), ("bak.", False)], size=92, t=lt,
             mark_a=ease((lt - 0.45) / 0.3))
    path_row(d, 640, "HOSTING PANELİ (cPanel)", "PHP Sürümünü Seç", ease((lt - 0.7) / 0.3))
    path_row(d, 820, "WORDPRESS", "Araçlar › Site Sağlığı › Bilgi", ease((lt - 1.2) / 0.3))


def s4(img, d, lt):
    d.text((X0, 330), "GÜVENLİ SÜRÜMLER", font=FM(28, True), fill=YEL)
    a = ease(lt / 0.3)
    evidence_card(img, _CARD, (W / 2, 610 + (1 - a) * 24), width=860, tilt=-1.4, a=a,
                  tag="PHP güvenlik ekibinin duyurusu · 21.10.2026")
    d = ImageDraw.Draw(img)
    for k, v in enumerate(["8.5.12", "8.4.27", "8.3.36", "8.2.35"]):
        b = ease((lt - 0.6 - k * 0.18) / 0.25)
        if b <= 0:
            continue
        x = X0 + (k % 2) * 440
        y = 890 + (k // 2) * 120
        d.rounded_rectangle([x, y, x + 410, y + 100], radius=14, fill=mix(GRN_BG, b))
        d.text((x + 205, y + 50), v, font=FM(56, True), fill=mix(GRN, b, GRN_BG), anchor="mm")
    c = ease((lt - 1.8) / 0.3)
    if c > 0:
        d.text((X0, 1150), "8.1 ve öncesi: resmî yama yok", font=FI(46, 700), fill=mix(RED, c))


def q_card(d, y, txt, a):
    if a <= 0:
        return y
    f = FI(40, 600)
    lines, cur = [], ""
    for wd in txt.split(" "):
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=f) <= MAXW - 110:
            cur = t
        else:
            lines.append(cur); cur = wd
    lines.append(cur)
    h = 36 + 52 * len(lines)
    yy = y + (1 - a) * 16
    d.rounded_rectangle([X0, yy, X0 + MAXW, yy + h], radius=14, fill=mix(PANEL, a))
    d.rectangle([X0, yy + 10, X0 + 6, yy + h - 10], fill=mix(YEL, a, PANEL))
    d.text((X0 + 34, yy + 18), "?", font=FM(42, True), fill=mix(YEL, a, PANEL))
    for j, ln in enumerate(lines):
        d.text((X0 + 90, yy + 20 + j * 52), ln, font=f, fill=mix(FG, a, PANEL))
    return y + h


def s5(img, d, lt):
    step(d, 330, 2, ease(lt / 0.2))
    headline(d, X0, 380, [("Hosting", False), (f"firmana{N}yazılı", True), ("sor.", False)], size=88, t=lt,
             mark_a=ease((lt - 0.4) / 0.3))
    y = 610
    y = q_card(d, y, "21 Ekim PHP güvenlik güncellemesi sunucuma uygulandı mı?", ease((lt - 0.6) / 0.25)) + 22
    y = q_card(d, y, "PHP servisleri yeniden başlatıldı mı?", ease((lt - 1.2) / 0.25)) + 22
    q_card(d, y, "Sürümüm 8.1 ya da eskiyse ne zaman taşınıyor?", ease((lt - 1.8) / 0.25))


def s6(img, d, lt):
    step(d, 330, 3, ease(lt / 0.2))
    headline(d, X0, 380, [("Şifreleri", False), ("yenile,", False), (f"iki{N}adımlıyı{N}aç.", True)], size=88, t=lt,
             mark_a=ease((lt - 0.5) / 0.3))
    a = ease((lt - 0.9) / 0.3)
    if a > 0:
        d.text((X0, 650), "NEDEN?", font=FM(26, True), fill=mix(MUTED, a))
        para(d, X0, 700, "Açık, sunucu belleğindeki parola ve anahtarları da okuyabiliyor.", size=50, w=600,
             col=mix(FG, a))
        source(d, 920, "Wiz araştırmacıları · 21.10.2026")
    b = ease((lt - 1.8) / 0.3)
    if b > 0:
        for k, txt in enumerate(["yönetici + veritabanı şifresi", "panel ve e-posta hesabı"]):
            y = 990 + k * 80
            d.text((X0, y), "+", font=FM(40, True), fill=mix(GRN, b))
            d.text((X0 + 56, y + 2), txt, font=FI(42, 600), fill=mix(FG, b))


def s7(img, d, lt):
    d.text((X0, 330), "TAM KONTROL LİSTESİ", font=FM(28, True), fill=MUTED)
    para(d, X0, 400, "Yorumlara", size=80, w=800, col=mix(FG, ease(lt / 0.2)))
    a = ease((lt - 0.25) / 0.3)
    f = FI(230, 850)
    tw = track_len(d, "LİSTE", f, -0.045)
    marker(d, (X0 - 10, 520, X0 + tw + 20, 790), seed=11, a=a)
    big_number(d, X0, 500, "LİSTE", size=230, col=BG if a > 0.6 else FG, a=1)
    b = ease((lt - 0.9) / 0.3)
    para(d, X0, 850, "yaz; hostinge sorulacaklar, sürüm kontrolü ve resmî linkler DM'de.", size=46, w=600,
         col=mix(FG, b))


def s8(img, d, lt):
    headline(d, X0, 330, [("Sitesi", False), ("olan", False), (f"birine{N}gönder.", True)], size=96, t=lt,
             mark_a=ease((lt - 0.4) / 0.3))
    for k, (key, txt) in enumerate([("A", "kontrol ettim, güvendeyim"), ("B", "şimdi bakıyorum")]):
        a = ease((lt - 0.8 - k * 0.15) / 0.25)
        if a <= 0:
            continue
        yy = 600 + k * 140
        d.rounded_rectangle([X0, yy, X0 + MAXW, yy + 110], radius=18, outline=mix(YEL if k else FG, a), width=3)
        d.text((X0 + 34, yy + 55), key, font=FM(44, True), fill=mix(YEL, a), anchor="lm")
        d.text((X0 + 100, yy + 55), txt, font=FI(46, 700), fill=mix(FG, a), anchor="lm")
    c = ease((lt - 1.6) / 0.3)
    if c > 0:
        d.text((X0, 930), "ne_yapmali()  ·  büyük olayda: ne yapmalı  ·  takip et", font=FM(25, True),
               fill=mix(MUTED, c))


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
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
    img = vignette(camera(img, t, t - STARTS[i], seed=61 + i))
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
                 [("WordPress'i güncellemek", False), (f"bu{N}sefer{N}yetmiyor", True)], theme="yellow",
                 sub="PHP2Shell: site sahibi ne yapmalı? 3 adım")
        sys.exit()
    vid = f"{OUT}/video_sessiz.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                           "-preset", "medium", vid], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        ff.stdin.write(frame(i / FPS).tobytes())
    ff.stdin.close(); ff.wait()
    rms, style, desc = make_music(f"{OUT}/muzik.wav", DUR, drop=STARTS[1], arp_start=STARTS[2], cta=STARTS[6],
                                  style="gerilim", seed="2026-10-22 ek php2shell wordpress", voice=f"{OUT}/ses/ses.wav",
                                  whooshes=(STARTS[3], STARTS[6]),
                                  events=[("ping", 0.2), ("ticks", STARTS[1] + 0.5, 5), ("type", STARTS[2] + 0.7, 8),
                                          ("chime", STARTS[3] + 0.6), ("success", STARTS[7] + 0.8)])
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", f"{OUT}/muzik.wav", "-c:v", "libx264",
                    "-crf", "22", "-maxrate", "14M", "-bufsize", "28M", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
                    "-shortest", "-movflags", "+faststart", f"{OUT}/reel.mp4"], check=True)
    print("ok", round(DUR, 2), round(rms, 1), desc)
