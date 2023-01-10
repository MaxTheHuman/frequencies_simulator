import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QWidget, QLabel
from PyQt5 import uic

from design import Ui_Simulator

plt.ion()

class Canvas(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(3, 2))
        # fig = plt.figure()
        # self.ax = fig.add_subplot(1)
        super().__init__(fig)
        self.setParent(parent)

    def x(self, t, alpha, beta, w, phi):
        return alpha * np.exp(-beta * t) * np.cos(w * t + phi)

    def show_plot(self, alpha, beta, w, phi):
        t = np.arange(0.0, 20.0, 0.01)
        s = [self.x(t_i, alpha, beta, w, phi) for t_i in t]
        
        self.ax.clear()
        self.ax.plot(t, s)

        self.ax.set(xlabel='time (s)', ylabel='x')
        self.ax.grid()
        
class UI(QMainWindow, Ui_Simulator):
    def __init__(self):
        super().__init__()

        # uic.loadUi('simulator.ui', self)
        self.setupUi(self)

        self.alpha_slider = self.findChild(QSlider, 'alphaHorizontalSlider')
        self.alpha = self.alpha_slider.value()
        self.alpha_slider.valueChanged.connect(self.changedAlphaSlider)

        self.phi_slider = self.findChild(QSlider, 'phiHorizontalSlider')
        self.phi = self.phi_slider.value() / 10 * np.pi
        self.phi_slider.valueChanged.connect(self.changedPhiSlider)
        
        self.beta_slider = self.findChild(QSlider, 'betaHorizontalSlider')
        self.beta = self.beta_slider.value() / 20
        self.beta_slider.valueChanged.connect(self.changedBetaSlider)

        self.w_slider = self.findChild(QSlider, 'wHorizontalSlider')
        self.w = self.w_slider.value()
        self.w_slider.valueChanged.connect(self.changedWSlider)

        

        self.diff_text = self.findChild(QLabel, 'diffLabel')

        self.graph_show = self.findChild(QWidget, 'graphWidget')
        self.chart = Canvas(self.graph_show)
        self.chart.show_plot(self.alpha, self.beta, self.w, self.phi)
    
    def changedAlphaSlider(self):
        self.alpha = self.alpha_slider.value()
        self.diff_text.setText('Изменили A на ' + str(self.alpha))
        self.chart.show_plot(self.alpha, self.beta, self.w, self.phi)

    def changedBetaSlider(self):
        self.beta = self.beta_slider.value() / 20
        self.diff_text.setText('Изменили B на ' + str(self.beta))
        self.chart.show_plot(self.alpha, self.beta, self.w, self.phi)

    def changedPhiSlider(self):
        self.phi = self.phi_slider.value() / 10 * np.pi
        self.diff_text.setText('Изменили ф на ' + str(self.phi))
        self.chart.show_plot(self.alpha, self.beta, self.w, self.phi)

    def changedWSlider(self):
        self.w = self.w_slider.value()
        self.diff_text.setText('Изменили w на ' + str(self.w))
        self.chart.show_plot(self.alpha, self.beta, self.w, self.phi)
    

app = QApplication([])
window = UI()
window.show()
app.exec()
