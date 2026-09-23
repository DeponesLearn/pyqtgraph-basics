from pyqtgraph_basics.plotting_service import PlotService

def main():
    
    plot_service = PlotService(size = Size(w=1000, h=600), bg_color = Rgb(r=30, g=30, b=40, a=0), 
                                  app_title = "app_title", widget_title = 'widget_title', win_title = "win_title")
    plot_service.add_basic_array_chart('Basic Plotting')
    plot_service.add_live_plotter('Live Plotter')
    plot_service.add_row()
    plot_service.add_line_chart('Line Chart')
    plot_service.add_candle_stick_chart('Candlestick Chart')
    plot_service.exec()

if __name__ == '__main__':
    
    main()
