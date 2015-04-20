from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from Observer import Observer
from LoadFile import LoadFile

M_Window_UI_class,M_Window_UI_Base_class = uic.loadUiType('gui/MainWindow.ui')

class Window(QMainWindow,M_Window_UI_class,Observer):

	def __init__(self, parent=None):
		
		QMainWindow.__init__(self,parent)
		self.setupUi(self)

		#Centrar QMainWindow
		display = QDesktopWidget().screenGeometry()
		interfaz = self.geometry()
		pos_horizontal = ( display.width() - interfaz.width() ) / 2
		pos_vertical = ( display.height() - interfaz.height() ) / 2
		self.move( pos_horizontal, pos_vertical )

		self.connect(self.pushButtonMoveRobot,SIGNAL("clicked()"),self.move_robot)
		self.connect(self.pushButtonLookGraph,SIGNAL("clicked()"),self.look_graph)
		self.connect(self.pushButtonFastSearch,SIGNAL("clicked()"),self.fast_search)
		self.connect(self.pushButtonNextStep,SIGNAL("clicked()"),self.step_search)

		loadFile = LoadFile("env.txt")
		dimension , environment = loadFile.read()
		queue_dimension = 0
		self.draw_environment(environment)

	def draw_environment(self,environment):
		matrix = environment
		self.tableWidgetEnvironment.setRowCount(len(matrix))
		self.tableWidgetEnvironment.setColumnCount(len(matrix[0]))
		for i,row in enumerate(matrix):
			for j,val in enumerate(row):
				self.tableWidgetEnvironment.setItem(i,j,QTableWidgetItem(str(val)))

	def move_robot(self):
		pass

	def look_graph(self):
		pass

	def fast_search(self):
		pass

	def step_search(self):
		pass