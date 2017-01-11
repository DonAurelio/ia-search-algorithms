import sys
from PyQt4.QtGui import *
from Window import Window

if __name__ == '__main__':
	app = QApplication( sys.argv )
	application = Window()
	application.show()
	app.exec_()

