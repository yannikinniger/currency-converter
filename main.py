from converter import Converter
from PyQt5.QtWidgets import *
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter = Converter()
    converter.show()
    sys.exit(app.exec_())
