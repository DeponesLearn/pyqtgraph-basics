import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

def main():

    app = pg.mkQApp("GeeksforGeeks PyQtGraph")
    
    window = pg.plot()
    window.setGeometry(100, 100, 600, 500)
    window.setWindowTitle("GeeksforGeeks PyQtGraph")
    
    y1 = [5, 5, 7, 10, 3, 8, 9, 1, 6, 2]
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    bargraph = pg.BarGraphItem(x=x, height=y1, width=0.6, brush='g')
    window.addItem(bargraph)
    
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
