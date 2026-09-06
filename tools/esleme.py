#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C sinifi sorularini A-B setiyle eslestirir (faz 2).

Kullanim:
    python tools/esleme.py            # esleme_C.json + docs/esleme_C.md uret
    python tools/esleme.py --rapor    # yalnizca ozet bas

Girdi:
  tools/cikti/*.json                  -- faz 1 ciktisi (ham banka metni)
  Amator_Telsizcilik_A-B_*.pptx       -- mevcut A-B sunumlari

A-B sunumlari, banka PDF'lerinden farkli olarak TAM ve DOGRU Turkce metin tasir
(i-noktasiz, s-cedilli, g-yumusak yerinde). Ortak sorularda slayt metni hazir
kaynaktir; bu yuzden esleme banka-banka degil, C BANKASI <-> A-B SLAYTI arasinda
yapilir ve sonuca slayt numarasi da yazilir.

Karsilastirma harf uzerinden DEGIL sik metni uzerinden yapilir: ayni soru govdesi
farkli sik kumesi tasiyabiliyor (bkz. docs/HANDOFF.md).
"""

import difflib
import json
import re
import sys
import zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
CIKTI = Path(__file__).resolve().parent / "cikti"
KARAR_DOSYASI = Path(__file__).resolve().parent / "karar_yakin_eslesme.json"
YAKINLIK_ESIGI = 0.85

KONULAR = [
    ("Duzenlemeler",
     "C_sinifi_ulusal_ve_uluslararasi_duzenlemeler_soru_bankasi",
     "A-B_sinifi_ulusal_ve_uluslararasi_duzenlemeler_soru_bankasi",
     "Amator_Telsizcilik_A-B_Duzenlemeler_Sinav_Hazirlik_v1.1.pptx"),
    ("Isletme",
     "C_sinifi_isletme_soru_bankasi",
     "A-B_sinifi_isletme_soru_bankasi",
     "Amator_Telsizcilik_A-B_Isletme_Sinav_Hazirlik_v1.1.pptx"),
    ("Teknik",
     "C_sinifi_teknik_soru_bankasi",
     "A-B_sinifi_teknik_soru_bankasi",
     "Amator_Telsizcilik_A-B_Teknik_Sinav_Hazirlik_v1.1.pptx"),
]

SORU_BASLIGI = re.compile(r"^Soru\s+(\d+)\s*(?:·\s*(.*))?$")
SIK_SATIRI = re.compile(r"^([a-d])\)\s*(.*)$", re.S)
DOGRU_ISARETI = "✓"


def anahtarla(metin):
    """Banka metni ile slayt metnini karsilastirilabilir hale getirir.

    Banka PDF'inde i-noktasiz 'i'ye donusmus, s-cedilli ve g-yumusak ise tamamen
    dusmustur. Ayni donusum slayt metnine de uygulanirsa iki taraf ayni tabanda
    bulusur. c/o/u iki tarafta da dogru oldugu icin korunur.
    """
    metin = metin.replace("İ", "i").replace("I", "ı").lower()
    metin = metin.replace("ı", "i").replace("ş", "").replace("ğ", "")
    return re.sub(r"[^a-z0-9çöü]+", "", metin)


def slayt_paragraflari(xml):
    paragraflar = []
    for p in re.findall(r"<a:p>(.*?)</a:p>", xml, re.S):
        metin = "".join(re.findall(r"<a:t>(.*?)</a:t>", p, re.S)).strip()
        if metin:
            paragraflar.append(metin)
    return paragraflar


def deck_oku(pptx):
    """Sunumdan soru no -> {slayt, govde, siklar, dogru_harf, blok} sozlugu."""
    sorular = {}
    with zipfile.ZipFile(pptx) as z:
        adlar = [a for a in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", a)]
        adlar.sort(key=lambda a: int(re.search(r"slide(\d+)", a).group(1)))
        for ad in adlar:
            no_slayt = int(re.search(r"slide(\d+)", ad).group(1))
            paragraflar = slayt_paragraflari(z.read(ad).decode("utf-8"))
            # "Soru N" basligi her zaman ilk paragraf DEGIL: bazi slaytlarda XML
            # siralamasi ACIKLAMA kutusunu one aliyor (or. Teknik slayt 140 / soru 129).
            # Yalnizca ilk paragrafa bakan surum bu sorulari tamamen kaciriyordu.
            basi, bas_i = None, -1
            for i, par in enumerate(paragraflar):
                m = SORU_BASLIGI.match(par)
                if m:
                    basi, bas_i = m, i
                    break
            if not basi:
                continue  # bolum girisi veya kapak
            no = int(basi.group(1))
            govde, siklar, dogru = [], {}, None
            for par in paragraflar[bas_i + 1:]:
                sik = SIK_SATIRI.match(par)
                if sik:
                    harf, gv = sik.group(1), sik.group(2)
                    if DOGRU_ISARETI in gv:
                        dogru = harf.upper()
                        gv = gv.split(DOGRU_ISARETI)[0]
                    siklar[harf] = re.sub(r"\s+", " ", gv).strip()
                elif siklar:
                    break  # siklardan sonrasi ACIKLAMA bolumu
                else:
                    govde.append(par)
            sorular[no] = {
                "slayt": no_slayt,
                "blok": (basi.group(2) or "").strip(),
                "govde": re.sub(r"\s+", " ", " ".join(govde)).strip(),
                "siklar": siklar,
                "dogru_harf": dogru,
            }
    return sorular


def deck_bankayla_tutuyor_mu(deck, banka):
    """Slayt numaralandirmasi banka numaralandirmasiyla ortusuyor mu?

    Govde metinlerinin BIREBIR tutmasi beklenmez: A-B setinde cizime bagli sorularin
    govdesi bilerek yeniden yazilmis, sekil sozle tarif edilmistir (or. Teknik 15
    "Sekildeki (8 [sekiz] seklinde iki loba sahip) yayilim kalibi..."). Bu bir hata
    degil, setin yontemidir. Bu yuzden yalnizca NUMARA ortusmesi ve cevap harfi
    tutarliligi denetlenir.
    """
    uyusmazlik = []
    bankaca = dict((s["no"], s) for s in banka["sorular"])
    for no in sorted(set(bankaca) - set(deck)):
        uyusmazlik.append("banka sorusu %d sunumda yok" % no)
    for no in sorted(set(deck) - set(bankaca)):
        uyusmazlik.append("sunum sorusu %d bankada yok" % no)
    for no, slayt in sorted(deck.items()):
        b = bankaca.get(no)
        if b and slayt["dogru_harf"] and b["cevap"] and slayt["dogru_harf"] != b["cevap"]:
            uyusmazlik.append("soru %d: sunumda isaretli sik %s, resmi anahtar %s"
                              % (no, slayt["dogru_harf"], b["cevap"]))
    return uyusmazlik


def sik_kumesi(siklar):
    return set(anahtarla(m) for m in siklar.values() if m)


def eylem_belirle(s):
    """Satirdan yapilacak isi turetir.

    "yakin" eslesmeler OTOMATIK KULLANILMAZ. Sebep olculdu: C Isletme 37 ile A-B
    Isletme 60'in benzerligi 0.98 ama sorular farkli ("VE cagri isareti oneki" -
    Kanada, "VK cagri isareti oneki" - Avustralya). Tek harflik ayrimi olan sorularda
    yuksek benzerlik yanlis eslesme demek; bu satirlar insana birakilir.

    CELISKI yalnizca sik kumesi AYNI iken resmi cevaplar farkliysa anlamlidir. Sik
    kumesi farkliysa cevabin farkli olmasi zaten beklenir, celiski degildir.
    """
    if s["durum"] == "yeni":
        return "YENI ACIKLAMA"
    if s["durum"] == "yakin":
        if s["yakin_karar"] == "farkli":
            return "YENI ACIKLAMA"
        if s["yakin_karar"] != "ayni":
            return "YAKIN ESLESME - DOGRULA"
    if s["ab_bulgu_devrediyor"]:
        return "BULGU DEVREDIYOR"
    if s["siklar_ayni"]:
        return "SLAYTI KOPYALA" if s["cevap_metni_ayni"] else "CELISKI - INCELE"
    return "KOPYALA + SIKLARI C'DEN AL"


def kararlari_oku():
    """Yakin eslesmelerin insan karari. Anahtar: '<Konu>/<C no>'."""
    if not KARAR_DOSYASI.exists():
        return {}
    ham = json.loads(KARAR_DOSYASI.read_text(encoding="utf-8"))
    return dict((k, v) for k, v in ham.items() if not k.startswith("_"))


def esle(c_banka, ab_banka, deck, konu, kararlar):
    """C bankasini A-B BANKASI ile eslestirir; slayt numarasini sonradan ekler.

    Esleme sunum metniyle DEGIL banka metniyle yapilir. Iki sebep: (1) sunumda cizime
    bagli sorularin govdesi bilerek yeniden yazilmis, banka metniyle karsilastirildiginda
    yapay olarak "yeni soru" gorunuyorlar; (2) sunumdaki sik metinleri zenginlestirilmis
    ("32" yerine "32 Ohm"), sik kumesi karsilastirmasi yaniltici olurdu. Iki banka ayni
    bozulmayi tasidigi icin karsilastirma adil.
    """
    ab_sorular = dict((s["no"], s) for s in ab_banka["sorular"])
    tersi = {}
    for no, s in ab_sorular.items():
        tersi.setdefault(anahtarla(s["govde"]), no)
    anahtar_listesi = list(tersi.keys())

    satirlar = []
    for c in c_banka["sorular"]:
        ca = anahtarla(c["govde"])
        ab_no, durum, benzerlik = None, "yeni", 0.0
        if ca in tersi:
            ab_no, durum, benzerlik = tersi[ca], "birebir", 1.0
        else:
            yakin = difflib.get_close_matches(ca, anahtar_listesi, n=1, cutoff=YAKINLIK_ESIGI)
            if yakin:
                ab_no = tersi[yakin[0]]
                durum = "yakin"
                benzerlik = round(difflib.SequenceMatcher(None, ca, yakin[0]).ratio(), 3)

        karar = kararlar.get("%s/%d" % (konu, c["no"]), {})
        slayt = deck.get(ab_no) if ab_no else None
        satir = {
            "c_no": c["no"],
            "yakin_karar": karar.get("karar"),
            "yakin_gerekce": karar.get("gerekce"),
            "durum": durum,
            "c_cevap": c["cevap"],
            "elle_aktarilmali": c["elle_aktarilmali"],
            "ab_no": ab_no,
            "ab_slayt": slayt["slayt"] if slayt else None,
            "ab_blok": slayt["blok"] if slayt else None,
            "benzerlik": benzerlik,
            "siklar_ayni": None,
            "cevap_metni_ayni": None,
            "ab_cevap": ab_sorular[ab_no]["cevap"] if ab_no else None,
            "ab_slaytta_isaretli": slayt["dogru_harf"] if slayt else None,
            "ab_bulgu_devrediyor": False,
        }

        if ab_no:
            ab = ab_sorular[ab_no]
            satir["siklar_ayni"] = sik_kumesi(c["siklar"]) == sik_kumesi(ab["siklar"])
            c_dogru = c["siklar"].get((c["cevap"] or "").lower(), "")
            ab_dogru = ab["siklar"].get((ab["cevap"] or "").lower(), "")
            satir["cevap_metni_ayni"] = bool(c_dogru) and anahtarla(c_dogru) == anahtarla(ab_dogru)
            # A-B setinde slaytta isaretli sik resmi anahtardan farkliysa, o soru
            # KEGM duzeltme onerisindeki bir bulgudur. Ayni soru C bankasinda da ayni
            # resmi cevapla duruyorsa bulgu C setine de gecer -- duzeltme onerisine
            # "C seti" olarak islenecek aday budur.
            if (slayt and slayt["dogru_harf"] and ab["cevap"]
                    and slayt["dogru_harf"] != ab["cevap"]
                    and satir["cevap_metni_ayni"]):
                satir["ab_bulgu_devrediyor"] = True

        satir["eylem"] = eylem_belirle(satir)
        satirlar.append(satir)
    return satirlar


def markdown(tum, genel):
    sat = ["# C Sinifi Esleme Tablosu", "",
           "Uretim: `python tools/esleme.py`. Elle duzenlenmez.", "",
           "Her C sorusunun A-B setindeki karsiligi ve buna gore yapilacak is. Esleme, soru",
           "govdesinin normalize edilmis hali uzerinden yapilir; **dogru sik karsilastirmasi",
           "harf uzerinden degil sik metni uzerinden** yapilir.", "",
           "## Ozet", "", "| Eylem | Soru |", "|---|---|"]
    for k in sorted(genel):
        sat.append("| %s | %d |" % (k, genel[k]))
    sat += ["",
            "**Eylemler**",
            "",
            "- `SLAYTI KOPYALA` - govde birebir ayni, sik kumesi ayni, resmi cevap ayni.",
            "  A-B slayti oldugu gibi tasinir.",
            "- `KOPYALA + SIKLARI C'DEN AL` - govde birebir ayni ama sik kumesi farkli.",
            "  Aciklama metni tasinir; **sik listesi ve isaretli harf C bankasindan alinir**.",
            "- `YAKIN ESLESME - DOGRULA` - benzerlik esigi asildi ama birebir degil. Otomatik",
            "  kullanilmaz: tek harflik ayrimi olan sorular yuksek benzerlikte yanlis eslesiyor",
            "  (or. C Isletme 37 \"VE oneki\" ile A-B Isletme 60 \"VK oneki\", benzerlik 0.98,",
            "  cevaplari haklı olarak farkli). Her satir insan tarafindan onaylanmali.",
            "- `YENI ACIKLAMA` - A-B'de karsiligi yok, sifirdan yazilacak.",
            "- `CELISKI - INCELE` - sik kumesi AYNI oldugu halde iki bankanin resmi cevabi",
            "  farkli. Gercek celiski; KEGM duzeltme onerisine bulgu adayi.",
            "- `BULGU DEVREDIYOR` - A-B setinde bu soru zaten bir bulgu (slaytta isaretli sik",
            "  resmi anahtardan farkli) ve ayni hata C bankasinda da duruyor.",
            "",
            "`elle` sutunu faz 1'den gelir: metin katmani yetmiyor, soru PDF'e bakilarak aktarilmali.",
            "",
            "Yakin eslesmelerin insan karari ve gerekcesi `tools/karar_yakin_eslesme.json`",
            "dosyasindadir; karari olmayan yakin eslesme tabloda `YAKIN ESLESME - DOGRULA`",
            "olarak kalir.",
            ""]
    for konu in tum:
        satirlar = tum[konu]
        sat += ["## %s" % konu, "",
                "| C # | Durum | A-B # | Slayt | Benzerlik | Siklar ayni | C cevap | A-B cevap | elle | Eylem |",
                "|---|---|---|---|---|---|---|---|---|---|"]
        for s in satirlar:
            sat.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
                s["c_no"], s["durum"],
                s["ab_no"] if s["ab_no"] else "-",
                s["ab_slayt"] if s["ab_slayt"] else "-",
                ("%.2f" % s["benzerlik"]) if s["benzerlik"] else "-",
                {True: "evet", False: "HAYIR", None: "-"}[s["siklar_ayni"]],
                s["c_cevap"] or "-", s["ab_cevap"] or "-",
                "evet" if s["elle_aktarilmali"] else "",
                s["eylem"]))
        sat.append("")
    return "\n".join(sat) + "\n"


def main():
    yalniz_rapor = "--rapor" in sys.argv
    tum = {}
    genel = {}
    uyari = []
    kararlar = kararlari_oku()

    for konu, c_dosya, ab_dosya, deck_dosya in KONULAR:
        c_banka = json.loads((CIKTI / (c_dosya + ".json")).read_text(encoding="utf-8"))
        ab_banka = json.loads((CIKTI / (ab_dosya + ".json")).read_text(encoding="utf-8"))
        deck = deck_oku(KOK / deck_dosya)

        for u in deck_bankayla_tutuyor_mu(deck, ab_banka):
            uyari.append("%s: %s" % (konu, u))

        satirlar = esle(c_banka, ab_banka, deck, konu, kararlar)
        tum[konu] = satirlar
        sayim = {}
        for s in satirlar:
            sayim[s["eylem"]] = sayim.get(s["eylem"], 0) + 1
            genel[s["eylem"]] = genel.get(s["eylem"], 0) + 1
        print("%-14s C=%3d  slayttaki soru=%3d  %s"
              % (konu, len(satirlar), len(deck),
                 "  ".join("%s:%d" % (k, sayim[k]) for k in sorted(sayim))))

    if uyari:
        print("\nUYARI -- slayt/banka numaralandirmasi (%d):" % len(uyari))
        for u in uyari[:25]:
            print("  - %s" % u)

    print("\nTOPLAM: %s" % "  ".join("%s:%d" % (k, genel[k]) for k in sorted(genel)))

    if not yalniz_rapor:
        (CIKTI / "esleme_C.json").write_text(
            json.dumps(tum, ensure_ascii=False, indent=2), encoding="utf-8")
        (KOK / "docs" / "esleme_C.md").write_text(markdown(tum, genel), encoding="utf-8")
        print("\nyazildi: tools/cikti/esleme_C.json  ve  docs/esleme_C.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
