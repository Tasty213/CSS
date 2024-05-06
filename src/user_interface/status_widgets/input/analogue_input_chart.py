import pyqtgraph as pg


class AnalogueInputPortChart:
    def __init__(self, port_name: str, win: pg.GraphicsLayoutWidget):
        self.x = []
        self.y = []
        graph_item = pg.PlotItem()
        self.plot = graph_item.plot()
        win.addItem(graph_item)

    def update_plot(self, x, y):
        self.x.append(x)
        self.y.append(y)
        self.plot.setData(self.x, self.y)
