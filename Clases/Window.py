from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from Observer import Observer
from LoadFile import LoadFile
from Robot import Robot

M_Window_UI_class,M_Window_UI_Base_class = uic.loadUiType('gui/MainWindow.ui')

class Window(QMainWindow,M_Window_UI_class,Observer):

	def __init__(self, parent=None):
		
		QMainWindow.__init__(self,parent)
		self.setupUi(self)
		self.setWindowTitle("Located Me Univalle")

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
		self.connect(self.actionUniformCost_2,SIGNAL("triggered()"),self.select_uniform_cost_search)

		loadFile = LoadFile("env.txt")
		self.dimension , self.environment = loadFile.read()
		
		self.queue_dimension = 100

		self.update_tree_graph()
		

	def clear_components(self):
		self.tableWidgetEnvironment.clear()
		self.plainTextEditDataStatus.setPlainText("")
		self.plainTextEditRobotStatus.setPlainText("")
		self.lineEditState.setText("")
		self.lineEditParent.setText("")
		self.lineEditAction.setText("")
		self.lineEditCost.setText("")
		self.lineEditDepth.setText("")


	def draw_environment(self,environment):
		matrix = environment
		self.tableWidgetEnvironment.setRowCount(len(matrix))
		self.tableWidgetEnvironment.setColumnCount(len(matrix[0]))
		for i,row in enumerate(matrix):
			for j,val in enumerate(row):
				if self.robot.actual_position == (i,j):
					self.tableWidgetEnvironment.setItem(i,j,QTableWidgetItem("R"))
				else:
					self.tableWidgetEnvironment.setItem(i,j,QTableWidgetItem(str(val)))

	def update_tree_graph(self):
		pixmap = QPixmap("serch_tree.jpeg")
		scaled_pixmap = pixmap.scaled(261,341)
		self.labelTreeGraph.setPixmap(scaled_pixmap)
		self.labelTreeGraph.show()

	def select_uniform_cost_search(self):
		self.clear_components()
		self.robot = Robot(self,self.environment,self.dimension,self.queue_dimension,"UniformCost")
		self.labelSelectedSearch.setText("UniformCost")
		self.draw_environment(self.environment)
		self.plainTextEditRobotStatus.appendPlainText("Ready .......")

		self.update_tree_graph()

		self.pushButtonMoveRobot.setEnabled(False)
		self.pushButtonLookGraph.setEnabled(True)
		self.pushButtonFastSearch.setEnabled(True)
		self.pushButtonNextStep.setEnabled(True)
	

	
	def fast_search(self):
		result = 3
		while result == 3:
			result = self.step_search()
			self.update_tree_graph()

	def step_search(self):
		result = self.robot.iterative_step()
		if result == 1:
			self.printRobotMassage("I already find the goal")
			way = self.robot.get_best_way()
			self.printRobotMassage("The minimal cost way is: " + str(way))
			directions = self.robot.get_best_direcctions()
			self.printRobotMassage("The route that I have to do is: " + str(directions))
			self.pushButtonFastSearch.setEnabled(False)
			self.pushButtonNextStep.setEnabled(False)
			self.pushButtonMoveRobot.setEnabled(True)
		elif result == 2:
			self.plainTextEditRobotStatus.appendPlainText("I cant move more")
			self.pushButtonFastSearch.setEnabled(False)
			self.pushButtonNextStep.setEnabled(False)
		self.update_tree_graph()
		return result


	def move_robot(self):
		pass

	def look_graph(self):
		pass

	def printRobotMassage(self,massage):
		self.plainTextEditRobotStatus.appendPlainText(massage)

	def update_from_search_node(self,data):
		self.lineEditState.setText(str(data[0]))
		self.lineEditParent.setText(str(data[1]))
		self.lineEditAction.setText(str(data[2]))
		self.lineEditCost.setText(str(data[3]))
		self.lineEditDepth.setText(str(data[4]))

	def update_from_search_queue(self,data):
		self.plainTextEditDataStatus.appendPlainText(str(data))

