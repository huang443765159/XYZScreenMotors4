from example.Gui._GuiCmd import GuiCmd
from example.Gui._GuiAttr import GuiAttr
from example.Gui.UI.UI import Ui_MainWindow


class Gui:

    def __init__(self, ui: Ui_MainWindow):
        self._cmd = GuiCmd(ui=ui)
        self._attr = GuiAttr(ui=ui)
