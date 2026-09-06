# HANDOFF

Son güncelleme: 6 Eylül 2026

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
2. **A-B dosyaları yeniden adlandırılacak** — adlarına `A-B` işareti eklenecek
   (ör. `Amator_Telsizcilik_A-B_Teknik_Sinav_Hazirlik_v1.1.pptx`). **Sürüm numarası sabit kalır**:
   içerik değişmiyor, yalnızca ad belirsizliği gideriliyor. Eski indirme bağlantıları kırılacak;
   bu bilinçli kabul edildi.
3. **Ortak sorular için yeniden açıklama üretilmeyecek.** Mevcut açıklama slaytı kopyalanır,
   yalnızca şık listesi ve işaretli harf düzeltilir.
4. **KEGM düzeltme önerisi tek dosya kalacak.** C setinde bulunacak hatalar ayrı bir çıktıya
   değil, mevcut `KEGM_Soru_Bankasi_Duzeltme_Onerisi` dosyasına işlenecek; her bulgu **hangi
   sete ait olduğu (A-B / C) açıkça belirtilerek**. Dosya henüz KEGM'ye iletilmedi, dolayısıyla
   C bulguları eklendikten sonra tek seferde sunulabilir.

## Fazlar

1. **Çıkarım hattı** — C bankalarından soru/şık/cevap anahtarı çıkarımı ve doğrulaması.
   *Uyarı:* `pdftotext` çıktısında Türkçe karakterler bozuluyor (ı/ş/ğ/İ kayboluyor). A-B setinde
   bu sorun çözülmüş olmalı; **aynı yöntem kullanılmalı, yeniden icat edilmemeli.**
2. **Eşleme tablosu** — 271 C sorusunun her biri için: hangi A-B slaytından geliyor / yeni mi,
   şık kümesi aynı mı farklı mı. Faz 3-4'ün tek doğruluk kaynağı bu tablodur.
3. **105 yeni açıklama** — mevcut formatı bozmadan: gerekçe + yönetmelik maddesi veya formül atfı.
   Setin varlık sebebi bu (bkz. CLAUDE.md); kısaltma yok.
4. **Ortak soruların taşınması** — yukarıdaki tuzak kuralına göre.
5. **Mevzuat denetimi** — v1.1'de A-B'ye uygulanan yürürlük denetimi C'ye taşınır. Mevcut beş
   bulgunun C karşılıkları aranır; C'ye özgü 105 sorudan çıkacak yeni bulgular düzeltme önerisine
   eklenir (9 bulgudan yukarı çıkar).
6. **Paketleme** — C toplu PDF, `index.html`, README, sürüm.

## Yol üstünde düzeltilecekler

- `index.html` sürüm rozeti **1.0** diyor ama v1.1 dosyalarına link veriyor. Alt başlık da
  şimdiden "A/B ve C Sınıfı" iddiasında — C çıktısı yokken bu yanlış.
- `Soru_Bankalari/` ad tutarsızlığı: `C_sinifi_isletme...` büyük C, diğer ikisi küçük
  `c_sinifi...`. GitHub Pages büyük/küçük harfe duyarlı; düzeltilirse `index.html` bağlantıları
  da güncellenmeli.

## Açık kalanlar

- C sunumlarının sürüm numarası: yeni set v1.0 olarak mı başlar, yoksa setin bütünü v1.2'ye mi
  taşınır? Karar verilmedi.
- Faz 1'deki karakter kodlaması sorununun A-B setinde nasıl çözüldüğü repoda yazılı değil.
