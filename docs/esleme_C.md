# C Sinifi Esleme Tablosu

Uretim: `python tools/esleme.py`. Elle duzenlenmez.

Her C sorusunun A-B setindeki karsiligi ve buna gore yapilacak is. Esleme, soru
govdesinin normalize edilmis hali uzerinden yapilir; **dogru sik karsilastirmasi
harf uzerinden degil sik metni uzerinden** yapilir.

## Ozet

| Eylem | Soru |
|---|---|
| KOPYALA + SIKLARI C'DEN AL | 12 |
| SLAYTI KOPYALA | 144 |
| YENI ACIKLAMA | 115 |

**Eylemler**

- `SLAYTI KOPYALA` - govde birebir ayni, sik kumesi ayni, resmi cevap ayni.
  A-B slayti oldugu gibi tasinir.
- `KOPYALA + SIKLARI C'DEN AL` - govde birebir ayni ama sik kumesi farkli.
  Aciklama metni tasinir; **sik listesi ve isaretli harf C bankasindan alinir**.
- `YAKIN ESLESME - DOGRULA` - benzerlik esigi asildi ama birebir degil. Otomatik
  kullanilmaz: tek harflik ayrimi olan sorular yuksek benzerlikte yanlis eslesiyor
  (or. C Isletme 37 "VE oneki" ile A-B Isletme 60 "VK oneki", benzerlik 0.98,
  cevaplari haklı olarak farkli). Her satir insan tarafindan onaylanmali.
- `YENI ACIKLAMA` - A-B'de karsiligi yok, sifirdan yazilacak.
- `CELISKI - INCELE` - sik kumesi AYNI oldugu halde iki bankanin resmi cevabi
  farkli. Gercek celiski; KEGM duzeltme onerisine bulgu adayi.
- `BULGU DEVREDIYOR` - A-B setinde bu soru zaten bir bulgu (slaytta isaretli sik
  resmi anahtardan farkli) ve ayni hata C bankasinda da duruyor.

`elle` sutunu faz 1'den gelir: metin katmani yetmiyor, soru PDF'e bakilarak aktarilmali.

Yakin eslesmelerin insan karari ve gerekcesi `tools/karar_yakin_eslesme.json`
dosyasindadir; karari olmayan yakin eslesme tabloda `YAKIN ESLESME - DOGRULA`
olarak kalir.

## Duzenlemeler

| C # | Durum | A-B # | Slayt | Benzerlik | Siklar ayni | C cevap | A-B cevap | elle | Eylem |
|---|---|---|---|---|---|---|---|---|---|
| 1 | birebir | 29 | 35 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 2 | birebir | 6 | 8 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 3 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 4 | birebir | 8 | 11 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 5 | birebir | 9 | 12 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 6 | birebir | 13 | 16 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 7 | birebir | 16 | 20 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 8 | birebir | 19 | 23 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 9 | birebir | 54 | 63 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 10 | birebir | 21 | 26 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 11 | birebir | 22 | 27 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 12 | yakin | 23 | 28 | 0.99 | evet | B | B |  | SLAYTI KOPYALA |
| 13 | birebir | 24 | 29 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 14 | birebir | 25 | 30 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 15 | birebir | 26 | 31 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 16 | birebir | 28 | 33 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 17 | birebir | 5 | 7 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 18 | birebir | 31 | 37 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 19 | birebir | 32 | 38 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 20 | birebir | 34 | 40 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 21 | birebir | 35 | 41 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 22 | birebir | 36 | 42 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 23 | birebir | 37 | 44 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 24 | birebir | 38 | 45 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 25 | birebir | 39 | 46 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 26 | yakin | 40 | 47 | 0.97 | HAYIR | D | A |  | YENI ACIKLAMA |
| 27 | birebir | 42 | 49 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 28 | birebir | 43 | 51 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 29 | birebir | 44 | 52 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 30 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 31 | birebir | 46 | 54 | 1.00 | HAYIR | C | C |  | KOPYALA + SIKLARI C'DEN AL |
| 32 | birebir | 47 | 55 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 33 | birebir | 48 | 56 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 34 | birebir | 50 | 59 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 35 | birebir | 45 | 53 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 36 | yakin | 41 | 48 | 0.97 | HAYIR | B | C |  | YENI ACIKLAMA |
| 37 | birebir | 60 | 70 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 38 | birebir | 57 | 67 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 39 | birebir | 58 | 68 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 40 | birebir | 59 | 69 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 41 | birebir | 61 | 71 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 42 | birebir | 62 | 72 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 43 | birebir | 63 | 73 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 44 | birebir | 64 | 74 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 45 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 46 | birebir | 65 | 75 | 1.00 | HAYIR | C | C |  | KOPYALA + SIKLARI C'DEN AL |
| 47 | birebir | 67 | 77 | 1.00 | HAYIR | D | D |  | KOPYALA + SIKLARI C'DEN AL |
| 48 | birebir | 52 | 61 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 49 | birebir | 53 | 62 | 1.00 | HAYIR | A | A |  | KOPYALA + SIKLARI C'DEN AL |

## Isletme

| C # | Durum | A-B # | Slayt | Benzerlik | Siklar ayni | C cevap | A-B cevap | elle | Eylem |
|---|---|---|---|---|---|---|---|---|---|
| 1 | birebir | 3 | 5 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 2 | birebir | 4 | 6 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 3 | birebir | 5 | 7 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 4 | yakin | 8 | 10 | 0.92 | evet | C | C |  | SLAYTI KOPYALA |
| 5 | birebir | 9 | 11 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 6 | birebir | 12 | 14 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 7 | birebir | 15 | 18 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 8 | birebir | 16 | 19 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 9 | birebir | 17 | 20 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 10 | birebir | 23 | 26 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 11 | birebir | 26 | 30 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 12 | birebir | 30 | 34 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 13 | birebir | 31 | 35 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 14 | birebir | 34 | 38 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 15 | birebir | 44 | 49 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 16 | birebir | 46 | 51 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 17 | birebir | 47 | 52 | 1.00 | HAYIR | B | B |  | KOPYALA + SIKLARI C'DEN AL |
| 18 | birebir | 49 | 55 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 19 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 20 | birebir | 55 | 61 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 21 | birebir | 56 | 62 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 22 | yakin | 57 | 63 | 0.95 | evet | C | C |  | SLAYTI KOPYALA |
| 23 | birebir | 58 | 64 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 24 | birebir | 59 | 65 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 25 | yakin | 92 | 101 | 0.87 | HAYIR | D | A |  | YENI ACIKLAMA |
| 26 | birebir | 60 | 67 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 27 | birebir | 61 | 68 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 28 | birebir | 62 | 69 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 29 | birebir | 65 | 72 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 30 | birebir | 66 | 73 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 31 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 32 | birebir | 68 | 75 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 33 | birebir | 69 | 76 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 34 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 35 | birebir | 74 | 82 | 1.00 | HAYIR | C | C |  | KOPYALA + SIKLARI C'DEN AL |
| 36 | yakin | 76 | 84 | 0.92 | evet | D | D |  | SLAYTI KOPYALA |
| 37 | yakin | 60 | 67 | 0.98 | evet | B | D |  | YENI ACIKLAMA |
| 38 | yakin | 80 | 88 | 0.92 | HAYIR | C | B |  | YENI ACIKLAMA |
| 39 | yakin | 117 | 128 | 0.88 | HAYIR | B | A |  | YENI ACIKLAMA |
| 40 | birebir | 81 | 89 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 41 | birebir | 82 | 90 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 42 | birebir | 83 | 91 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 43 | birebir | 85 | 94 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 44 | birebir | 86 | 95 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 45 | birebir | 90 | 99 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 46 | birebir | 91 | 100 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 47 | birebir | 92 | 101 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 48 | birebir | 93 | 102 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 49 | birebir | 94 | 103 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 50 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 51 | birebir | 96 | 105 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 52 | yeni | - | - | - | - | D | - |  | YENI ACIKLAMA |
| 53 | birebir | 99 | 109 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 54 | yakin | 100 | 110 | 0.98 | evet | B | B |  | SLAYTI KOPYALA |
| 55 | birebir | 101 | 111 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 56 | birebir | 102 | 112 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 57 | birebir | 103 | 113 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 58 | birebir | 104 | 114 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 59 | yakin | 105 | 115 | 0.96 | HAYIR | D | D |  | YENI ACIKLAMA |
| 60 | birebir | 106 | 116 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 61 | birebir | 107 | 117 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 62 | birebir | 108 | 118 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 63 | birebir | 110 | 121 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 64 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 65 | yakin | 115 | 126 | 0.89 | HAYIR | A | A |  | YENI ACIKLAMA |
| 66 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 67 | birebir | 140 | 153 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 68 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 69 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 70 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 71 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 72 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 73 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 74 | birebir | 142 | 155 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 75 | birebir | 51 | 57 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 76 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 77 | birebir | 52 | 58 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 78 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 79 | birebir | 145 | 158 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 80 | birebir | 148 | 161 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 81 | birebir | 150 | 163 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 82 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |

## Teknik

| C # | Durum | A-B # | Slayt | Benzerlik | Siklar ayni | C cevap | A-B cevap | elle | Eylem |
|---|---|---|---|---|---|---|---|---|---|
| 1 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 2 | birebir | 14 | 17 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 3 | yakin | 15 | 18 | 0.93 | evet | A | A | evet | SLAYTI KOPYALA |
| 4 | birebir | 16 | 19 | 1.00 | HAYIR | D | D |  | KOPYALA + SIKLARI C'DEN AL |
| 5 | birebir | 20 | 23 | 1.00 | evet | D | D | evet | SLAYTI KOPYALA |
| 6 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 7 | birebir | 21 | 24 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 8 | birebir | 22 | 25 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 9 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 10 | yeni | - | - | - | - | B | - | evet | YENI ACIKLAMA |
| 11 | birebir | 23 | 26 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 12 | birebir | 24 | 27 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 13 | yeni | - | - | - | - | C | - | evet | YENI ACIKLAMA |
| 14 | birebir | 25 | 29 | 1.00 | HAYIR | D | D | evet | KOPYALA + SIKLARI C'DEN AL |
| 15 | birebir | 26 | 30 | 1.00 | evet | D | D | evet | SLAYTI KOPYALA |
| 16 | birebir | 29 | 33 | 1.00 | evet | D | D | evet | SLAYTI KOPYALA |
| 17 | birebir | 31 | 35 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 18 | birebir | 34 | 39 | 1.00 | evet | B | B | evet | SLAYTI KOPYALA |
| 19 | birebir | 35 | 40 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 20 | birebir | 36 | 41 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 21 | birebir | 41 | 46 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 22 | birebir | 42 | 47 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 23 | birebir | 43 | 48 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 24 | birebir | 47 | 53 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 25 | birebir | 48 | 54 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 26 | birebir | 52 | 58 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 27 | birebir | 53 | 59 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 28 | birebir | 54 | 60 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 29 | birebir | 55 | 61 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 30 | birebir | 56 | 62 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 31 | birebir | 58 | 64 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 32 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 33 | birebir | 61 | 68 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 34 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 35 | yeni | - | - | - | - | A | - | evet | YENI ACIKLAMA |
| 36 | yeni | - | - | - | - | D | - |  | YENI ACIKLAMA |
| 37 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 38 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 39 | birebir | 72 | 79 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 40 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 41 | birebir | 3 | 5 | 1.00 | HAYIR | B | B |  | KOPYALA + SIKLARI C'DEN AL |
| 42 | yeni | - | - | - | - | A | - | evet | YENI ACIKLAMA |
| 43 | birebir | 129 | 140 | 1.00 | HAYIR | C | C | evet | KOPYALA + SIKLARI C'DEN AL |
| 44 | birebir | 79 | 87 | 1.00 | evet | D | D | evet | SLAYTI KOPYALA |
| 45 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 46 | yeni | - | - | - | - | D | - |  | YENI ACIKLAMA |
| 47 | yeni | - | - | - | - | D | - |  | YENI ACIKLAMA |
| 48 | yeni | - | - | - | - | C | - | evet | YENI ACIKLAMA |
| 49 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 50 | birebir | 94 | 103 | 1.00 | evet | C | C |  | SLAYTI KOPYALA |
| 51 | birebir | 95 | 104 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 52 | birebir | 96 | 105 | 1.00 | evet | A | A | evet | SLAYTI KOPYALA |
| 53 | birebir | 97 | 106 | 1.00 | evet | A | A | evet | SLAYTI KOPYALA |
| 54 | yakin | 99 | 108 | 0.99 | HAYIR | C | C | evet | KOPYALA + SIKLARI C'DEN AL |
| 55 | yeni | - | - | - | - | D | - | evet | YENI ACIKLAMA |
| 56 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 57 | birebir | 101 | 111 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 58 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 59 | birebir | 102 | 112 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 60 | birebir | 105 | 115 | 1.00 | evet | C | C | evet | SLAYTI KOPYALA |
| 61 | yeni | - | - | - | - | D | - |  | YENI ACIKLAMA |
| 62 | yeni | - | - | - | - | A | - | evet | YENI ACIKLAMA |
| 63 | birebir | 114 | 124 | 1.00 | evet | B | B | evet | SLAYTI KOPYALA |
| 64 | yeni | - | - | - | - | A | - | evet | YENI ACIKLAMA |
| 65 | yeni | - | - | - | - | A | - | evet | YENI ACIKLAMA |
| 66 | yeni | - | - | - | - | C | - | evet | YENI ACIKLAMA |
| 67 | yeni | - | - | - | - | D | - |  | YENI ACIKLAMA |
| 68 | yeni | - | - | - | - | B | - | evet | YENI ACIKLAMA |
| 69 | birebir | 137 | 149 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 70 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 71 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 72 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 73 | yeni | - | - | - | - | B | - | evet | YENI ACIKLAMA |
| 74 | yeni | - | - | - | - | D | - | evet | YENI ACIKLAMA |
| 75 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 76 | yeni | - | - | - | - | C | - | evet | YENI ACIKLAMA |
| 77 | yeni | - | - | - | - | A | - | evet | YENI ACIKLAMA |
| 78 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 79 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 80 | yeni | - | - | - | - | D | - |  | YENI ACIKLAMA |
| 81 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 82 | birebir | 138 | 150 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 83 | birebir | 139 | 151 | 1.00 | evet | A | A | evet | SLAYTI KOPYALA |
| 84 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 85 | yeni | - | - | - | - | D | - |  | YENI ACIKLAMA |
| 86 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 87 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 88 | yeni | - | - | - | - | B | - | evet | YENI ACIKLAMA |
| 89 | yeni | - | - | - | - | D | - |  | YENI ACIKLAMA |
| 90 | birebir | 140 | 152 | 1.00 | evet | B | B |  | SLAYTI KOPYALA |
| 91 | yeni | - | - | - | - | C | - | evet | YENI ACIKLAMA |
| 92 | birebir | 141 | 153 | 1.00 | evet | A | A | evet | SLAYTI KOPYALA |
| 93 | yeni | - | - | - | - | D | - | evet | YENI ACIKLAMA |
| 94 | birebir | 142 | 154 | 1.00 | evet | C | C | evet | SLAYTI KOPYALA |
| 95 | birebir | 143 | 155 | 1.00 | evet | D | D | evet | SLAYTI KOPYALA |
| 96 | birebir | 144 | 156 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 97 | birebir | 145 | 157 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 98 | yeni | - | - | - | - | D | - | evet | YENI ACIKLAMA |
| 99 | birebir | 134 | 146 | 1.00 | evet | D | D |  | SLAYTI KOPYALA |
| 100 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 101 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 102 | birebir | 95 | 104 | 1.00 | HAYIR | D | B |  | KOPYALA + SIKLARI C'DEN AL |
| 103 | birebir | 146 | 158 | 1.00 | evet | A | A |  | SLAYTI KOPYALA |
| 104 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 105 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 106 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 107 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 108 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 109 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 110 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 111 | yeni | - | - | - | - | D | - |  | YENI ACIKLAMA |
| 112 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 113 | yeni | - | - | - | - | D | - |  | YENI ACIKLAMA |
| 114 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 115 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 116 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 117 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 118 | yeni | - | - | - | - | D | - |  | YENI ACIKLAMA |
| 119 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 120 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 121 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 122 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 123 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 124 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 125 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 126 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 127 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 128 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 129 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 130 | yeni | - | - | - | - | D | - |  | YENI ACIKLAMA |
| 131 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 132 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 133 | yeni | - | - | - | - | B | - |  | YENI ACIKLAMA |
| 134 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 135 | yakin | 154 | 167 | 0.95 | HAYIR | A | A |  | YENI ACIKLAMA |
| 136 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |
| 137 | yeni | - | - | - | - | D | - |  | YENI ACIKLAMA |
| 138 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 139 | yeni | - | - | - | - | C | - |  | YENI ACIKLAMA |
| 140 | yeni | - | - | - | - | A | - |  | YENI ACIKLAMA |

