import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

def main():
    # 1. Qt Uygulamasını başlat
    app = pg.mkQApp("GeeksforGeeks PyQtGraph")
    
    # 2. Grafik penceresini oluştur ve ayarla
    window = pg.plot()
    window.setGeometry(100, 100, 600, 500)
    window.setWindowTitle("GeeksforGeeks PyQtGraph")
    
    # 3. Verileri tanımla ve grafiği ekle
    y1 = [5, 5, 7, 10, 3, 8, 9, 1, 6, 2]
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    bargraph = pg.BarGraphItem(x=x, height=y1, width=0.6, brush='g')
    window.addItem(bargraph)
    
    # 4. Pencereyi göster
    window.show()
    
    # 5. Olay döngüsünü başlat (Pencerenin açık kalmasını sağlar)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
