# amator-telsiz-egitimi

Türkçe konuş. Kullanıcı Türkçe çalışıyor.

KEGM Amatör Telsizcilik Belgesi (A/B ve C sınıfı) sınavına hazırlık seti — **soru + açıklama +
kaynak** formatında iki sınıf için üçer PowerPoint sunumu ve sınıf başına bir toplu PDF.
Depo: `TA3HRJ/amator-telsiz-egitimi`

Bu bir kod projesi değil, belge projesidir. Çıktılar `.pptx` ve `.pdf`; `index.html` indirme
sayfasıdır.

## İçerik

| Belge | A/B Sınıfı (v1.1) | C Sınıfı (v1.0) |
|---|---|---|
| Ulusal ve Uluslararası Düzenlemeler | 67 soru | 49 soru |
| İşletme | 151 soru | 82 soru |
| Teknik | 172 soru | 140 soru |
| Tüm Konular (PDF) | 429 sayfa | 299 sayfa |

Konular: Düzenlemeler — KEGM Yönetmeliği (RG 27482), CEPT/ITU; İşletme — Q-kodları, fonetik
alfabe, mors, çağrı işareti kuralları; Teknik — devre analizi, anten, propagasyon, temel
formüller.

`Soru_Bankalari/` altında altı orijinal KEGM soru bankası durur: açıklamasız, sonlarında resmî
cevap anahtarı var.

C sunumları elle düzenlenmez; `icerik/*.json` ve `tools/*.py` üzerinden yeniden üretilir
(zincir `docs/HANDOFF.md` → "Üretim zinciri"). A/B sunumlarının repoda üretici betiği yoktur;
onlar dosya üzerinde düzenlenir.

## Setin varlık sebebi — bunu bozma

Hazır soru bankalarının çoğu yalnızca doğru şıkkı işaretler. Bu set her sorunun **neden** doğru
olduğunu ilgili yönetmelik maddesine veya fiziksel/teknik formüle atıfla açıklar. Bir slaytı
düzenlerken gerekçeyi veya kaynak atfını kısaltma — setin tek ayırt edici özelliği bu.

## Sürüm disiplini

Dosya adları sürüm numarası taşır (`_v1.1`). İçerik değiştiğinde sürüm numarası da değişir.
Bu kural, erken indirenlerin güncellemeleri fark edememesi üzerine getirildi — dosya adını sabit
tutup içeriği değiştirme. A/B ve C setleri ayrı sürüm hattı yürütür.

Kapaktaki yazar/editör satırı gibi künye düzeltmeleri sürüm atlatmaz (Eylül 2026'daki çağrı
işareti değişikliği böyle işlendi); soru, şık, açıklama veya kaynak değişikliği atlatır.

v1.1'de sorulara dayanak olan yönetmelik hükümlerinin yürürlükte olup olmadığı Resmî Gazete
metinleri üzerinden denetlendi; çıkan beş bulgu (Düzenlemeler 17, 42, 60 ve İşletme 22, 89)
ilgili slaytlara uyarı kutusu olarak işlendi.

## Notlar

- Mevzuat metinlerinin ham arşivi (Resmî Gazete PDF'leri, kanunlar, yönetmelikler)
  `_shared/amator-radyo-mevzuat-arsivi/` altındadır — bu depo ile `amator-telsiz-mevzuat` deposu
  aynı kaynağı kullanır.
- KEGM soru bankalarındaki hataları belgeleyen düzeltme önerisi ayrı bir çıktıdır
  (`KEGM_Soru_Bankasi_Duzeltme_Onerisi_v1.2.pptx`, 16 bulgu, altı bankayı kapsar; her bulgu
  A-B / C setini belirtir) ve kuruma sunulmak üzere hazırlanmıştır. Tek dosya kalır; yeni
  bulgular bu dosyaya işlenir.

## Oturum sonu

Anlamlı bir iş yaptıysan — bir karar verildi, bir şey kırılıp düzeldi, bir varsayım ölçüldü —
bitirmeden önce `docs/HANDOFF.md`'yi güncelle: nerede kalındı, ne açık kaldı, hangi tuzağa
düşüldü ve neden. Dosya yoksa oluştur.

Sohbet geçmişi kalıcı değildir. Repoda yazılı olmayan her şey oturumla birlikte gider.

## Git kimliği

Bu depoda kimlik **yerel** olarak ayarlı (`.git/config`); makinede global `.gitconfig` yok
ve olmamalı:

```
user.name  = TA3HX
user.email = 136229226+TA3HRJ@users.noreply.github.com
```

Yerel olması kasıtlı — klasör başka bir makineye taşındığında commit atmak için hiçbir
kurulum gerekmiyor. Özel e-posta adresi kullanma; noreply adresi hem gerçek adresi gizler
hem de commit'lerin GitHub hesabına düzgün atfedilmesini sağlar.
