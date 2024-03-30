# =============================================================================
# CODE IMPORTS
# =============================================================================
import os, sys
from functools import partial
from numbers import Number
import matplotlib
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
# import qdarktheme

__doc__     = "Calculator and Math Helper"
__version__ = "0.1.3"

PTH_APP = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(PTH_APP, 'data'))

# ---- Local addins
from _global_ import *
matplotlib.use('Qt5Agg')
from generic_widgets import QCalcWidget, QTriangle_Solver
import mainWindow
    
class MainWindow(QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self, app:QApplication) -> None:
        super().__init__(None)
        self.setupUi(self)
        self.setWindowTitle(__doc__)
        self.show()
        self._app  = app

        # add custom widgets
        self._calc = QCalcWidget(self.tab)
        self.triangle_solver = QTriangle_Solver(self.tab_2)
        return
    
    def closeEvent(self, event):
        self._app.quit()
        return sys.exit()


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        # qdarktheme.setup_theme("auto")
        navForm = MainWindow(app)
        sys.exit(app.exec_())   

    except KeyboardInterrupt:
        app.quit()
