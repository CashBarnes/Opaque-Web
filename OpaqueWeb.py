import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngine import *

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()
        print(self.browser.page().profile().httpUserAgent())

        self.browser.page().profile().setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0")
        
        self.browser.setUrl(QUrl('http://google.com'))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        #opacity slider values to divide by 100. These are high so that the slider is more smooth than ticky.
        sliderMin = 300
        sliderMax = 1000        
        
        self.set_new_opacity(sliderMax)

        #create navbar
        navbar = QToolBar()
        navbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.addToolBar(navbar)
        
        #create opacity slider
        mySlider = QSlider(Qt.Horizontal, self)
        mySlider.setRange(sliderMin, sliderMax)
        mySlider.setValue(sliderMax)
        mySlider.setMaximum(sliderMax)
        mySlider.setMinimum(sliderMin)
        navbar.addWidget(mySlider)
        mySlider.valueChanged[int].connect(self.set_new_opacity)
        
        #create On Top button to toggle having the browser stay on top of the desktop
        self.top_button = QAction('On Top', self)
        self.top_button.setCheckable(True)
        self.top_button.setChecked(False)
        self.top_button.toggled.connect(self.toggle_stay_on_top)
        navbar.addAction(self.top_button)          
        
        #create back button
        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        #create forward button
        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        #create refresh button
        refresh_btn = QAction('Refresh', self)
        refresh_btn.triggered.connect(self.browser.reload)
        navbar.addAction(refresh_btn)

        #create home button
        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        #create url bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)
        self.browser.urlChanged.connect(self.update_url)
    
    def toggle_stay_on_top(self):
        if self.top_button.isChecked():
           self.setWindowFlags(Qt.WindowStaysOnTopHint)
           print('camera1')
        else:
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
            print('camera2')
        self.show()
                
    def navigate_home(self):
        self.browser.setUrl(QUrl('http://google.com'))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())
        
    def set_new_opacity(self, o):
        self.setWindowOpacity(o * .001)
            
    def onTop(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.showMaximized()
    
app = QApplication(sys.argv)
QApplication.setApplicationName('Opaque Web')
QApplication.setWindowIcon(QtGui.QIcon('icon.ico'))
window = MainWindow()
app.exec_()
