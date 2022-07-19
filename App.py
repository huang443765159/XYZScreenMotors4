import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from example.Utils import QTools
from example.Gui.Gui import Gui
from example.Gui.UI.UI import Ui_MainWindow
from example.Devices.Devices import Devices


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        QApplication.setStyle('Fusion')
        QApplication.setPalette(QTools.get_default_palette())
        QTools.font_size_auto_adapt(qt_ui=self._ui)
        self._devices = Devices()
        self._gui = Gui(ui=self._ui)

    def closeEvent(self, _):
        self._devices.exit()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec_())
