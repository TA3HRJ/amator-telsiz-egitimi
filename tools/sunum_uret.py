#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C sinifi sunumlarini uretir (faz 4).

Kullanim:
    python tools/sunum_uret.py

Girdi:
  tools/cikti/esleme_C.json          -- her C sorusu icin yapilacak is (faz 2)
  tools/cikti/sekil/*.png            -- cikarilan sekiller (faz 4/1)
  icerik/C_*.json                    -- sifirdan yazilan aciklamalar (faz 3)
  icerik/C_sik_duzeltme.json         -- sik kumesi farkli olan 12 soru
  Amator_Telsizcilik_A-B_*.pptx      -- ortak sorularin metni ve gorsel dili

Cikti: Amator_Telsizcilik_C_<Konu>_Sinav_Hazirlik_v1.0.pptx

Bicim A-B setinden birebir alinmistir (renkler, punto, kutu konumlari); iki set yan
yana durdugunda ayni urun gibi gorunmeli. Slaytlar sifirdan kurulur, A-B slaytlari
klonlanmaz: klonlama iliskili nesneler (resim) yuzunden kirilgan, uretim ise
esleme tablosundan deterministik.
"""

import json
import re
import sys
import zipfile
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Pt

KOK = Path(__file__).resolve().parent.parent
CIKTI = Path(__file__).resolve().parent / "cikti"
SEKIL = CIKTI / "sekil"
ICERIK = KOK / "icerik"
SURUM = "v1.0"

KONULAR = [
    ("Duzenlemeler", "Ulusal ve Uluslararası Düzenlemeler",
     "C_sinifi_ulusal_ve_uluslararasi_duzenlemeler_soru_bankasi",
     "Amator_Telsizcilik_A-B_Duzenlemeler_Sinav_Hazirlik_v1.1.pptx",
     ["C_Duzenlemeler.json"]),
    ("Isletme", "İşletme",
     "C_sinifi_isletme_soru_bankasi",
     "Amator_Telsizcilik_A-B_Isletme_Sinav_Hazirlik_v1.1.pptx",
     ["C_Isletme.json"]),
    ("Teknik", "Teknik",
     "C_sinifi_teknik_soru_bankasi",
     "Amator_Telsizcilik_A-B_Teknik_Sinav_Hazirlik_v1.1.pptx",
     ["C_Teknik_metin.json", "C_Teknik_gorsel.json"]),
]

# --- A-B setinden alinan gorsel dil ---
LACIVERT = RGBColor(0x1F, 0x38, 0x64)
ACIK_MAVI = RGBColor(0xD6, 0xE4, 0xF0)
BEYAZ = RGBColor(0xFF, 0xFF, 0xFF)
KOYU = RGBColor(0x22, 0x22, 0x22)
YESIL = RGBColor(0x2E, 0x7D, 0x32)
TURUNCU = RGBColor(0xC0, 0x50, 0x00)
GRI = RGBColor(0x59, 0x59, 0x59)
KAYNAK_GRI = RGBColor(0x40, 0x40, 0x40)
SOL_ZEMIN = RGBColor(0xF7, 0xF9, 0xFB)
SAG_ZEMIN = RGBColor(0xE2, 0xEF, 0xDA)
UYARI_ZEMIN = RGBColor(0xFC, 0xE4, 0xD6)

BOLUM_BASLIK_Y = 1005840
BOLUM_BASLIK = (457200, 164592, 11277295, 731520)
BOLUM_GOVDE = (640080, 1371600, 10911535, 4114800)
BOLUM_KAYNAK = (640080, 5623560, 10911535, 914400)

SLAYT_G, SLAYT_Y = 12191695, 6858000
BASLIK_Y = 640080
SOL = (457200, 960120, 5608179, 5394960)
SAG = (6339699, 960120, 5394796, 5394960)
UST_YAZI = (365760, 73152, 11460175, 502920)
ALT_YAZI = (365760, 6492240, 11460175, 274320)

SORU_BASLIGI = re.compile(r"^Soru\s+(\d+)\s*(?:·\s*(.*))?$")
SIK_SATIRI = re.compile(r"^([a-d])\)\s*(.*)$", re.S)
DOGRU_ISARETI = "✓"


# ----------------------------------------------------------------- A-B okuma
def ab_slaytlari(pptx):
    """A-B sunumundan soru no -> {blok, govde, siklar, dogru, aciklama, kaynak, uyari}."""
    sorular = {}
    with zipfile.ZipFile(pptx) as z:
        adlar = sorted((a for a in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", a)),
                       key=lambda a: int(re.search(r"slide(\d+)", a).group(1)))
        for ad in adlar:
            xml = z.read(ad).decode("utf-8")
            paragraflar = []
            for p in re.findall(r"<a:p>(.*?)</a:p>", xml, re.S):
                t = "".join(re.findall(r"<a:t>(.*?)</a:t>", p, re.S)).strip()
                if t:
                    paragraflar.append(t)
            # "Soru N" basligi her zaman ilk paragraf DEGIL; bazi slaytlarda XML
            # siralamasi ACIKLAMA kutusunu one aliyor (or. A-B Teknik soru 129).
            # Bu yuzden paragraflar bastan sona taranir ve bolum, gorulen basliga
            # gore degisir; basligin once gelmesi sart degildir.
            no = None
            govde, siklar, dogru = [], {}, None
            aciklama, kaynak, uyari, blok = [], None, None, ""
            bolum = None
            for par in paragraflar:
                m = SORU_BASLIGI.match(par)
                if m:
                    no = int(m.group(1))
                    blok = (m.group(2) or "").strip()
                    bolum = "govde"
                    continue
                if par.startswith("AÇIKLAMA"):
                    bolum = "aciklama"
                    continue
                if par.startswith("Kaynak:"):
                    kaynak = par[len("Kaynak:"):].strip()
                    bolum = None
                    continue
                if par.startswith("DİKKAT"):
                    uyari = par
                    continue
                sik = SIK_SATIRI.match(par)
                if bolum == "govde" and sik:
                    harf, gv = sik.group(1), sik.group(2)
                    if DOGRU_ISARETI in gv:
                        dogru = harf.upper()
                        gv = gv.split(DOGRU_ISARETI)[0]
                    siklar[harf] = re.sub(r"\s+", " ", gv).strip()
                elif bolum == "govde":
                    govde.append(par)
                elif bolum == "aciklama":
                    aciklama.append(par)
            if no is None:
                continue
            sorular[no] = {
                "blok": blok,
                "govde": re.sub(r"\s+", " ", " ".join(govde)).strip(),
                "siklar": siklar,
                "cevap": dogru,
                "aciklama": " ".join(aciklama).strip(),
                "kaynak": kaynak or "",
                "uyari": uyari,
            }
    return sorular


# ------------------------------------------------------------- icerik birlestirme
def icerigi_kur(konu, c_dosya, ab_pptx, icerik_dosyalari):
    esleme = json.loads((CIKTI / "esleme_C.json").read_text(encoding="utf-8"))[konu]
    c_banka = json.loads((CIKTI / (c_dosya + ".json")).read_text(encoding="utf-8"))
    c_sorular = dict((s["no"], s) for s in c_banka["sorular"])
    ab = ab_slaytlari(KOK / ab_pptx)

    yazilan = {}
    for ad in icerik_dosyalari:
        for s in json.loads((ICERIK / ad).read_text(encoding="utf-8"))["sorular"]:
            yazilan[s["no"]] = s
    sik_duzeltme = json.loads((ICERIK / "C_sik_duzeltme.json").read_text(encoding="utf-8"))

    slaytlar, eksik = [], []
    for satir in esleme:
        no, eylem = satir["c_no"], satir["eylem"]
        if eylem == "YENI ACIKLAMA":
            s = yazilan.get(no)
            if not s:
                eksik.append((no, "yazili aciklama yok"))
                continue
            kayit = {
                "no": no, "blok": s["blok"], "govde": s["govde"], "siklar": s["siklar"],
                "cevap": s["cevap"], "aciklama": s["aciklama"], "kaynak": s["kaynak"],
                "uyari": s.get("uyari"), "kaynak_tipi": "yeni",
            }
        else:
            a = ab.get(satir["ab_no"])
            if not a:
                eksik.append((no, "A-B slaydi bulunamadi"))
                continue
            kayit = {
                "no": no, "blok": a["blok"], "govde": a["govde"], "siklar": dict(a["siklar"]),
                "cevap": a["cevap"], "aciklama": a["aciklama"], "kaynak": a["kaynak"],
                "uyari": a["uyari"], "kaynak_tipi": "tasindi",
            }
            if eylem == "KOPYALA + SIKLARI C'DEN AL":
                dz = sik_duzeltme.get("%s/%d" % (konu, no))
                if not dz:
                    eksik.append((no, "sik duzeltmesi yok"))
                    continue
                kayit["siklar"] = dz["siklar"]
                kayit["cevap"] = dz["cevap"]
                kayit["kaynak_tipi"] = "tasindi+sik"

        resmi = c_sorular[no]["cevap"]
        if kayit["cevap"] != resmi:
            eksik.append((no, "cevap %s, resmi anahtar %s" % (kayit["cevap"], resmi)))
        png = SEKIL / ("%s_%03d.png" % (konu, no))
        kayit["sekil"] = str(png) if png.exists() else None
        slaytlar.append(kayit)
    return slaytlar, eksik


# ------------------------------------------------------------------ cizim
def kutu(slayt, l, t, w, h, zemin):
    sh = slayt.shapes.add_shape(1, Emu(l), Emu(t), Emu(w), Emu(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = zemin
    sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def yazi_kutusu(slayt, l, t, w, h):
    sh = slayt.shapes.add_textbox(Emu(l), Emu(t), Emu(w), Emu(h))
    sh.text_frame.word_wrap = True
    return sh


def kos(para, metin, punto, kalin, renk):
    r = para.add_run()
    r.text = metin
    r.font.size = Pt(punto)
    r.font.bold = kalin
    r.font.color.rgb = renk
    return r


def buyuk_harf(metin):
    """Turkce buyuk harf: Python'un upper() metodu 'i' harfini 'I' yapiyor,
    dogrusu 'İ'. Duzeltilmezse kapakta 'TEKNIK' yaziyor."""
    return metin.replace("i", "İ").replace("ı", "I").upper()


def kapak(prs, baslik, altbaslik):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    kutu(s, 0, 0, SLAYT_G, SLAYT_Y, LACIVERT)
    kb = yazi_kutusu(s, 914400, 2286000, 10362895, 1280160)
    kos(kb.text_frame.paragraphs[0], buyuk_harf(baslik), 36, True, BEYAZ)
    ab = yazi_kutusu(s, 914400, 3291840, 10362895, 731520)
    kos(ab.text_frame.paragraphs[0], altbaslik, 20, False, ACIK_MAVI)
    yb = yazi_kutusu(s, 914400, 4343400, 10360152, 457200)
    kos(yb.text_frame.paragraphs[0],
        "Yazar: Claude Opus 5 (Anthropic)  —  Editör / Hata kontrolü: H. Erhan Özkan, TA3HRJ",
        13, False, ACIK_MAVI)
    kk = yazi_kutusu(s, 914400, 6035040, 10362895, 457200)
    kos(kk.text_frame.paragraphs[0],
        "Kaynak: KEGM Amatör Telsizcilik C Sınıfı Soru Bankası — sınav hazırlık amaçlıdır, "
        "resmî bir KEGM yayını değildir.", 13, False, ACIK_MAVI)
    return s


def bolum_slaydi(prs, konu_adi, bolum):
    """A-B setindeki 'BÖLÜM n' giris slaydinin ayni yapisi."""
    s = prs.slides.add_slide(prs.slide_layouts[6])
    kutu(s, 0, 0, SLAYT_G, BOLUM_BASLIK_Y, LACIVERT)

    bb = yazi_kutusu(s, *BOLUM_BASLIK)
    kos(bb.text_frame.paragraphs[0],
        "BÖLÜM %d: %s" % (bolum["no"], bolum["baslik"]), 25, True, BEYAZ)

    gb = yazi_kutusu(s, *BOLUM_GOVDE)
    tf = gb.text_frame
    tf.word_wrap = True
    for i, madde in enumerate(bolum["maddeler"]):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = PP_ALIGN.LEFT
        para.space_after = Pt(14)
        kos(para, "•  " + madde, 17, False, KOYU)

    kb = kutu(s, *BOLUM_KAYNAK, zemin=ACIK_MAVI)
    tf2 = kb.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = Emu(228600)
    tf2.vertical_anchor = MSO_ANCHOR.MIDDLE
    q = tf2.paragraphs[0]
    q.alignment = PP_ALIGN.LEFT
    kos(q, "Bu bölümün kaynağı: ", 13, True, LACIVERT)
    kos(q, bolum["kaynak"], 13, False, KOYU)

    alt = yazi_kutusu(s, *ALT_YAZI)
    kos(alt.text_frame.paragraphs[0],
        "%s — C Sınıfı — Bölüm %d Girişi" % (konu_adi, bolum["no"]), 10, False, GRI)
    return s


def soru_slaydi(prs, konu_adi, kayit):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    kutu(s, 0, 0, SLAYT_G, BASLIK_Y, LACIVERT)

    ust = yazi_kutusu(s, *UST_YAZI)
    p = ust.text_frame.paragraphs[0]
    kos(p, "Soru %d" % kayit["no"], 18, True, BEYAZ)
    if kayit["blok"]:
        kos(p, "   ·   " + kayit["blok"], 14, False, ACIK_MAVI)

    uyarili = bool(kayit.get("uyari"))
    sol = kutu(s, *SOL, zemin=SOL_ZEMIN)
    tf = sol.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Emu(274320)
    tf.margin_top = tf.margin_bottom = Emu(182880)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE

    p0 = tf.paragraphs[0]
    p0.alignment = PP_ALIGN.LEFT
    p0.space_after = Pt(14)
    kos(p0, kayit["govde"], 17, True, KOYU)
    for harf in "abcd":
        metin = kayit["siklar"].get(harf)
        if not metin:
            continue
        dogru = (kayit["cevap"] or "").lower() == harf
        pp = tf.add_paragraph()
        pp.alignment = PP_ALIGN.LEFT
        pp.space_after = Pt(8)
        kos(pp, "%s)  " % harf, 15, dogru, YESIL if dogru else KOYU)
        kos(pp, metin, 15, dogru, YESIL if dogru else KOYU)
        if dogru:
            kos(pp, "   ✓ Doğru cevap", 12, False, YESIL)

    if kayit.get("sekil"):
        # Sekil sol panelin ust yarisina konur, metin altina akar: metin ortalanmis
        # birakilirsa sekille cakisiyor.
        # Metin uzunsa sekil kucultulur; yoksa metin sekle giriyor.
        uzunluk = len(kayit["govde"]) + sum(len(v) for v in kayit["siklar"].values())
        en_fazla_h = 1750000 if uzunluk <= 180 else (1500000 if uzunluk <= 260 else 1250000)
        s.shapes.add_picture(kayit["sekil"], Emu(SOL[0] + 300000), Emu(SOL[1] + 130000),
                             height=Emu(en_fazla_h))
        res = s.shapes[-1]
        if res.width > SOL[2] - 600000:
            oran = (SOL[2] - 600000) / res.width
            res.width = Emu(int(res.width * oran))
            res.height = Emu(int(res.height * oran))
        res.left = Emu(SOL[0] + (SOL[2] - res.width) // 2)
        # Metin, sekil kadar asagidan baslasin; anchor ORTA kalir ki kalan bosluga
        # dengeli yerlessin. Anchor ALT birakilinca sekil ile metin arasinda buyuk
        # bir bosluk kaliyordu.
        tf.margin_top = Emu(130000 + res.height + 200000)

    sag = kutu(s, *SAG, zemin=UYARI_ZEMIN if uyarili else SAG_ZEMIN)
    tf2 = sag.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = Emu(274320)
    tf2.margin_top = tf2.margin_bottom = Emu(182880)
    tf2.vertical_anchor = MSO_ANCHOR.MIDDLE
    vurgu = TURUNCU if uyarili else YESIL

    q0 = tf2.paragraphs[0]
    q0.space_after = Pt(10)
    kos(q0, "AÇIKLAMA", 14, True, vurgu)
    q1 = tf2.add_paragraph()
    q1.space_after = Pt(10)
    kos(q1, kayit["aciklama"], 12.5 if uyarili else 13, False, KOYU)
    if uyarili:
        q2 = tf2.add_paragraph()
        q2.space_after = Pt(10)
        uy = kayit["uyari"]
        if not uy.startswith("DİKKAT"):
            uy = "DİKKAT — " + uy
        kos(q2, uy, 11, True, TURUNCU)
    q3 = tf2.add_paragraph()
    kos(q3, "Kaynak: ", 11, True, LACIVERT)
    kos(q3, kayit["kaynak"], 11, False, KAYNAK_GRI)

    alt = yazi_kutusu(s, *ALT_YAZI)
    kos(alt.text_frame.paragraphs[0], "%s — C Sınıfı — Soru %d" % (konu_adi, kayit["no"]),
        10, False, GRI)
    return s


def bos_sunum(sablon):
    """Sablonun temasini alir, slaytlarini siler."""
    prs = Presentation(sablon)
    xml = prs.slides._sldIdLst
    for sid in list(xml):
        prs.part.drop_rel(sid.rId)
        xml.remove(sid)
    return prs


def main():
    toplam_eksik = []
    for konu, konu_adi, c_dosya, ab_pptx, icerikler in KONULAR:
        slaytlar, eksik = icerigi_kur(konu, c_dosya, ab_pptx, icerikler)
        toplam_eksik += [(konu,) + e for e in eksik]
        prs = bos_sunum(KOK / ab_pptx)
        kapak(prs, konu_adi, "Amatör Telsizcilik Sınav Hazırlık Seti — C Sınıfı (%d Soru)" % len(slaytlar))
        bolumler = json.loads((ICERIK / "C_bolumler.json").read_text(encoding="utf-8"))[konu]
        girisler = dict((b["ilk_soru"], b) for b in bolumler)
        sekilli = 0
        for kayit in slaytlar:
            if kayit["no"] in girisler:
                bolum_slaydi(prs, konu_adi, girisler[kayit["no"]])
            soru_slaydi(prs, konu_adi, kayit)
            sekilli += 1 if kayit.get("sekil") else 0
        hedef = KOK / ("Amator_Telsizcilik_C_%s_Sinav_Hazirlik_%s.pptx" % (konu, SURUM))
        prs.save(str(hedef))
        print("%-14s %3d soru + %d bolum + kapak = %3d slayt, %2d sekil  ->  %s"
              % (konu, len(slaytlar), len(bolumler), len(prs.slides._sldIdLst), sekilli, hedef.name))
    if toplam_eksik:
        print("\nEKSIK/UYUMSUZ (%d):" % len(toplam_eksik))
        for e in toplam_eksik:
            print("   ", e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
