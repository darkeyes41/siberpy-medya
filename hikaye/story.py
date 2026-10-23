import sys
sys.path.insert(0,"/home/claude/sablon")
from siber_v2 import *
from PIL import Image, ImageDraw
def story(cover, out, top, line1, kw, dark):
    im=Image.open(cover).convert("RGB").resize((W,H))
    d=ImageDraw.Draw(im)
    bg=BG if dark else YEL; fg=YEL if dark else BG; tx=FG if dark else BG; sub=MUTED if dark else (92,76,20)
    # üst etiket
    f=FM(30,True); tw=d.textlength(top,font=f)
    d.rounded_rectangle([X0,320,X0+tw+44,384],radius=10,fill=RED)
    d.text((X0+22,352),top,font=f,fill=(255,255,255),anchor="lm")
    # alt kart
    y=1380
    d.rounded_rectangle([X0-10,y,W-X0+10,y+300],radius=26,fill=bg)
    d.text((X0+30,y+40),line1,font=FI(54,800),fill=tx)
    d.text((X0+30,y+125),"Yorumlara",font=FI(44,600),fill=tx)
    x=X0+30+d.textlength("Yorumlara ",font=FI(44,600))+16
    kwf=FI(64,850); kw_w=d.textlength(kw,font=kwf)
    marker(d,(x-8,y+118,x+kw_w+10,y+196),seed=3,col=fg)
    d.text((x,y+112),kw,font=kwf,fill=bg)
    d.text((x+kw_w+26,y+125),"yaz → DM",font=FI(44,600),fill=tx)
    d.text((X0+30,y+225),"profilde izle  ·  @siber.py",font=FM(28,True),fill=sub)
    apply_grain(im,0,strength=4).save(out,quality=92)
story(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6]=="1")
