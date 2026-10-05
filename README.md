# Bebek Molada — web sitesi

Bebek Molada mobil uygulamasının statik sitesi. GitHub Pages ile
<https://nodabasi.github.io/bebek-molada-app/> adresinde yayınlanır.

Düz HTML ve tek stil dosyası; derleme adımı ya da bağımlılık yok. Dosyayı düzenle,
commit et, push et; Pages bir iki dakikada yeniden yayınlar.

## Sayfalar

| Adres | Dosya | Mağazada kullanımı |
|---|---|---|
| `/bebek-molada-app/` | `index.html` | Pazarlama URL'si (Türkçe) |
| `/bebek-molada-app/support/` | `support/index.html` | Destek URL'si (Türkçe) |
| `/bebek-molada-app/privacy/` | `privacy/index.html` | Gizlilik Politikası URL'si (Türkçe) |
| `/bebek-molada-app/delete-account/` | `delete-account/index.html` | Google Play "hesap silme" URL'si (Türkçe) |
| `/bebek-molada-app/en/` | `en/index.html` | Pazarlama URL'si (İngilizce) |
| `/bebek-molada-app/en/support/` | `en/support/index.html` | Destek URL'si (İngilizce) |
| `/bebek-molada-app/en/privacy/` | `en/privacy/index.html` | Gizlilik Politikası URL'si (İngilizce) |
| `/bebek-molada-app/en/delete-account/` | `en/delete-account/index.html` | Hesap silme URL'si (İngilizce) |

**Klasör adlarını değiştirme.** Bu adresler App Store Connect ve Google Play Console'a
girildikten sonra adı değişen her klasör canlı bir mağaza bağlantısını bozar.

## Düzenleme

- Renkler ve yerleşim `assets/style.css` içinde; tüm sayfalar onu kullanır.
- Bağlantılar görelidir, site dosya sisteminden açıldığında da çalışır.
- Gizlilik politikası özünden değişirse `privacy/index.html` ve `en/privacy/index.html`
  başındaki yürürlük tarihini de güncelle.
- Uygulamaya yeni bir veri ya da SDK eklendiğinde (ör. telefonla giriş açılırsa telefon
  numarası) gizlilik politikasını ve hesap silme sayfasını o sürümden önce güncelle.

## Yerel önizleme

```sh
python3 -m http.server 8000
# sonra http://localhost:8000/ adresini aç
```
