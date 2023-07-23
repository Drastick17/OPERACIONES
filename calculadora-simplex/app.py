

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from windows.login import LoginWindow
import sys  

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora SIMLEX")
        self.resize(600, 180)
        self.login_ui = LoginWindow()
        self.main()

    def main(self):
        self.login_ui.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())