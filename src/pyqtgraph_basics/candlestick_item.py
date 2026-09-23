import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

class CandlestickItem(pg.GraphicsObject):
    """
    Isolated custom graphics item for rendering candlestick charts.
    Responsible ONLY for drawing data to a QPicture buffer.
    Oblivious to the parent layout, axes, or main window.
    """
    
    def __init__(self, data=None):
        super().__init__()
        
        # Buffer for hardware-accelerated drawing
        self.picture = QtGui.QPicture()
        self.data = data
        
        # Defensive check to prevent segmentation faults / index errors on init
        if self.data is not None and len(self.data) > 1:
            self.generate_picture()
            
    def set_data(self, data):
        """
        Memory-safe interface to update the data stream dynamically.
        Forces the Qt Event Loop to flag the region as dirty and trigger a repaint.
        """
        self.data = data
        if self.data is not None and len(self.data) > 1:
            self.generate_picture()
        else:
            self.picture = QtGui.QPicture() # Flush buffer if data is corrupted/empty
            
        # Trigger the Qt paint engine (equivalent to invalidating a framebuffer)
        self.update()
        self.informViewBoundsChanged() # Signal parent to auto-range X/Y axis
    
    def generate_picture(self):
        """Pre-computes vector instructions into QPicture to minimize CPU overhead during paint()."""
        
        self.picture = QtGui.QPicture()
        painter = QtGui.QPainter(self.picture)
        painter.setPen(pg.mkPen('w'))
        
        # Defensive delta calculation
        try:
            bar_width = (self.data[1][0] - self.data[0][0]) / 3.0
        except IndexError:
            bar_width = 1.0

        for (t, open_val, close_val, min_val, max_val) in self.data:
            # Draw the wicks (high/low)
            painter.drawLine(QtCore.QPointF(t, min_val), QtCore.QPointF(t, max_val))
            
            # Determine body color based on tick direction
            if open_val > close_val:
                painter.setBrush(pg.mkBrush('r')) # Bearish
            else:
                painter.setBrush(pg.mkBrush('g')) # Bullish
                
            # Draw the body
            body_rect = QtCore.QRectF(t - bar_width, open_val, bar_width * 2, close_val - open_val)
            painter.drawRect(body_rect)
            
        painter.end()
    
    def paint(self, painter, *args):
        """Hardware callback. Dumps the pre-compiled QPicture buffer to the screen."""
        painter.drawPicture(0, 0, self.picture)
    
    def boundingRect(self):
        """Defines the memory footprint area for the clipping engine."""
        return QtCore.QRectF(self.picture.boundingRect())
    
    
    # 2. The High-Level Controller Struct (Branch Node / Wrapper)
class CandlestickChartWidget:
    """
    Encapsulates both the PlotItem (Viewport) and the CandlestickItem (Texture).
    Exposes a ready-to-use .plot_item pointer for the main window layout.
    """
    def __init__(self, title: str = "Market Data", data=None):
        
        # Allocate the viewport (Axes, Grid, Labels)
        self.plot_item = pg.PlotItem(title=title)
        self.plot_item.showGrid(x=True, y=True, alpha=0.3)
        self.plot_item.setLabel('left', 'Price')
        self.plot_item.setLabel('bottom', 'Time')
        
        # Allocate the hardware-accelerated drawing object
        self.candle_visual = CandlestickItem(data=data)
        
        # Link the leaf to the branch internally
        self.plot_item.addItem(self.candle_visual)
        
    def update_data(self, new_data):
        """Pass-through method to update the internal visual safely."""
        self.candle_visual.data = new_data
        self.candle_visual.generate_picture()
        self.candle_visual.update() # Flag for repaint