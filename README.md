# Amatör Telsizcilik — Sınav Hazırlık Seti

**Sürüm 1.1 · 7 Ağustos 2026**

Türkiye'de Amatör Telsizcilik Belgesi (A/B/C sınıfı) sınavına hazırlananlar için, KEGM'nin resmî
soru bankalarına dayanan, **soru + açıklama + kaynak** formatında üç sunum seti.

Mevcut hazır soru bankalarının çoğu yalnızca "doğru şık" işaretler; gerekçe veya kaynak göstermez.
Bu set, her sorunun **neden** doğru olduğunu, ilgili yönetmelik maddesine veya fiziksel/teknik
formüle atıfla açıklar.

## İndirme

**İndirme sayfası:** <https://ta3hrj.github.io/amator-telsiz-egitimi/>

GitHub'ın mobil uygulamasında ve mobil tarayıcı görünümünde "Deployments" sekmesi
gösterilmediği için bu adrese oradan ulaşılamaz; telefondan indirmek için yukarıdaki adresi
doğrudan tarayıcıda (Chrome/Safari) açın.

## İçindekiler

| Belge | Kapsam |
|-------|--------|
| **A/B Sınıfı — Ulusal ve Uluslararası Düzenlemeler (v1.1)** | 67 soru — KEGM Sınav ve Belgelendirme Yönetmeliği (RG 27482), CEPT/ITU |
| **A/B Sınıfı — İşletme (v1.1)** | 151 soru — Q-kodları, fonetik alfabe, mors, çağrı işareti kuralları, işletme adabı |
| **A/B Sınıfı — Teknik (v1.1)** | 172 soru — devre analizi, anten, propagasyon, temel elektrik/elektronik formülleri |
| **A/B Sınıfı — Tüm Konular (PDF, v1.1)** | Yukarıdaki üç sunumun tamamı tek PDF'te (429 sayfa) — PowerPoint gerektirmeden görüntüleme/yazdırma için |
| **Soru_Bankalari/** | Orijinal KEGM soru bankaları (cevap anahtarsız) — pratik sınav olarak kullanılabilir |
| **Soru Bankası Düzeltme Önerisi (v1.1)** | KEGM Telsiz İşletme Müdürlüğü'ne sunulmak üzere hazırlanmış, 9 bulgu içeren düzeltme önerisi (bkz. aşağıda) |

> **Sürüm 1.1'de ne değişti:** Soruların dayandığı yönetmelik hükümlerinin bugün yürürlükte olup
> olmadığı Resmî Gazete metinleri üzerinden denetlendi. Bu denetimden çıkan **beş yeni bulgu**
> (Düzenlemeler 17, 42, 60 ve İşletme 22, 89) hem ilgili soru slaytlarına uyarı kutusu olarak işlendi
> hem de KEGM düzeltme önerisine eklendi. Düzeltme önerisi 4 bulgudan **9 bulguya** çıktı.

## Format

Her soru slaytı iki bölümden oluşur: solda **soru ve şıklar** (doğru şık işaretli), sağda
**açıklama ve kaynak**. Kısaltmalar ve teknik terimler *(parantez içinde italik)* sade Türkçe ile
açıklanmıştır — amatör olmayan biri de takip edebilir.

Sorular ~10 soruluk konu bloklarına ayrılmış; her blok kısa bir konu girişiyle başlar.

## Kaynak doğruluğu

Cevaplar, sorulara eşlik eden görsel işaretlerden değil, **her soru bankasının sonundaki resmî
cevap anahtarı tablosundan** programatik olarak çıkarılmış ve doğrulanmıştır. Hesaba dayalı sorular
(Ohm Kanunu, rezonans, güç/dB, anten boyu vb.) bağımsız olarak yeniden hesaplanmıştır.

Bu doğrulama sürecinde kaynak soru bankasının kendisinde birkaç **gerçek hata** bulunmuştur
(örn. bir rezonans frekansı hesabı, bir anten kısalma faktörü açıklaması). Bu sorularda slaytta
**doğru fizik/hesap gösterilmiş**, resmî anahtardan farkı sarı/turuncu bir uyarı kutusuyla açıkça
belirtilmiştir — gerçek sınavda resmî anahtarın ne diyebileceği not edilmiştir.

## KEGM'ye sunulacak düzeltme önerisi

`KEGM_Soru_Bankasi_Duzeltme_Onerisi_v1.1.pptx`, üç bankada tespit edilen **9 bulguyu** — orijinal soru,
resmî işaretli cevap, gerekçe/hesap ve önerilen düzeltmeyle — KEGM Telsiz İşletme Müdürlüğü'ne
sunulmak üzere derler. Bulgular iki ayrı denetimden gelir:

| Denetim | Bulgu |
|---|---|
| **Cevap anahtarı ve hesap** | İşletme 43 (CQ mod zorunluluğu); Teknik 46 (RMS → tepeden tepeye), 66 (LC rezonans), 120 (dipol kısalma sebebi) |
| **Mevzuat güncelliği** | Düzenlemeler 17 ve 42 (mülga Özel Telsiz Sistemleri Yönetmeliği'ne atıf); Düzenlemeler 60 ve İşletme 22 (ITU Region / CQ Zone / ITU Zone karışıklığı); İşletme 89 (dernek çağrı işareti ön eki — 20/2/2011 Yönetmelik değişikliği) |

Mevzuat güncelliği denetimi, soruların dayandığı hükümlerin bugün yürürlükte olup olmadığını Resmî
Gazete metinleri üzerinden kontrol eder. En belirgin bulgu, Özel Telsiz Sistemleri Yönetmeliği'nin
(RG 27292) FTM Yönetmeliği (RG 30608) Md.9/2 ile **27/11/2018'de yürürlükten kaldırılmış** olmasına
rağmen iki sorunun hâlâ bu yönetmeliği doğru cevap olarak göstermesidir.

Bu bulguların dokuzu da eğitim sunumlarında ilgili soru slaytına **turuncu uyarı kutusu** olarak
işlenmiştir: slaytta doğru bilgi/hesap gösterilir, resmî anahtarın ne dediği ve gerçek sınavda ne
beklenebileceği ayrıca belirtilir.

## Hazırlanış

Sorular, resmî KEGM soru bankalarından; açıklamalar ilgili yönetmelik maddelerinden (Düzenlemeler)
ve genel elektrik/elektronik/telsiz işletme referanslarından (İşletme, Teknik) türetilmiştir.

**Yazar:** Claude Sonnet 5 (Anthropic) · **Editör / Hata Kontrolü:** H. Erhan Özkan, TA3HRJ

## İlgili çalışma

Aynı camiaya yönelik mevzuat analizi ve kurumlara talep çalışması ayrı bir repoda yayımlanmaktadır:
[github.com/TA3HRJ/amator-telsiz-mevzuat](https://github.com/TA3HRJ/amator-telsiz-mevzuat)

İndirme sayfası: <https://ta3hrj.github.io/amator-telsiz-mevzuat/>

## Sorumluluk Reddi

Bu set, amatör telsiz camiasına katkı amacıyla gönüllü olarak hazırlanmıştır. **Sınav hazırlık
amaçlıdır; resmî bir KEGM yayını değildir.** Hata veya eksik içerebilir; gerçek sınavda resmî
cevap anahtarı esas alınır (yukarıda açıklanan istisnalar hariç). Ticari amaç taşımaz.

Katkı, düzeltme ve geri bildirimler memnuniyetle karşılanır:
[github.com/TA3HRJ/amator-telsiz-egitimi](https://github.com/TA3HRJ/amator-telsiz-egitimi)
