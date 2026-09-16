import time
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore

class TimeAxisItem(pg.AxisItem):

    def tickStrings(self, values, scale, spacing):

        # Converts Unix timestamp values into 'HH:MM:SS' strings
        return [time.strftime('%H:%M:%S', time.localtime(local_time)) for local_time in values]

class LivePlotter:
    
    def __init__(self, win: pg.GraphicsLayoutWidget, max_points: int = 150, sma_period: int = 20, timer_ms: int = 1000):

        self.max_points = max_points
        self.sma_period = sma_period
        self.step_sec = timer_ms / 1000.0

        # Main Plot Setup with Custom Time Axis
        self.p = win.addPlot(title="Live Plotter", axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.p.showGrid(x=True, y=True, alpha=0.3)
        self.p.setLabel('left', 'Price', color='#ffffff', size='12pt')
        self.p.setLabel('bottom', 'Time', color='#ffffff', size='12pt')
        
        # UI Performance: Enable automatic tracking instead of manual X/Y range.
        self.p.enableAutoRange(axis=pg.ViewBox.XYAxes)

        current_time = time.time()
        self.x_data = np.linspace(current_time - (self.max_points * self.step_sec), current_time, self.max_points)
        self.y_data = np.zeros(self.max_points)

        # 3. Curve Visual Overlays
        self.price_curve = self.p.plot(pen=pg.mkPen(color=(255, 100, 100), width=1), name="Raw Price")
        self.sma_curve = self.p.plot(pen=pg.mkPen(color=(240, 230, 140), width=1, style=QtCore.Qt.PenStyle.DashLine), 
                                     name=f"SMA ({self.sma_period})")

        # 4. Asynchronous Animation Engine Setup
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_stream_tick)
        self.timer.start(timer_ms)

    def update_stream_tick(self):
        
        next_time = self.x_data[-1] + self.step_sec
        self.x_data[:-1] = self.x_data[1:]
        self.x_data[-1] = next_time
        
        # Slicing instead of np.append (Zero-ram load)
        new_tick = self.y_data[-1] + np.random.normal(scale=0.15)
        self.y_data[:-1] = self.y_data[1:]
        self.y_data[-1] = new_tick
        
        # Vectorel SMA (np.convolve) instead of for loop
        weights = np.ones(self.sma_period) / self.sma_period
        sma_calculated = np.convolve(self.y_data, weights, mode='valid')
        sma_padded = np.pad(sma_calculated, (self.sma_period - 1, 0), 'edge')

        # Commit array streams directly to canvas items
        self.price_curve.setData(x=self.x_data, y=self.y_data)
        self.sma_curve.setData(x=self.x_data, y=sma_padded)

def basic_array_plotting(win: pg.GraphicsLayoutWidget):

    p = win.addPlot(title="Basic array")
    p.setLabel('left', 'Price', color='#ffffff', size='12pt')
    p.setLabel('bottom', 'Time', color='#ffffff', size='12pt')

    p.setYRange(-5, 5, padding=0)
    p.setXRange(0, 100, padding=0)

    p.showGrid(x=True, y=True, alpha=0.9)
    p.plot(np.random.normal(size=100), pen=pg.mkPen(color=(255, 100, 100), width=1))    
    
def live_basic_array_plotting(win: pg.GraphicsLayoutWidget):
    
    # Pass the custom TimeAxisItem for the bottom (X) axis
    p = win.addPlot(title="Live Stream", axisItems={'bottom': TimeAxisItem(orientation='bottom')})

    # 1. Enable gridlines with alpha transparency
    p.showGrid(x=True, y=True, alpha=0.3)

    p.setLabel('left', 'Price', color='#ffffff', size='12pt')
    p.setLabel('bottom', 'Time', color='#ffffff', size='12pt')

    # Initialize data arrays for tracking live feeds
    max_points = 100
    # Populate initial historical X coordinates with consecutive timestamps up to 'now'
    current_time = time.time()
    x_data = np.linspace(current_time - max_points, current_time, max_points)
    y_data = np.random.normal(size=max_points)

    # Create an empty curve line item we can update on every tick
    curve = p.plot(pen=pg.mkPen(color=(255, 100, 100), width=1))
