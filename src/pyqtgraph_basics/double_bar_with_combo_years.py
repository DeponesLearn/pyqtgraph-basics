import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel
from PySide6.QtCore import Qt
import pyqtgraph as pg

class GraphApp(QMainWindow):
    
    def __init__(self):
        
        super().__init__()
        
        self.setWindowTitle("Yıllara Göre Aylık İşlem Sayıları")
        self.setGeometry(100, 100, 900, 650)
        
        # 1. Sahte Veri Seti Oluşturma (Son 3 Yıl İçin)
        # Her yıl için 12 ay var ve her ay için 2 farklı veri (Başarılı, Hatalı)
        self.data = {
            "2024": {
                "basarili": [10, 12,  8, 15, 11,  9, 14, 13, 10,  8, 12, 11],
                "hatali":   [10, 12,  8, 15, 11,  9, 14, 13, 10,  8, 12, 11]
            },
            "2025": {
                "basarili": [],
                "hatali":   [8,  11,  9,  7, 12, 10,  8, 11,  6,   9,  11,  13]
            },
            "2026": {
                "basarili": [],
                "hatali":   [5,   7,  6,   8,   5,   9,   7,   6,   8,   5,   4,   6]
            }
        }
        
        self.months = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", 
                      "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
        
        # 2. Arayüz Elemanlarının Oluşturulması
        ana_widget = QWidget()
        self.setCentralWidget(ana_widget)
        main_layout = QVBoxLayout(ana_widget)
        
        # Üst Panel (Yıl Seçimi İçin)
        top_layout = QHBoxLayout()
        year_label = QLabel("Görüntülenecek Yılı Seçin:")
        
        self.year_combo = QComboBox()
        self.year_combo.addItems(["2024", "2025", "2026"])
        # Combobox değiştiğinde grafiği güncelleyecek fonksiyonu bağlıyoruz
        self.year_combo.currentIndexChanged.connect(self.update_graph)
        
        top_layout.addWidget(year_label)
        top_layout.addWidget(self.year_combo)
        top_layout.addStretch() # Sağ tarafı boş bırakıp elemanları sola yaslar
        
        # 3. PyQtGraph Grafik Alanının Oluşturulması
        self.graph_area = pg.PlotWidget()
        self.graph_area.setLabel('left', 'İşlem Sayısı', units='Adet')
        self.graph_area.setLabel('bottom', 'Aylar')
        self.graph_area.showGrid(x=False, y=True)
        
        # X Ekseni Etiketlerini Sabitleme (0-11 arası konumlara ay isimlerini basıyoruz)
        month_labels = [(i, ay) for i, ay in enumerate(self.months)]
        ax = self.graph_area.getAxis('bottom')
        ax.setTicks([month_labels])
        
        # Gösterge (Legend) Tanımlama
        self.legend = self.graph_area.addLegend()
        
        # Düzeni Birleştirme
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.graph_area)
        
        # 4. İlk Grafiği Çizdirme (Varsayılan olarak ilk yıl)
        self.bar1 = None
        self.bar2 = None
        self.update_graph()

    def update_graph(self):
        # Seçili yılı alıyoruz
        selected_year = self.year_combo.currentText()
        
        # O yıla ait verileri çekiyoruz
        basarili_veri = self.data[selected_year]["basarili"]
        hatali_veri = self.data[selected_year]["hatali"]
        
        # Matematiksel konumlandırma (12 ay için)
        x_centers = np.arange(12)
        bar_length = 0.35
        x_series1 = x_centers - (bar_length / 2)
        x_series2 = x_centers + (bar_length / 2)
        
        # Eski barlar varsa hafızadan ve ekrandan temizliyoruz (Üst üste binmemesi için)
        if self.bar1 is not None:
            self.graph_area.removeItem(self.bar1)
        if self.bar2 is not None:
            self.graph_area.removeItem(self.bar2)
            
        # Yeni BarGraphItem'ları oluşturuyoruz
        self.bar1 = pg.BarGraphItem(x=x_series1, height=basarili_veri, width=bar_length, brush=pg.mkBrush('#2ecc71'), pen=pg.mkPen('w', width=1))
        self.bar2 = pg.BarGraphItem(x=x_series2, height=hatali_veri, width=bar_length, brush=pg.mkBrush('#e74c3c'), pen=pg.mkPen('w', width=1))
        
        # Grafiğe ekleme
        self.graph_area.addItem(self.bar1)
        self.graph_area.addItem(self.bar2)
        
        # Legend (Gösterge) eşleşmesini yeniliyoruz
        self.legend.clear()
        self.legend.addItem(self.bar1, "Başarılı İşlemler")
        self.legend.addItem(self.bar2, "Hatalı İşlemler")
        
        # Grafik eksen sınırlarını otomatik optimize et
        self.graph_area.enableAutoRange()

def main():
    
    app = QApplication(sys.argv)
    window = GraphApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
