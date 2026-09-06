#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KEGM soru bankasi PDF'lerinden soru/sik/cevap anahtari cikarimi.

Kullanim:
    python tools/cikarim.py            # tum bankalari isle, tools/cikti/ altina yaz
    python tools/cikarim.py --rapor    # yalnizca dogrulama raporu bas, dosya yazma

Karakter kodlamasi notu (bkz. docs/HANDOFF.md):
PDF'lerin metin katmaninda i-noktasiz, s-cedilli ve g-yumusak HIC YOK -- bozuk degil,
akistan tamamen dusmus. Hicbir pdftotext bayragi geri getiremez. Buna karsilik c/o/u
kurtarilabiliyor: varsayilan UTF-8 kipinde U+FFFD oluyorlar, `-enc Latin1` ile alinip
cp1254 olarak cozulurse dogru geliyorlar. Bu dosya o receteyi uygular.

Eksik harflerin tamamlanmasi bu hattin isi DEGILDIR; ayri bir adimdir ve sonucu
PDF'e karsi gozle dogrulanmalidir.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
BANKA_DIZINI = KOK / "Soru_Bankalari"
CIKTI_DIZINI = Path(__file__).resolve().parent / "cikti"

# Sayfa basligi/altligi -- soru metnine karismamali
# BUYUK HARF duyarli olmali: "c) Kiyi Emniyeti Genel Mudurlugu" gecerli bir sikti ve
# buyuk/kucuk harf duyarsiz desen bu sikki sayfa basligi sanip yutuyordu.
GURULTU = re.compile(
    r"^\s*(KIYI\s+EMN|TELS[Iİ]?Z\s+[Iİ]?[SŞ]?LETME\s+M|~\s*\d+\s*~"
    r"|[A-Z]-?\s*B?-?\s*SINIFI\b.*(BANKASI|ANAHTARI)\s*$)"
)
SORU_BASI = re.compile(r"(?<![\d.,])(\d{1,3})\)\s")
# Bosluk istege bagli: bankalarda 'c)3' ve 'd)Yozgat' gibi bitisik dizgi var.
SIK_BASI = re.compile(r"(?<![\wğüşıöçİĞÜŞÖÇ])([a-d])\)\s*")


def ham_metin(pdf: Path) -> str:
    """pdftotext -enc Latin1 ciktisini cp1254 olarak coz (bkz. modul acikamasi)."""
    ham = subprocess.run(
        ["pdftotext", "-enc", "Latin1", "-layout", str(pdf), "-"],
        capture_output=True,
        check=True,
    ).stdout
    return ham.decode("cp1254", "replace").replace("\r\n", "\n")


def govde_ve_anahtar(metin: str):
    """Metni soru govdesi ve cevap anahtari bolumu olarak ikiye ayir."""
    yer = metin.rfind("CEVAP ANAHTARI")
    if yer == -1:
        return metin, ""
    # Basligin bulundugu satirin basina kadar geri git
    satir_basi = metin.rfind("\n", 0, yer)
    return metin[:satir_basi], metin[satir_basi:]


def anahtari_coz(bolum: str) -> dict:
    """'1 C   11 D  21 C' bicimindeki tabloyu {soru_no: harf} sozlugune cevir."""
    anahtar = {}
    for no, harf in re.findall(r"(?<![\w.])(\d{1,3})\s+([A-Da-d])(?![\w)])", bolum):
        anahtar.setdefault(int(no), harf.upper())
    return anahtar


def siklari_ayir(blok: str):
    """Bir soru blogundan a-d siklarini cikar.

    Iki tuzak var:
    1. Siklar tek satirda yan yana gelebiliyor ('a) Ankara  b) Aydin  c) ...').
    2. Iki sutunlu dizgide siklar ALFABETIK SIRADA GELMIYOR -- -layout ciktisinda once
       b) ve d), sonra a) ve c) gorulebiliyor (or. C teknik 26). Bu yuzden a->b->c->d
       sirasi dayatilmaz: etiketler bulunduklari yerde alinir, her sikkin metni kendisi
       ile bir SONRAKI etiket arasindaki metindir. Sira bozuk olsa da dogru calisir.
    """
    ilk = {}
    for m in SIK_BASI.finditer(blok):
        ilk.setdefault(m.group(1), (m.start(), m.end()))
    kabul = sorted((bas, son, harf) for harf, (bas, son) in ilk.items())
    siklar = {}
    for i, (bas, son, harf) in enumerate(kabul):
        bitis = kabul[i + 1][0] if i + 1 < len(kabul) else len(blok)
        siklar[harf] = temizle(blok[son:bitis])
    return siklar, (kabul[0][0] if kabul else len(blok))


def temizle(parca: str) -> str:
    satirlar = [s.strip() for s in parca.split("\n")]
    satirlar = [s for s in satirlar if s and not GURULTU.match(s)]
    return re.sub(r"\s{2,}", " ", " ".join(satirlar)).strip()


def bankayi_coz(pdf: Path) -> dict:
    metin = ham_metin(pdf)
    govde, anahtar_bolumu = govde_ve_anahtar(metin)
    anahtar = anahtari_coz(anahtar_bolumu)

    baslangiclar = [(m.start(), m.end(), int(m.group(1))) for m in SORU_BASI.finditer(govde)]
    # Yalnizca 1'den baslayip birer birer artan diziyi soru basi say; formul/olcu
    # icindeki '2) ' benzeri yakalamalari ele
    kabul, beklenen = [], 1
    for bas, son, no in baslangiclar:
        if no == beklenen:
            kabul.append((bas, son, no))
            beklenen += 1

    sorular = []
    for i, (bas, son, no) in enumerate(kabul):
        bitis = kabul[i + 1][0] if i + 1 < len(kabul) else len(govde)
        blok = govde[son:bitis]
        siklar, sik_basi = siklari_ayir(blok)
        sorular.append(
            {
                "no": no,
                "govde": temizle(blok[:sik_basi]),
                "siklar": siklar,
                "cevap": anahtar.get(no),
            }
        )

    return {
        "kaynak": pdf.name,
        "soru_sayisi": len(sorular),
        "anahtar_sayisi": len(anahtar),
        "eksik_harf_uyarisi": "Metin katmaninda i-noktasiz/s-cedilli/g-yumusak yok; "
        "tamamlama ayri adimdir ve PDF'e karsi dogrulanmalidir.",
        "sorular": sorular,
    }


SEMBOL_SIK = re.compile(r"^[-./·\s]*$")

# Govdesi bir cizime/tabloya atif yapan sorular. Desenler i-noktasiz ve s-cedilli
# DUSMUS haliyle yazilmistir ("sekildeki" -> "ekildeki"), cunku metin katmani boyle
# geliyor (bkz. modul aciklamasi).
GORSEL_ATIF = re.compile(
    r"\b(ekilde|ekildeki|yukarid|semboller|sembolleri|diyagram|grafik|ema\b|emada)",
    re.IGNORECASE,
)
# "ne sekilde yapilir", "yukaridakilerden hangisi" gibi kaliplar cizime degil, dile ait.
# Bunlar temizlenmeden GORSEL_ATIF taranirsa metin-only sorular yanlislikla isaretlenir
# (or. C isletme 8/20/60/61 "hecelemesi ne sekilde yapilir").
GORSEL_ATIF_ISTISNA = re.compile(
    r"\b(ne|hangi|bu|ayni|o|hiçbir)\s+ekilde\b|\byukaridakilerden\b",
    re.IGNORECASE,
)


def dogrula(veri: dict) -> dict:
    """Bulgulari uc kategoriye ayirir; hepsi ayni agirlikta degildir.

    AYRISTIRMA -- hattin kendi hatasi. SIFIR olmali; degilse cikti guvenilmez.
    GORSEL     -- metin katmani yetmiyor (devre semasi, mors isaretleri, mikro simgesi
                  gibi dusen semboller). Hat duzeltemez; ilgili soru PDF'e bakilarak
                  ELLE aktarilmalidir. Sorulara "elle_aktarilmali" isareti konur.
    INCELE     -- dortten az sik. Ya dizgi ya da bankada gercek eksik; ikincisi ise
                  KEGM duzeltme onerisine bulgu adayidir.
    """
    bulgular = {"AYRISTIRMA": [], "GORSEL": [], "INCELE": []}
    sorular = veri["sorular"]
    numaralar = [s["no"] for s in sorular]

    if numaralar != list(range(1, len(numaralar) + 1)):
        eksik = sorted(set(range(1, max(numaralar) + 1)) - set(numaralar)) if numaralar else []
        bulgular["AYRISTIRMA"].append("numaralandirma kesintili; eksik: %s" % eksik)

    for s in sorular:
        etiketler = sorted(s["siklar"])
        metinler = list(s["siklar"].values())
        dolu = [m for m in metinler if m]
        elle = False

        if not s["cevap"]:
            bulgular["AYRISTIRMA"].append("soru %d: cevap anahtarinda yok" % s["no"])
        elif etiketler == ["a", "b", "c", "d"] and s["cevap"].lower() not in s["siklar"]:
            bulgular["AYRISTIRMA"].append("soru %d: cevap %s ama o etikette sik yok"
                                          % (s["no"], s["cevap"]))
        if len(s["govde"]) < 15:
            bulgular["AYRISTIRMA"].append("soru %d: govde cok kisa (%d karakter)"
                                          % (s["no"], len(s["govde"])))

        if etiketler and len(dolu) < len(metinler):
            bos = sorted(h for h, m in s["siklar"].items() if not m)
            bulgular["GORSEL"].append("soru %d: %s sikki bos -- secenek cizim"
                                      % (s["no"], "".join(bos)))
            elle = True
        elif dolu and all(SEMBOL_SIK.match(m) for m in dolu):
            bulgular["GORSEL"].append("soru %d: siklar yalnizca isaretten olusuyor "
                                      "(mors); noktalar metin katmaninda yok" % s["no"])
            elle = True
        elif len(set(dolu)) != len(dolu):
            bulgular["GORSEL"].append("soru %d: iki sik ayni metne dusuyor -- ayirt eden "
                                      "sembol (or. mikro) metin katmaninda yok" % s["no"])
            elle = True

        if GORSEL_ATIF.search(GORSEL_ATIF_ISTISNA.sub(" ", s["govde"])):
            bulgular["GORSEL"].append("soru %d: govde cizime/tabloya atif yapiyor "
                                      "-- metin tek basina yetmez" % s["no"])
            elle = True
        else:
            # Soru cumlesi '?', ':' veya ';' ile biter; sonrasinda kalan sey cizimin
            # uzerindeki etiketlerdir ("... kaç amperdir? 1A 2A 0.5A I"). Cizim var demektir.
            kesim = max(s["govde"].rfind(k) for k in "?:;")
            artik = s["govde"][kesim + 1:].strip() if kesim != -1 else ""
            if len(artik) >= 2:
                bulgular["GORSEL"].append("soru %d: govdeye cizim etiketi sizmis (%s...) "
                                          "-- cizime bagli" % (s["no"], artik[:40]))
                elle = True

        if etiketler and etiketler != ["a", "b", "c", "d"]:
            bulgular["INCELE"].append("soru %d: yalnizca %s sikki bulundu"
                                      % (s["no"], "".join(etiketler)))
            elle = True

        s["elle_aktarilmali"] = elle
    return bulgular


def main() -> int:
    yalniz_rapor = "--rapor" in sys.argv
    pdfler = sorted(BANKA_DIZINI.glob("*.pdf"))
    if not pdfler:
        print("HATA: %s altinda PDF yok" % BANKA_DIZINI)
        return 1
    if not yalniz_rapor:
        CIKTI_DIZINI.mkdir(exist_ok=True)

    ayristirma_hatasi = 0
    elle_toplam = 0
    for pdf in pdfler:
        veri = bankayi_coz(pdf)
        bulgular = dogrula(veri)
        ayristirma_hatasi += len(bulgular["AYRISTIRMA"])
        elle = [s["no"] for s in veri["sorular"] if s["elle_aktarilmali"]]
        elle_toplam += len(elle)
        veri["elle_aktarilmali_sorular"] = elle

        ozet = "temiz" if not elle and not bulgular["AYRISTIRMA"] else "%d soru elle" % len(elle)
        print("%-58s %3d soru / %3d anahtar  %s"
              % (pdf.stem, veri["soru_sayisi"], veri["anahtar_sayisi"], ozet))
        for kategori in ("AYRISTIRMA", "GORSEL", "INCELE"):
            for b in bulgular[kategori]:
                print("    [%s] %s" % (kategori, b))
        if not yalniz_rapor:
            hedef = CIKTI_DIZINI / (pdf.stem + ".json")
            hedef.write_text(json.dumps(veri, ensure_ascii=False, indent=2), encoding="utf-8")

    if not yalniz_rapor:
        print("\ncikti: %s" % CIKTI_DIZINI)
    print("ayristirma hatasi: %d  |  elle aktarilacak soru: %d"
          % (ayristirma_hatasi, elle_toplam))
    return 0 if ayristirma_hatasi == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
