from collections import namedtuple

import pyqtgraph as pg

from pyqtgraph_basics.basic_plotter import basic_array_plotting, LivePlotter, LineChart
from pyqtgraph_basics.candle_stick_item import CandlestickChartWidget

Size = namedtuple("size", ["w", "h"])
Rgb = namedtuple("rgb", ["r", "g", "b", "a"])

class PlotAppService:
    
    def __init__(self, size: Size, bg_color: Rgb, antialias: bool = True, app_title: str = '', widget_title: str = '', win_title: str = ''):
        
        # Enable antialiasing for prettier plots
        pg.setConfigOption('antialias', antialias)
        pg.setConfigOption('background', (bg_color.r, bg_color.g, bg_color.b))

        # Store the application instance to prevent garbage collection
        self.app = pg.mkQApp(app_title)

        self.win = pg.GraphicsLayoutWidget(show=True, title=widget_title)
        self.win.resize(size.w, size.h)
        self.win.setWindowTitle(win_title)
        
    def add_basic_array_chart(self, title: str = ''):
        
        self.basic_array_plotting_item = basic_array_plotting(title)
        self.win.addItem(self.basic_array_plotting_item)
    
    def add_line_chart(self, title: str = ''):

        x_data = [1, 2, 3, 4, 5]
        y_data = [2, 6, 11, -3, 4]
        
        self.line_chart = LineChart(title=title)
        self.line_chart.update_data(x_data=x_data, y_data=y_data)
        self.win.addItem(self.line_chart.plot_item)
        
    def add_live_plotter(self, title: str = ''):
        
        self.live_plotter = LivePlotter()
        self.win.addItem(self.live_plotter.plot_item)
    
    def add_candle_stick_chart(self, title: str = ''):
        
        data = [  ## fields are (time, open, close, min, max).
                (1., 10, 13, 5, 15),
                (2., 13, 17, 9, 20),
                (3., 17, 14, 11, 23),
                (4., 14, 15, 5, 19), 
                (5., 15, 9, 8, 22),
                (6., 9, 15, 8, 16),
            ]
        # Instantiate the self-contained module
        self.btc_chart_item = CandlestickChartWidget(title="BTC/USD", data=data)
        # Extract the exposed pointer and mount it to the physical layout
        self.win.addItem(self.btc_chart_item.plot_item)

    
    def add_row(self):
        
        self.win.nextRow()
    
    def exec(self):
        """
        Starts the Qt event loop.
        This is a blocking call and must be the absolute last instruction executed.
        """
        pg.exec()

def main():
    
    plot_service = PlotAppService(size = Size(w=1000, h=600), bg_color = Rgb(r=30, g=30, b=40, a=0), 
                                  app_title = "app_title", widget_title = 'widget_title', win_title = "win_title")
    plot_service.add_basic_array_chart('Basic Plotting')
    plot_service.add_live_plotter('Live Plotter')
    plot_service.add_row()
    plot_service.add_line_chart('Line Chart')
    plot_service.add_candle_stick_chart('Candlestick Chart')
    plot_service.exec()

    



if __name__ == '__main__':
    
    main()
