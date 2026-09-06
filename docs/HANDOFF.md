# HANDOFF

Son güncelleme: 6 Eylül 2026 (ikinci tur)

## Nerede kalındı

C sınıfı sorularının sete dahil edilmesi **planlandı, henüz uygulanmadı**. Repoda C ile ilgili
hiçbir çıktı üretilmedi; `Soru_Bankalari/` altındaki üç C bankası zaten duruyordu.

Bu oturumda yapılan tek dosya değişikliği README'ye indirme sayfası bağlantısının eklenmesi
(`c2fdcfd`) ve fazla gelen doğrudan dosya bağlantılarının geri alınmasıdır (`f9e1730`).

## Ölçüm sonuçları — planın dayanağı

C bankalarının soru gövdeleri A-B bankalarıyla programatik olarak karşılaştırıldı
(`pdftotext -layout` + gövde normalizasyonu + `difflib` yakınlık eşiği 0.85):

| Konu | C soru | A-B ile birebir | Yakın | **Gerçekten yeni** |
|---|---|---|---|---|
| Düzenlemeler | 49 | 43 | 3 | **3** |
| İşletme | 82 | 56 | 10 | **16** |
| Teknik | 140 | 50 | 4 | **86** |
| **Toplam** | **271** | 149 | 17 | **105** |

C'nin **%61'i zaten açıklanmış durumda**. Yazılacak yeni açıklama 105 soru; ağırlığı Teknik'te
(86). Üç C bankasının da cevap anahtarı tam (49/49, 82/82, 140/140).

C İşletme bankası 1-82 arası kesintisiz numaralanmış; boşluk veya tekrar yok.

## Tuzak — kör kopyalamayı engelleyen bulgu

**Aynı soru gövdesi, farklı şık kümesi olabiliyor.** İki vaka ölçüldü:

- **Teknik** — "Bir telsiz alıcısının seçiciliği:" → A-B soru 95'te doğru şık **b**
  (*"almama kabiliyetidir"*), C soru 102'de doğru şık **d** (*"bastırabilme kabiliyetidir"*).
  Şık metinleri de farklı yazılmış.
- **Düzenlemeler** — lisans bölümü sorusu: A-B soru 40'ta şıklar Fizik/Biyoloji/Kimya/İnşaat
  (cevap **a**), C soru 26'da Fizik/Elektrik/Haberleşme/Kimya (cevap **d**).

Kural: ortak sorularda **açıklama metni A-B'den aynen taşınır**, ama **şık listesi ve doğru harf
mutlaka C bankasından alınır**. Eşleme harf üzerinden değil, **şık metni** üzerinden doğrulanmalı.
Bu ayrım yapılmazsa set yanlış cevap gösterir.

## Verilen kararlar

1. **Ayrı C sunumları** üretilecek; A-B ile birleşik tek sunum yapılmayacak. C adayının A-B'ye
   özgü sorulardan geçmesi gerekmesin, setin konu-bazlı yapısı korunsun diye.
2. **A-B dosyaları yeniden adlandırıldı** (uygulandı) — üç sunumun adına `A-B` işareti eklendi
   (`Amator_Telsizcilik_A-B_Teknik_Sinav_Hazirlik_v1.1.pptx` vb.). **Sürüm numarası sabit tutuldu**:
   içerik değişmedi, yalnızca ad belirsizliği giderildi. Eski indirme bağlantıları kırıldı; bu
   bilinçli kabul edildi. Toplu PDF adında `A-B` zaten vardı, dokunulmadı.
3. **Ortak sorular için yeniden açıklama üretilmeyecek.** Mevcut açıklama slaytı kopyalanır,
   yalnızca şık listesi ve işaretli harf düzeltilir.
4. **C seti v1.0 olarak başlar.** A-B seti kendi çizgisinde v1.1'de kalır; iki set ayrı sürüm
   hattı yürütür. Sitede "A/B Sınıfı … (v1.1)" ile "C Sınıfı … (v1.0)" yan yana duracak, bu
   beklenen durumdur. Dosya adları A-B kuralını izler:
   `Amator_Telsizcilik_C_Teknik_Sinav_Hazirlik_v1.0.pptx`,
   `KEGM_Amator_Telsizcilik_C_Sinav_Hazirlik_Tum_Konular_v1.0.pdf`.
   Düzeltme önerisi bu ikisinden bağımsızdır: tek dosya olduğu ve iki seti birden kapsadığı için
   C bulguları eklendiğinde kendi numarası v1.2'ye çıkar.
5. **KEGM düzeltme önerisi tek dosya kalacak.** C setinde bulunacak hatalar ayrı bir çıktıya
   değil, mevcut `KEGM_Soru_Bankasi_Duzeltme_Onerisi` dosyasına işlenecek; her bulgu **hangi
   sete ait olduğu (A-B / C) açıkça belirtilerek**. Dosya henüz KEGM'ye iletilmedi, dolayısıyla
   C bulguları eklendikten sonra tek seferde sunulabilir.

## Fazlar

1. **Çıkarım hattı** — **tamamlandı**, bkz. aşağıdaki "Faz 1 sonucu".
2. **Eşleme tablosu** — 271 C sorusunun her biri için: hangi A-B slaytından geliyor / yeni mi,
   şık kümesi aynı mı farklı mı. Faz 3-4'ün tek doğruluk kaynağı bu tablodur.
3. **105 yeni açıklama** — mevcut formatı bozmadan: gerekçe + yönetmelik maddesi veya formül atfı.
   Setin varlık sebebi bu (bkz. CLAUDE.md); kısaltma yok.
4. **Ortak soruların taşınması** — yukarıdaki tuzak kuralına göre.
5. **Mevzuat denetimi** — v1.1'de A-B'ye uygulanan yürürlük denetimi C'ye taşınır. Mevcut beş
   bulgunun C karşılıkları aranır; C'ye özgü 105 sorudan çıkacak yeni bulgular düzeltme önerisine
   eklenir (9 bulgudan yukarı çıkar).
6. **Paketleme** — C toplu PDF, `index.html`, README, sürüm.

## Faz 1 sonucu — çıkarım hattı kuruldu

`tools/cikarim.py`. Altı bankayı da işler, `tools/cikti/*.json` üretir:

```
python tools/cikarim.py            # isle ve yaz
python tools/cikarim.py --rapor    # yalnizca dogrulama raporu
```

Çıktı: her soru için `no`, `govde`, `siklar` (a-d), `cevap` (resmî anahtardan) ve
`elle_aktarilmali` işareti.

**Durum: ayrıştırma hatası 0.** Altı bankanın da soru sayısı ile cevap anahtarı sayısı birebir
tutuyor (151/172/67 ve 82/140/49), numaralandırmada boşluk yok, her cevap harfi mevcut bir şıkka
denk düşüyor.

### Ayrıştırmada çözülen üç tuzak

1. **Şıklar alfabetik sırada gelmiyor.** İki sütunlu dizgide `-layout` çıktısı önce `b)` ve `d)`,
   sonra `a)` ve `c)` verebiliyor (C teknik 26). a→b→c→d sırası dayatan ilk sürüm bu soruları
   tek şıkka düşürüyordu. Çözüm: sıra dayatma, etiketleri bulundukları yerde al.
2. **Sayfa başlığı filtresi geçerli bir şıkkı yiyordu.** `c) Kıyı Emniyeti Genel Müdürlüğü`
   gerçek bir şık; büyük/küçük harf duyarsız filtre bunu sayfa başlığı sanıyordu. Filtre
   büyük harf duyarlı yapıldı.
3. **Bitişik dizgi:** `c)3`, `d)Yozgat`. Etiket deseninde boşluk zorunluluğu kaldırıldı.

### Metin katmanının yetmediği sorular — elle aktarılmalı

Bunlar hattın hatası değil, kaynak PDF'in sınırı. `elle_aktarilmali` ile işaretlendi:

| Banka | İşaretli | Sebep |
|---|---|---|
| C Düzenlemeler | 0 / 49 | — |
| C İşletme | 0 / 82 | — |
| **C Teknik** | **36 / 140** | devre şeması, sembol, çizim üstü etiket |
| A-B Düzenlemeler | 0 / 67 | — |
| A-B İşletme | 12 / 151 | mors soruları: nokta işaretleri metin katmanında yok |
| A-B Teknik | 53 / 172 | devre şeması ve semboller |

Üç algılama ölçütü: (a) boş şık — seçenek çizim; (b) şıkların yalnızca işaretten oluşması veya
iki şıkkın aynı metne düşmesi — ayırt eden sembol (mors noktası, mikro) düşmüş; (c) gövdenin
`?`/`:`/`;` sonrasında çizim etiketi taşıması (`... kaç amperdir? 1A 2A 0.5A I`).

"ne şekilde yapılır", "yukarıdakilerden hangisi" gibi kalıplar çizim atfı sayılmaz — bunlar
istisna listesinde; olmasaydı C İşletme'nin fonetik alfabe soruları yanlışlıkla işaretlenirdi.

**Bilinen sınır:** ölçüt sezgiseldir. Elle taramada C teknik 53 gibi tek tük kaçak görüldü
(gövdesi `:` ile bitip ardından `Empedans Z f` etiketi gelen soru sonradan yakalandı, ama benzeri
başka kalıplar olabilir). Faz 3'te C Teknik soruları slayta dökülürken görsele bağlı olanlar
ayrıca gözle kontrol edilmeli.

**Eksik harflerin tamamlanması bu hattın işi değildir** ve yapılmadı: çıktıdaki metinlerde
ı/ş/ğ hâlâ yok. Tamamlama faz 3'te, slayt metni yazılırken yapılacak ve PDF'e karşı doğrulanacak.

## Yol üstünde düzeltilecekler

- `index.html` sürüm rozeti **1.0** diyordu ama v1.1 dosyalarına link veriyordu — 1.1 olarak
  düzeltildi.
- `index.html` alt başlığı hâlâ "A/B ve C Sınıfı" diyor. Şu an yalnızca C **soru bankaları**
  sunuluyor, C sunumu yok; C çıktıları yayımlanana kadar bu ifade fazla iddialı.
- `Soru_Bankalari/` ad tutarsızlığı giderildi: iki dosya küçük `c_sinifi...` idi, üçü de büyük
  `C_sinifi...` yapıldı (`A-B_sinifi...` kuralıyla uyumlu olsun diye). `index.html` bağlantıları
  da güncellendi. Git `core.ignorecase=true` olduğu için yeniden adlandırma ara ad üzerinden
  iki adımda yapıldı; tek adımda yapılırsa Git değişikliği görmez.

## PDF karakter sorunu — ölçüldü, çözüm devir dosyalarında yok

A-B setinde bu sorunun nasıl çözüldüğü **hiçbir yerde yazılı değil**: repoda devir/handoff `.md`
dosyası yoktu (bu dosya ilk), `_archive/oturum-transkriptleri/` ve
`_shared/claude-verisi/` altındaki oturum kayıtlarında da konuyla ilgili kayıt çıkmadı.

Sorunun sınırı ölçüldü:

- Soru bankası PDF'lerinin metin katmanında **ı, ş, ğ (ve büyükleri) hiç yok** — karakter bozuk
  değil, akıştan tamamen düşmüş. Üç çıkarım kipinde de aynı: `Haberleşme` → `Haberleme`.
  Hiçbir `pdftotext` bayrağı bunu geri getiremez.
- Buna karşılık **ç, ö, ü, Ç, Ö, Ü kurtarılabiliyor**: varsayılan UTF-8 kipinde `U+FFFD` oluyorlar,
  ama `pdftotext -enc Latin1` ile alınıp **cp1254 olarak çözülürse** doğru geliyorlar.

Pratik reçete:

```
pdftotext -enc Latin1 -layout <dosya>.pdf -   # ciktiyi cp1254 olarak decode et
```

Kalan {ı, ş, ğ, İ, Ş, Ğ} Türkçe imlâdan deterministik olarak tamamlanır (`Haberleme` →
`Haberleşme` bağlamda tek okumaya sahiptir), ama **tamamlama sonrası metin PDF'e karşı gözle
doğrulanmalıdır** — sette kaynak sadakati temel iddiadır.

## Açık kalanlar

Şu an yok — plan uygulanmayı bekliyor (bkz. Fazlar).
