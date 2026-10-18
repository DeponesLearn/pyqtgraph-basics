import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

def main():
    # 1. Qt Uygulamasını başlatıyoruz
    app = pg.mkQApp("İşlem Sayısı Grafik Uygulaması")
    
    # 2. Grafik penceresini oluşturuyoruz
    window = pg.plot()
    window.setGeometry(100, 100, 800, 600)
    window.setWindowTitle("Aylık İşlem Sayıları Kontrol Paneli")
    
    # Eksen başlıklarını (Labels) tanımlıyoruz
    window.setLabel('left', 'İşlem Sayısı', units='Adet')
    window.setLabel('bottom', 'Aylar')
    window.showGrid(x=False, y=True) # Sadece yatay kılavuz çizgilerini açalım
    
    # 3. Örnek Verilerimizi hazırlıyoruz (6 aylık veri)
    aylar_isimleri = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran"]
    x_merkezleri = np.arange(len(aylar_isimleri))  # [0, 1, 2, 3, 4, 5] merkez noktalar
    
    # Her ay için yan yana çizilecek iki farklı veri grubu (Y ekseni değerleri)
    basarili_islemler = [120, 150, 80, 200, 170, 220]
    hatali_islemler = [15, 30, 10, 45, 20, 35]
    
    # 4. Yan Yana Gruplama Mantığı (X eksenini kaydırma)
    bar_genisligi = 0.35  # Barların kalınlığı
    
    # İlk bar serisini (Yeşil) sola kaydırıyoruz
    x_seri1 = x_merkezleri - (bar_genisligi / 2)
    # İkinci bar serisini (Kırmızı) sağa kaydırıyoruz
    x_seri2 = x_merkezleri + (bar_genisligi / 2)
    
    # 5. Bar nesnelerini oluşturup pencereye ekliyoruz
    # Başarılı İşlemler Barı
    bar1 = pg.BarGraphItem(
        x=x_seri1, 
        height=basarili_islemler, 
        width=bar_genisligi, 
        brush=pg.mkBrush('g'),      # Yeşil dolgu
        pen=pg.mkPen('w', width=1), # Beyaz dış çerçeve çizgisi
        name="Başarılı"
    )
    
    # Hatalı İşlemler Barı
    bar2 = pg.BarGraphItem(
        x=x_seri2, 
        height=hatali_islemler, 
        width=bar_genisligi, 
        brush=pg.mkBrush('r'),      # Kırmızı dolgu
        pen=pg.mkPen('w', width=1), # Beyaz dış çerçeve çizgisi
        name="Hatalı"
    )
    
    window.addItem(bar1)
    window.addItem(bar2)
    
    # 6. X Ekseni yazılarını (Ocak, Şubat vb.) sayılar yerine yerleştirme
    # setTicks formatı: [ [(sayisal_pozisyon, "görünecek_metin"), (...)] ] şeklindedir.
    ay_etiketleri = [(i, ay) for i, ay in enumerate(aylar_isimleri)]
    
    ax = window.getAxis('bottom')
    ax.setTicks([ay_etiketleri])
    
    # 7. Grafiğe Gösterge (Legend) ekleme
    legend = window.addLegend()
    legend.addItem(bar1, "Başarılı İşlemler")
    legend.addItem(bar2, "Hatalı İşlemler")
    
    # Pencereyi görünür yapıp Qt döngüsünü başlatıyoruz
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
