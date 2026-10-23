"""Reel No.008 (EK, 23.10.2026 12:30) — prompt_hack(): "ChatGPT seni gereğinden fazla övüyor" → 5 komut, PROMPT→DM.
SARI kapak. Ses: Ec (ElevenLabs, Speko üzerinden). Müzik: enerjik elektro-pop."""
import json, subprocess, sys
sys.path.insert(0, "/home/claude/sablon")
from siber_v2 import *  # noqa
from muzik_uretici import make_music
from PIL import Image, ImageDraw

OUT = "/home/claude/reel_ek8"
NO, DATE, SERIES = 8, "23.10.2026", "prompt_hack()"
N = " "
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


def quote_card():
    """OpenAI'ın 29.04.2025 açıklamasındaki cümlenin birebir dizgisi (logo/arayüz taklidi yok)."""
    w, h = 820, 360
    im = Image.new("RGB", (w, h), (246, 244, 238))
    d = ImageDraw.Draw(im)
    d.text((36, 30), "OPENAI  ·  29 Apr 2025  ·  Sycophancy in GPT-4o", font=FM(22, True), fill=(110, 110, 110))
    body = "“The update we removed was overly flattering or agreeable, often described as sycophantic.”"
    f = FI(40, 600)
    y = 90
    for ln in wrap(d, body, f, w - 72):
        if "flattering" in ln:
            x0 = 36 + d.textlength(ln.split("flattering")[0], font=f)
            x1 = x0 + d.textlength("flattering", font=f)
            marker(d, (x0 - 6, y + 6, x1 + 6, y + 52), seed=5)
        d.text((36, y), ln, font=f, fill=(30, 30, 34))
        y += 54
    return im


_CARD = quote_card()


def num(d, k, a):
    big_number(d, X0, 300, f"0{k}", size=150, col=YEL, a=a)
    d.text((X0 + 200, 352), f"/ 05", font=FM(30, True), fill=mix(MUTED, a))


def prompt_box(d, y, text, a, label="KOPYALA, YAPIŞTIR"):
    if a <= 0:
        return y
    f = FM(34, True)
    lines = wrap(d, text, f, MAXW - 90)
    h = 80 + 50 * len(lines)
    yy = y + (1 - a) * 18
    d.rounded_rectangle([X0, yy, X0 + MAXW, yy + h], radius=14, fill=mix(GRN_BG, a))
    d.rectangle([X0, yy + 12, X0 + 6, yy + h - 12], fill=mix(GRN, a, GRN_BG))
    d.text((X0 + 34, yy + 22), label, font=FM(22, True), fill=mix(GRN, a, GRN_BG))
    for j, ln in enumerate(lines):
        d.text((X0 + 34, yy + 62 + j * 50), ln, font=f, fill=mix(FG, a, GRN_BG))
    return y + h


def s1(img, d, lt):
    d.text((X0, 330), "ChatGPT  ·  Gemini  ·  Claude", font=FM(28, True), fill=mix(MUTED, ease(lt / 0.2)))
    headline(d, X0, 400, [("ChatGPT seni", False), (f"gereğinden{N}fazla", True), ("övüyor.", False)], size=112,
             t=lt, mark_a=ease((lt - 0.55) / 0.3))
    a = ease((lt - 1.1) / 0.3)
    if a > 0:
        x = badge(d, X0, 820, "5 KOMUT", col=mix(YEL, a))
        badge(d, x + 16, 820, "KAYDET", col=mix(MUTED, a))


def s2(img, d, lt):
    d.text((X0, 330), "BUNU ŞİRKETİN KENDİSİ SÖYLEDİ", font=FM(28, True), fill=YEL)
    a = ease(lt / 0.3)
    evidence_card(img, _CARD, (W / 2, 590 + (1 - a) * 24), width=860, tilt=-1.5, a=a,
                  tag="OpenAI açıklaması · 29.04.2025")
    d = ImageDraw.Draw(img)
    b = ease((lt - 0.9) / 0.3)
    if b > 0:
        para(d, X0, 880, "“Geri çektiğimiz güncelleme aşırı övücü ve onaylayıcıydı.”", size=46, w=600,
             col=mix(FG, b))


def s3(img, d, lt):
    num(d, 1, ease(lt / 0.2))
    headline(d, X0, 520, [("Beni", False), (f"övme.", True)], size=104, t=lt, mark_a=ease((lt - 0.35) / 0.3))
    prompt_box(d, 680, "Beni övme. Bu fikrin en zayıf 3 noktasını söyle, sonra nasıl düzelteceğimi yaz.",
               ease((lt - 0.6) / 0.3))


def s4(img, d, lt):
    num(d, 2, ease(lt / 0.2))
    headline(d, X0, 520, [("Uydurmayı", False), (f"yakala.", True)], size=104, t=lt, mark_a=ease((lt - 0.35) / 0.3))
    y = prompt_box(d, 800, "Emin olmadığın her cümlenin sonuna [?] koy.", ease((lt - 0.55) / 0.3))
    a = ease((lt - 1.2) / 0.3)
    if a > 0:
        d.text((X0, y + 40), "CEVAPTA ŞÖYLE GÖRÜNÜR", font=FM(22, True), fill=mix(MUTED, a))
        f = FI(44, 600)
        ln = "Bu özellik 2023'te eklendi"
        d.text((X0, y + 84), ln, font=f, fill=mix(FG, a))
        x = X0 + d.textlength(ln + " ", font=f)
        tw = d.textlength("[?]", font=FM(44, True))
        marker(d, (x - 6, y + 86, x + tw + 6, y + 140), seed=9, a=a)
        d.text((x, y + 88), "[?]", font=FM(44, True), fill=BG)


def s5(img, d, lt):
    num(d, 3, ease(lt / 0.2))
    headline(d, X0, 520, [("Kendi cevabını", False), (f"çürüt.", True)], size=100, t=lt,
             mark_a=ease((lt - 0.4) / 0.3))
    a = ease((lt - 0.5) / 0.3)
    if a > 0:
        f = FI(48, 700)
        d.rounded_rectangle([X0, 800, X0 + MAXW, 900], radius=14, fill=mix(RED_BG, a))
        d.text((X0 + 34, 850), "“Harika fikir, kesin tutar!”", font=f, fill=mix(FG, a, RED_BG), anchor="lm")
        s = ease((lt - 0.8) / 0.3)
        if s > 0:
            tw = d.textlength("“Harika fikir, kesin tutar!”", font=f)
            d.line([X0 + 24, 854, X0 + 24 + (tw + 20) * s, 846], fill=RED, width=7)
    prompt_box(d, 940, "Şimdi bu cevaba karşı çıkan biri ol ve en güçlü itirazı yaz.", ease((lt - 1.1) / 0.3))


def s6(img, d, lt):
    num(d, 4, ease(lt / 0.2))
    a = ease((lt - 0.15) / 0.3)
    big_number(d, X0 - 8, 470, "12", size=330, col=FG, a=a)
    b = ease((lt - 0.4) / 0.3)
    if b > 0:
        d.text((X0 + 400, 560), "yaşındakine", font=FI(64, 800), fill=mix(FG, b))
        d.text((X0 + 400, 640), "anlatır gibi", font=FI(64, 800), fill=mix(YEL, b))
    prompt_box(d, 900, "Bunu 12 yaşındaki birine anlatır gibi anlat, sonra günlük hayattan 1 örnek ver.",
               ease((lt - 0.9) / 0.3))


def s7(img, d, lt):
    num(d, 5, ease(lt / 0.2))
    a = ease((lt - 0.2) / 0.3)
    if a > 0:
        yy = 500 + (1 - a) * 20
        d.rounded_rectangle([X0, yy, X0 + MAXW, yy + 220], radius=26, fill=mix(PANEL, a), outline=mix(RULE, a), width=2)
        d.text((X0 + 34, yy + 30), "MESAJ  ·  bilinmeyen numara", font=FM(22, True), fill=mix(MUTED, a, PANEL))
        for j, ln in enumerate(["Kargonuz teslim edilemedi. Adresinizi", "güncelleyin: kisa.link/xxxx"]):
            d.text((X0 + 34, yy + 80 + j * 52), ln, font=FI(42, 600), fill=mix(FG, a, PANEL))
        d.text((X0 + MAXW - 20, yy + 30), "örnek", font=FM(22, True), fill=mix(MUTED, a, PANEL), anchor="ra")
    b = ease((lt - 0.8) / 0.25)
    if b > 0:
        d.text((X0 + MAXW - 80, 290), "?", font=FI(150, 850), fill=mix(RED, b))
    prompt_box(d, 770, "Bu mesaj dolandırıcılık mı? Şüpheli işaretleri tek tek say. (Linke tıklama.)",
               ease((lt - 1.2) / 0.3))


def s8(img, d, lt):
    d.text((X0, 330), "AMA DİKKAT", font=FM(30, True), fill=RED)
    headline(d, X0, 390, [("Bunları", False), (f"asla{N}yapıştırma.", True)], size=100, t=lt,
             mark_a=ease((lt - 0.4) / 0.3))
    for k, txt in enumerate(["şifre ve doğrulama kodu", "TC kimlik numarası", "kart ve IBAN bilgisi"]):
        a = ease((lt - 0.8 - k * 0.2) / 0.25)
        if a <= 0:
            continue
        y = 680 + k * 100
        d.rounded_rectangle([X0, y, X0 + MAXW, y + 80], radius=12, fill=mix(RED_BG, a))
        d.text((X0 + 28, y + 40), "−", font=FM(44, True), fill=mix(RED, a, RED_BG), anchor="lm")
        d.text((X0 + 90, y + 40), txt, font=FI(44, 700), fill=mix(FG, a, RED_BG), anchor="lm")
    c = ease((lt - 1.6) / 0.3)
    if c > 0:
        para(d, X0, 1010, "Mesaj örneği verirken isim ve numaraları sil.", size=40, w=500, col=mix(MUTED, c))


def s9(img, d, lt):
    d.text((X0, 330), "5 KOMUTUN TAM METNİ + BONUS", font=FM(28, True), fill=MUTED)
    para(d, X0, 400, "Yorumlara", size=80, w=800, col=mix(FG, ease(lt / 0.2)))
    a = ease((lt - 0.25) / 0.3)
    f = FI(200, 850)
    tw = track_len(d, "PROMPT", f, -0.045)
    marker(d, (X0 - 10, 520, X0 + tw + 20, 760), seed=13, a=a)
    big_number(d, X0, 505, "PROMPT", size=200, col=BG if a > 0.6 else FG, a=1)
    b = ease((lt - 0.9) / 0.3)
    para(d, X0, 820, "yaz; kopyalanabilir hâlleri ve 6. bonus komut DM'de.", size=46, w=600, col=mix(FG, b))


def s10(img, d, lt):
    headline(d, X0, 330, [("Hangisini", False), (f"ilk{N}deneyeceksin?", True)], size=96, t=lt,
             mark_a=ease((lt - 0.35) / 0.3))
    a = ease((lt - 0.6) / 0.3)
    if a > 0:
        for k in range(5):
            x = X0 + k * 172
            d.rounded_rectangle([x, 600, x + 150, 750], radius=18, outline=mix(YEL if k == 2 else FG, a), width=3)
            d.text((x + 75, 675), str(k + 1), font=FI(80, 850), fill=mix(YEL if k == 2 else FG, a), anchor="mm")
        d.text((X0, 790), "Yorumlara numarasını yaz.", font=FI(44, 700), fill=mix(FG, a))
    c = ease((lt - 1.2) / 0.3)
    if c > 0:
        d.text((X0, 900), "prompt_hack()  ·  her hafta yeni komutlar  ·  takip et", font=FM(25, True),
               fill=mix(MUTED, c))


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
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
    img = vignette(camera(img, t, t - STARTS[i], seed=83 + i))
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
                 [("ChatGPT seni", False), (f"fazla{N}övüyor", True)], theme="yellow",
                 sub="Dürüst cevap için 5 komut. Kaydet.")
        sys.exit()
    vid = f"{OUT}/video_sessiz.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                           "-preset", "medium", vid], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        ff.stdin.write(frame(i / FPS).tobytes())
    ff.stdin.close(); ff.wait()
    rms, style, desc = make_music(f"{OUT}/muzik.wav", DUR, drop=STARTS[2], arp_start=STARTS[2] + 0.4, cta=STARTS[8],
                                  style="enerjik", seed="2026-10-23 ek prompt_hack yalakalik", voice=f"{OUT}/ses/ses.wav",
                                  whooshes=(STARTS[2], STARTS[7], STARTS[8]),
                                  events=[("ping", 0.15), ("chime", STARTS[1] + 0.4), ("type", STARTS[3] + 0.7, 7),
                                          ("buzz", STARTS[7] + 0.1), ("success", STARTS[9] + 0.7)])
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", f"{OUT}/muzik.wav", "-c:v", "libx264",
                    "-crf", "24", "-maxrate", "11M", "-bufsize", "22M", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
                    "-shortest", "-movflags", "+faststart", f"{OUT}/reel.mp4"], check=True)
    print("ok", round(DUR, 2), round(rms, 1), desc)
