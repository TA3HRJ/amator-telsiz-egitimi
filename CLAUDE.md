# amator-telsiz-egitimi

Türkçe konuş. Kullanıcı Türkçe çalışıyor.

KEGM Amatör Telsizcilik Belgesi (A/B sınıfı) sınavına hazırlık seti — **soru + açıklama + kaynak**
formatında üç PowerPoint sunumu ve tek PDF. Depo: `TA3HRJ/amator-telsiz-egitimi`

Bu bir kod projesi değil, belge projesidir. Çıktılar `.pptx` ve `.pdf`; `index.html` indirme
sayfasıdır.

## İçerik

| Belge | Kapsam |
|---|---|
| Ulusal ve Uluslararası Düzenlemeler | 67 soru — KEGM Yönetmeliği (RG 27482), CEPT/ITU |
| İşletme | 151 soru — Q-kodları, fonetik alfabe, mors, çağrı işareti kuralları |
| Teknik | 172 soru — devre analizi, anten, propagasyon, temel formüller |
| Tüm Konular (PDF) | üçünün tamamı, 429 sayfa |
| `Soru_Bankalari/` | orijinal KEGM soru bankaları, cevap anahtarsız |

## Setin varlık sebebi — bunu bozma

Hazır soru bankalarının çoğu yalnızca doğru şıkkı işaretler. Bu set her sorunun **neden** doğru
olduğunu ilgili yönetmelik maddesine veya fiziksel/teknik formüle atıfla açıklar. Bir slaytı
düzenlerken gerekçeyi veya kaynak atfını kısaltma — setin tek ayırt edici özelliği bu.

## Sürüm disiplini

Dosya adları sürüm numarası taşır (`_v1.1`). İçerik değiştiğinde sürüm numarası da değişir.
Bu kural, erken indirenlerin güncellemeleri fark edememesi üzerine getirildi — dosya adını sabit
tutup içeriği değiştirme.

v1.1'de sorulara dayanak olan yönetmelik hükümlerinin yürürlükte olup olmadığı Resmî Gazete
metinleri üzerinden denetlendi; çıkan beş bulgu (Düzenlemeler 17, 42, 60 ve İşletme 22, 89)
ilgili slaytlara uyarı kutusu olarak işlendi.

## Notlar

- Mevzuat metinlerinin ham arşivi (Resmî Gazete PDF'leri, kanunlar, yönetmelikler)
  `_shared/amator-radyo-mevzuat-arsivi/` altındadır — bu depo ile `amator-telsiz-mevzuat` deposu
  aynı kaynağı kullanır.
- KEGM soru bankasındaki hataları belgeleyen düzeltme önerisi ayrı bir çıktıdır
  (`KEGM_Soru_Bankasi_Duzeltme_Onerisi_v1.1.pptx`, 9 bulgu) ve kuruma sunulmak üzere hazırlanmıştır.

## Oturum sonu

Anlamlı bir iş yaptıysan — bir karar verildi, bir şey kırılıp düzeldi, bir varsayım ölçüldü —
bitirmeden önce `docs/HANDOFF.md`'yi güncelle: nerede kalındı, ne açık kaldı, hangi tuzağa
düşüldü ve neden. Dosya yoksa oluştur.

Sohbet geçmişi kalıcı değildir. Repoda yazılı olmayan her şey oturumla birlikte gider.
