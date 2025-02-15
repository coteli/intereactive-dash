# Türkiye Konut Satışları Dashboard

Bu dashboard uygulaması, Türkiye İstatistik Kurumu (TÜİK) tarafından aylık olarak açıklanan Konut Satış İstatistikleri'ni interaktif bir şekilde görselleştirmektedir.

## 🎯 Proje Hakkında

Bu uygulama, Türkiye'deki konut satış verilerini üç farklı perspektiften analiz etmenizi sağlar:

1. **İnteraktif Türkiye Haritası**
   - Yıllara göre illerdeki toplam konut satış sayılarını renk skalası ile gösterir
   - Beyaz-Yeşil-Kırmızı renk skalası ile satış yoğunluğunu görselleştirir
   - İllere tıklayarak detaylı analiz yapılabilir

2. **İlçe Bazlı Analiz**
   - Seçilen il ve yıla göre ilçelerdeki konut satış sayılarını gösterir
   - İlçeler satış sayılarına göre sıralanır
   - Yatay bar grafik ile kolay karşılaştırma imkanı sunar

3. **Aylık Satış Trendi**
   - Seçilen il ve yıl için aylık satış trendini gösterir
   - Mevsimsel değişimleri analiz etme imkanı sunar
   - Dikey bar grafik ile aylık karşılaştırma yapılabilir

## 🔧 Teknik Özellikler

- **Framework**: Python Dash
- **Veri Kaynağı**: TÜİK Konut Satış İstatistikleri
- **Harita**: GeoJSON ile Türkiye il sınırları
- **Grafikler**: Plotly Express
- **Stil**: Bootstrap tema

## 📊 Veri Seti

Uygulamada kullanılan veriler:
- TÜİK'in aylık olarak yayınladığı Konut Satış İstatistikleri'nden derlenmiştir
- İl ve ilçe bazında konut satış sayılarını içerir
- Aylık periyotta güncellenebilir yapıdadır

## 🚀 Kullanım

1. Yıl seçimi için üst kısımdaki slider'ı kullanın
2. Türkiye haritası üzerinde istediğiniz ile tıklayın
3. Alt bölümde seçilen ile ait detaylı analizleri görüntüleyin:
   - Sol tarafta ilçe bazlı satış sayıları
   - Sağ tarafta aylık satış trendi

## 💻 Kurulum

## 📝 Gereksinimler

- Python 3.7+
- Dash
- Plotly
- Pandas
- Dash Bootstrap Components

## 🤝 Katkıda Bulunma

1. Bu repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: Detay'`)
4. Branch'inizi push edin (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakınız.

## 🙏 Teşekkür

- Veriler için Türkiye İstatistik Kurumu'na
- GeoJSON verisi için [cihadturhan/tr-geojson](https://github.com/cihadturhan/tr-geojson) repository'sine

## 📧 İletişim

Sorularınız için [GitHub Issues](https://github.com/coteli/intereactive-dash/issues) sayfasını kullanabilirsiniz.