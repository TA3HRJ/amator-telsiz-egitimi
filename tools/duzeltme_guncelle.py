#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KEGM duzeltme onerisini C bulgulariyla gunceller (faz 5).

Kullanim:
    python tools/duzeltme_guncelle.py

Girdi : KEGM_Soru_Bankasi_Duzeltme_Onerisi_v1.1.pptx  (9 A-B bulgusu)
        icerik/KEGM_C_bulgulari.json                  (7 C bulgusu + ortak notlar)
Cikti : KEGM_Soru_Bankasi_Duzeltme_Onerisi_v1.2.pptx  (16 bulgu)

Belge SIFIRDAN URETILMEZ, mevcut dosya uzerinde duzenlenir. Sebep: dokumandaki
dokuz bulgunun gerekce ve talep metinleri kuruma sunulmak uzere ozenle yazilmis;
yeniden uretim bu metni kaybetme riski tasir. Betik yalnizca kapak/ozet/kok neden/
talep metinlerini gunceller ve yedi yeni bulgu slaydini bulgu 9'dan sonra ekler.
"""

import copy
import json
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Pt

KOK = Path(__file__).resolve().parent.parent
KAYNAK = KOK / "KEGM_Soru_Bankasi_Duzeltme_Onerisi_v1.1.pptx"
HEDEF = KOK / "KEGM_Soru_Bankasi_Duzeltme_Onerisi_v1.2.pptx"
ICERIK = KOK / "icerik" / "KEGM_C_bulgulari.json"
SURUM_METNI = "Hazırlayan: Amatör telsiz camiası — gönüllü katkı  ·  Sürüm 1.2 · 7 Eylül 2026"

LACIVERT = RGBColor(0x1F, 0x38, 0x64)
BEYAZ = RGBColor(0xFF, 0xFF, 0xFF)
KOYU = RGBColor(0x22, 0x22, 0x22)
KIRMIZI = RGBColor(0xA9, 0x2B, 0x2B)
YESIL = RGBColor(0x2E, 0x7D, 0x32)
TURUNCU = RGBColor(0xC0, 0x50, 0x00)
GRI = RGBColor(0x59, 0x59, 0x59)
SOL_ZEMIN = RGBColor(0xF7, 0xF9, 0xFB)
SAG_ZEMIN = RGBColor(0xE2, 0xEF, 0xDA)

SLAYT_G = 12191695
BASLIK_Y = 777240
SOL = (457200, 960120, 5364345, 5440680)
SAG = (6050145, 960120, 5684350, 5440680)
UST_YAZI = (365760, 109728, 11460175, 548640)
ALT_YAZI = (365760, 6492240, 11460175, 274320)


def kos(para, metin, punto, kalin, renk):
    r = para.add_run()
    r.text = metin
    r.font.size = Pt(punto)
    r.font.bold = kalin
    r.font.color.rgb = renk
    return r


def kutu(slayt, l, t, w, h, zemin):
    sh = slayt.shapes.add_shape(1, Emu(l), Emu(t), Emu(w), Emu(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = zemin
    sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def metni_degistir(slayt, eski_bas, yeni_metin):
    """Belirli bir metinle baslayan paragrafi tek parca hâlinde yeniden yazar."""
    for sh in slayt.shapes:
        if not sh.has_text_frame:
            continue
        for para in sh.text_frame.paragraphs:
            metin = "".join(r.text for r in para.runs)
            if metin.strip().startswith(eski_bas):
                ilk = para.runs[0]
                ilk.text = yeni_metin
                for r in para.runs[1:]:
                    r.text = ""
                return True
    return False


def bulgu_slaydi(prs, b):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    kutu(s, 0, 0, SLAYT_G, BASLIK_Y, LACIVERT)

    ust = s.shapes.add_textbox(Emu(UST_YAZI[0]), Emu(UST_YAZI[1]), Emu(UST_YAZI[2]), Emu(UST_YAZI[3]))
    ust.text_frame.word_wrap = True
    kos(ust.text_frame.paragraphs[0],
        "BULGU %d   ·   %s Soru Bankası, Soru %d — %s" % (b["no"], b["banka"], b["soru_no"], b["baslik"]),
        20, True, BEYAZ)

    sol = kutu(s, *SOL, zemin=SOL_ZEMIN)
    tf = sol.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Emu(274320)
    tf.margin_top = tf.margin_bottom = Emu(228600)
    tf.vertical_anchor = MSO_ANCHOR.TOP
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    p.space_after = Pt(10)
    kos(p, "ORİJİNAL SORU", 13, True, LACIVERT)
    p = tf.add_paragraph()
    p.alignment = PP_ALIGN.LEFT
    p.space_after = Pt(12)
    kos(p, b["soru"], 13.5, True, KOYU)
    for harf in "abcd":
        if harf not in b["siklar"]:
            continue
        resmi = b["resmi"].lower() == harf
        p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(7)
        kos(p, "%s)  %s" % (harf, b["siklar"][harf]), 13.5, resmi, KIRMIZI if resmi else KOYU)
        if resmi:
            kos(p, "   ← Resmî cevap anahtarı", 12, True, KIRMIZI)

    sag = kutu(s, *SAG, zemin=SAG_ZEMIN)
    tf2 = sag.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = Emu(274320)
    tf2.margin_top = tf2.margin_bottom = Emu(228600)
    tf2.vertical_anchor = MSO_ANCHOR.TOP
    q = tf2.paragraphs[0]
    q.alignment = PP_ALIGN.LEFT
    q.space_after = Pt(8)
    kos(q, "GEREKÇE / KANIT", 13, True, YESIL)
    q = tf2.add_paragraph()
    q.alignment = PP_ALIGN.LEFT
    q.space_after = Pt(14)
    kos(q, b["gerekce"], 13, False, KOYU)
    q = tf2.add_paragraph()
    q.alignment = PP_ALIGN.LEFT
    q.space_after = Pt(8)
    kos(q, "ÖNERİLEN DÜZELTME", 13, True, TURUNCU)
    q = tf2.add_paragraph()
    q.alignment = PP_ALIGN.LEFT
    kos(q, b["duzeltme"], 13, False, KOYU)

    alt = s.shapes.add_textbox(Emu(ALT_YAZI[0]), Emu(ALT_YAZI[1]), Emu(ALT_YAZI[2]), Emu(ALT_YAZI[3]))
    kos(alt.text_frame.paragraphs[0], "KEGM Düzeltme Önerisi — Bulgu %d" % b["no"], 10, False, GRI)
    return s


def satir_ekle(tablo, degerler, sablon=None):
    """Tabloya yeni satir ekler.

    Bicim, verilen sablon satirindan kopyalanir. Sablon verilmezse son satir
    kullanilir; bos tabloda son satir BASLIK satiri oldugu icin yeni satirlar
    baslik bicimini aliyordu -- C ozet tablosunda sablon acikca verilir.
    """
    yeni = copy.deepcopy(sablon if sablon is not None else tablo._tbl.tr_lst[-1])
    tablo._tbl.append(yeni)
    satir = tablo.rows[len(tablo.rows) - 1]
    for hucre, deger in zip(satir.cells, degerler):
        tf = hucre.text_frame
        para = tf.paragraphs[0]
        if para.runs:
            para.runs[0].text = deger
            for r in para.runs[1:]:
                r.text = ""
        else:
            kos(para, deger, 12, False, KOYU)
        for fazla in tf.paragraphs[1:]:
            for r in fazla.runs:
                r.text = ""


def satirlari_sil(tablo, bastan_kac_kalsin):
    """Baslik disinda kalan veri satirlarini siler."""
    for tr in list(tablo._tbl.tr_lst[bastan_kac_kalsin:]):
        tablo._tbl.remove(tr)


def slayt_kopyala(prs, kaynak):
    """Sekilleri XML duzeyinde kopyalayarak yeni slayt uretir (resim yok)."""
    yeni = prs.slides.add_slide(kaynak.slide_layout)
    for sh in list(yeni.shapes):
        sh._element.getparent().remove(sh._element)
    for sh in kaynak.shapes:
        yeni.shapes._spTree.append(copy.deepcopy(sh._element))
    return yeni


def slayt_sirala(prs, kaynak_indeksleri, hedef_indeks):
    """Sonda duran slaytlari istenen konuma tasir."""
    lst = prs.slides._sldIdLst
    ogeler = list(lst)
    tasinan = [ogeler[i] for i in kaynak_indeksleri]
    for t in tasinan:
        lst.remove(t)
    kalan = list(lst)
    for k, t in enumerate(tasinan):
        lst.insert(hedef_indeks + k, t)
    return len(kalan) + len(tasinan)


def main():
    veri = json.loads(ICERIK.read_text(encoding="utf-8"))
    bulgular = veri["bulgular"]
    prs = Presentation(KAYNAK)
    onceki = len(prs.slides._sldIdLst)

    # 1) Kapak
    metni_degistir(prs.slides[0], "A-B Sınıfı Düzenlemeler",
                   "A-B ve C Sınıfı Düzenlemeler, İşletme ve Teknik Soru Bankaları — 16 Bulgu")
    metni_degistir(prs.slides[0], "Hazırlayan:", SURUM_METNI)

    # 2) Amac ve yontem
    metni_degistir(prs.slides[1], "•  Bu belge",
                   "•  Bu belge, KEGM'nin amatör telsizcilik sınav hazırlığında kullanılan altı soru "
                   "bankasının — A-B ve C sınıfı Ulusal ve Uluslararası Düzenlemeler, İşletme ve Teknik "
                   "— bağımsız olarak yeniden çözülmesi sonucunda tespit edilen hataları içerir.")
    metni_degistir(prs.slides[1], "•  390 sorunun",
                   "•  661 sorunun büyük çoğunluğunda (645/661) resmî cevap anahtarı ile bağımsız "
                   "hesap/analiz tam olarak örtüşmüştür; aşağıdaki on altı bulgu, örtüşmeyen ya da "
                   "dayanağı güncelliğini yitirmiş sorulardır.")

    # 3) Ozet: 16 satir tek tabloya sigmiyor, ozet ikiye bolunur.
    #    Birinci slayt A-B bulgulari (mevcut tablo), ikincisi C bulgulari.
    ozet1 = prs.slides[2]
    metni_degistir(ozet1, "BULGULARIN ÖZETİ", "BULGULARIN ÖZETİ (1/2) — A-B Sınıfı")
    metni_degistir(ozet1, "(*)",
                   "(*) Soru 46 ve 66'da iki olası düzeltme yolu vardır — soru metni/değerleri mi, "
                   "yoksa cevap anahtarı mı düzeltilmeli. (†) İşletme 22'de soru metninin düzeltilmesi "
                   "önerilmektedir. C sınıfı bulguları sonraki slayttadır.")

    ozet2 = slayt_kopyala(prs, ozet1)
    metni_degistir(ozet2, "BULGULARIN ÖZETİ", "BULGULARIN ÖZETİ (2/2) — C Sınıfı")
    tablo2 = None
    for sh in ozet2.shapes:
        if sh.has_table:
            tablo2 = sh.table
            break
    veri_sablonu = copy.deepcopy(tablo2._tbl.tr_lst[1])   # silmeden once bicim ornegi
    satirlari_sil(tablo2, 1)
    for b in bulgular:
        satir_ekle(tablo2, b["ozet"], veri_sablonu)
    metni_degistir(ozet2, "(*)",
                   "(†) C Teknik 86'da soru metninin düzeltilmesi önerilmektedir. Ayrıca Bulgu 2 "
                   "(A-B Düzenlemeler 42) ve Bulgu 3 (A-B Düzenlemeler 60) ile aynı sorular, C sınıfı "
                   "Düzenlemeler bankasında 27 ve 37 numarayla ve aynı resmî cevapla yer almaktadır.")
    metni_degistir(ozet2, "KEGM Düzeltme Önerisi — Bulguların Özeti",
                   "KEGM Düzeltme Önerisi — Bulguların Özeti (C Sınıfı)")
    slayt_sirala(prs, [len(prs.slides._sldIdLst) - 1], 3)

    # 4) Yedi bulgu slaydi -- once sona eklenir, sonra bulgu 9'dan sonraya tasinir
    for b in bulgular:
        bulgu_slaydi(prs, b)
    toplam = len(prs.slides._sldIdLst)
    yeni_indeksler = list(range(toplam - len(bulgular), toplam))
    slayt_sirala(prs, yeni_indeksler, 13)   # ozet ikiye bolundugu icin bulgu 9 artik 13. sirada biter

    # 5) Kok neden -- kapsam siniri artik gecerli degil
    metni_degistir(prs.slides[len(prs.slides._sldIdLst) - 2], "▪  Kapsam sınırı.",
                   "▪  Kapsam. Bu sürümde inceleme C sınıfı üç soru bankasına da genişletilmiştir. "
                   "Bulgu 10-16 yalnızca C sınıfı bankalarında görülmektedir; Bulgu 2 ve 3'teki sorular "
                   "ise her iki sınıfın bankasında da aynı hâliyle yer almaktadır.")

    # 6) Talep
    metni_degistir(prs.slides[len(prs.slides._sldIdLst) - 1], "•  Adaylar hâlihazırda",
                   "•  C sınıfı bankalarındaki Bulgu 10-16'nın da düzeltilmesini — özellikle Teknik 73 "
                   "ve 74'te doğru sonucun şıklar arasında bulunmadığını,")
    son = prs.slides[len(prs.slides._sldIdLst) - 1]
    for sh in son.shapes:
        if sh.has_text_frame and "saygıyla" in sh.text_frame.text:
            tf = sh.text_frame
            # Paragraf nesneleri her erisimde yeniden uretildigi icin .index()
            # calismaz; konum bastan sayilarak bulunur.
            hedef_i = None
            for i, para in enumerate(tf.paragraphs):
                if "saygıyla" in "".join(r.text for r in para.runs):
                    hedef_i = i
                    break
            if hedef_i is not None:
                hedef_p = tf.paragraphs[hedef_i]._p
                yeni_p = copy.deepcopy(tf.paragraphs[hedef_i - 1]._p)
                hedef_p.addprevious(yeni_p)
                eklendi = tf.paragraphs[hedef_i]
                if eklendi.runs:
                    eklendi.runs[0].text = ("•  Adaylar hâlihazırda bu dosyalarla çalıştığından, yayımda "
                                            "kalan soru dosyalarının güncellenmesini veya yayımdan "
                                            "kaldırılmasını,")
                    for r in eklendi.runs[1:]:
                        r.text = ""
            break

    prs.save(str(HEDEF))
    print("%s -> %s" % (KAYNAK.name, HEDEF.name))
    print("slayt: %d -> %d   (7 yeni bulgu slaydi)" % (onceki, len(prs.slides._sldIdLst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
