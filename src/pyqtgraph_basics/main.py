import pyqtgraph as pg

from pyqtgraph_basics.basic_plotter import basic_array_plotting, LivePlotter, LineChart

def main():
    
    # Enable antialiasing for prettier plots
    pg.setConfigOption('antialias', True)
    pg.setConfigOption('background', (30, 30, 40))

    app = pg.mkQApp("Plotting Example")

    win = pg.GraphicsLayoutWidget(show=True, title="Hello !")
    win.resize(1000, 600)
    win.setWindowTitle('Basic Plottings')
        
    basic_array_plotting(win)
    win.nextRow()
    # live_plotter = LivePlotter(win)
    line_chart = LineChart(win)

    pg.exec()


if __name__ == '__main__':
    
    main()
