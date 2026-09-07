#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Soru bankasi PDF'lerinden soru sekillerini PNG olarak cikarir (faz 4).

Kullanim:
    python tools/sekil_cikar.py            # tools/cikti/sekil/ altina yaz
    python tools/sekil_cikar.py --rapor    # yalnizca hangi soruda sekil bulundugunu bas

A-B Teknik sunumunda cizime bagli sorularin sekli slayta GOMULU PNG olarak duruyor
(49 slayt). C sunumu icin ayni sey gerekiyor; bu betik onlari uretir.

Yontem: sekil kutusunu vektor cizimlerin sinir kutusundan bulmaya calismak kirilgan
cikti -- soru cercevesinin kenar cizgileri ve pek cok kucuk parca ayiklanamadi. Bunun
yerine METIN BOSLUGU kullanilir: bir sorunun cercevesi icinde metin blogu bulunmayan
dikey bant sekil bandidir. Bant, o bantta vektor cizim bulunmasi sartiyla kabul edilir.
Yatayda kirpma kutu genisligine sabitlenir; sekil ortali oldugu icin kenarlarda yalnizca
beyaz bosluk kalir.
"""

import json
import re
import sys
from pathlib import Path

import pymupdf

KOK = Path(__file__).resolve().parent.parent
CIKTI = Path(__file__).resolve().parent / "cikti" / "sekil"

BANKALAR = {
    "Duzenlemeler": "C_sinifi_ulusal_ve_uluslararasi_duzenlemeler_soru_bankasi.pdf",
    "Isletme": "C_sinifi_isletme_soru_bankasi.pdf",
    "Teknik": "C_sinifi_teknik_soru_bankasi.pdf",
}

SORU_BASI = re.compile(r"^\s*(\d{1,3})\)\s")
EN_AZ_BANT = 22      # bundan kisa bant sekil sayilmaz
BANT_BOSLUGU = 45    # dikeyde bu kadar bosluk ayni sekle ait sayilir
KENAR = 8            # kirpmaya eklenen pay (punto) -- etiketler icin
DPI = 300

# Otomatik bant bulma birkac soruda calismadi (kutu sinirlari yeterince temiz
# cikmadi). Bunlar icin kirpma dikdortgeni elle verildi; degerler sayfa goruntusu
# uzerinden okundu. Bicim: (konu, soru) -> (sayfa, y0, y1)
ELLE_KIRPMA = {
    ("Teknik", 48): (9, 175, 345),
    ("Teknik", 55): (10, 660, 735),
    ("Teknik", 62): (12, 158, 275),
    ("Teknik", 74): (14, 520, 625),
    ("Teknik", 14): (3, 335, 450),
    ("Teknik", 15): (3, 520, 645),
    ("Teknik", 53): (10, 240, 400),
    ("Teknik", 61): (12, 380, 450),
}


def sayfa_sorulari(sf):
    """Sayfadaki metin bloklarini ve soru baslangiclarini dondurur."""
    bloklar = [b for b in sf.get_text("blocks") if b[4].strip()]
    bloklar.sort(key=lambda b: b[1])
    basi = []
    for i, b in enumerate(bloklar):
        m = SORU_BASI.match(b[4])
        if m:
            basi.append((int(m.group(1)), i))
    return bloklar, basi


def cizimler(sf):
    """Cerceve cizgileri ayiklanmis vektor cizim dikdortgenleri."""
    kalan = []
    for c in sf.get_drawings():
        r = c["rect"]
        if r.y1 < 60 or r.y0 > sf.rect.height - 55:
            continue
        if r.x0 < 90 or r.x1 > 525:            # cercevenin dikey kenarlari
            continue
        if r.width > sf.rect.width * 0.6:      # cercevenin yatay cizgileri
            continue
        kalan.append(r)
    return kalan


SIK_SATIRI = re.compile(r"^\s*[a-d]\)")


def kutu_sinirlari(sf):
    """Soru cercevelerinin yatay cizgilerinden kutu sinirlarini cikarir.

    Cerceveler tek dikdortgen olarak degil, ayri cizgi parcalari olarak ciziliyor;
    bu yuzden genis ve ince yatay cizgilerin y degerleri toplanir.
    """
    W = sf.rect.width
    ys = set()
    for c in sf.get_drawings():
        r = c["rect"]
        if r.width > W * 0.6 and r.height < 3:
            ys.add(round(r.y0, 1))
    return sorted(ys)


def kutular(sf, bloklar, basi):
    """Her soru icin (no, kutu_y0, kutu_y1) uretir."""
    sinirlar = kutu_sinirlari(sf)
    cikti = []
    for no, i in basi:
        by = bloklar[i][1]
        ust = max([y for y in sinirlar if y <= by], default=60.0)
        alt = min([y for y in sinirlar if y > by], default=sf.rect.height - 55)
        cikti.append((no, ust, alt))
    return cikti


def sekil_bandi(sf, bloklar, y0, y1):
    """Bir soru kutusunda sekil bandini bulur.

    Band, kutu icindeki (a) vektor cizimlerin ve (b) soru/sik metni OLMAYAN metin
    bloklarinin kapladigi dikey araliktir. Ikinci kosul onemli: sekillerin uzerindeki
    etiketler ("50 ohm", "250V") de metin blogu olarak geliyor; bunlari metin sayip
    "bos bant" aramak, sekilleri gorunmez kiliyordu.
    """
    cizim = [(r.y0, r.y1) for r in cizimler(sf) if r.y0 >= y0 and r.y1 <= y1]
    if not cizim:
        return None
    ust = min(c[0] for c in cizim)
    alt = max(c[1] for c in cizim)
    # Sekil etiketleri ("50 ohm", "250V") metin blogu olarak geliyor; yalnizca cizimin
    # HEMEN yanindakiler bandi genisletir. Uzaktaki soru cumlesi kapsama alinmaz --
    # aksi halde kirpilan goruntude soru metni de gorunuyordu.
    for b in bloklar:
        if b[1] < y0 or b[3] > y1:
            continue
        metin = b[4].strip()
        if SORU_BASI.match(metin) or SIK_SATIRI.match(metin) or len(metin) > 60:
            continue
        if b[3] < ust - 22 or b[1] > alt + 22:
            continue
        ust = min(ust, b[1])
        alt = max(alt, b[3])
    parcalar = [(ust, alt)]
    if not parcalar:
        return None
    ust = min(p[0] for p in parcalar)
    alt = max(p[1] for p in parcalar)
    if alt - ust < EN_AZ_BANT:
        return None
    return ust, alt


def bankayi_isle(konu, pdf_adi, yalniz_rapor):
    d = pymupdf.open(KOK / "Soru_Bankalari" / pdf_adi)
    bulunan = {}
    for sn in range(len(d)):
        sf = d[sn]
        bloklar, basi = sayfa_sorulari(sf)
        if not basi:
            continue
        for no, ky0, ky1 in kutular(sf, bloklar, basi):
            bant = sekil_bandi(sf, bloklar, ky0, ky1)
            if bant is None:
                continue
            y0, y1 = bant
            # Kirpma soru kutusunun disina tasmasin: aksi halde cercevenin cizgisi
            # ve komsu sorunun metni goruntuye giriyordu.
            kirp = pymupdf.Rect(95, max(ky0 + 3, y0 - KENAR), 520,
                                min(ky1 - 3, y1 + KENAR))
            bulunan[no] = (sn + 1, [round(v) for v in kirp], kirp)
            if not yalniz_rapor:
                CIKTI.mkdir(parents=True, exist_ok=True)
                sf.get_pixmap(dpi=DPI, clip=kirp).save(
                    str(CIKTI / ("%s_%03d.png" % (konu, no))))
    for (k_konu, no), (sayfa, y0, y1) in ELLE_KIRPMA.items():
        if k_konu != konu:
            continue
        sf = d[sayfa - 1]
        kirp = pymupdf.Rect(95, y0, 520, y1)
        bulunan[no] = (sayfa, [round(v) for v in kirp], kirp)
        if not yalniz_rapor:
            CIKTI.mkdir(parents=True, exist_ok=True)
            sf.get_pixmap(dpi=DPI, clip=kirp).save(str(CIKTI / ("%s_%03d.png" % (konu, no))))
    return dict((k, (v[0], v[1])) for k, v in bulunan.items())


def main():
    yalniz_rapor = "--rapor" in sys.argv
    ozet = {}
    for konu, pdf in BANKALAR.items():
        bulunan = bankayi_isle(konu, pdf, yalniz_rapor)
        ozet[konu] = sorted(bulunan)
        print("%-14s %3d soruda sekil bulundu: %s" % (konu, len(bulunan), sorted(bulunan)))
    if not yalniz_rapor:
        (CIKTI / "_ozet.json").write_text(
            json.dumps(ozet, ensure_ascii=False, indent=2), encoding="utf-8")
        print("\ncikti: %s" % CIKTI)
    return 0


if __name__ == "__main__":
    sys.exit(main())
