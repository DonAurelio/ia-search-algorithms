from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from sys import exit
from Observer import Observer
from LoadFile import LoadFile
from Robot import Robot
from SearchModel import SearchModel

D_Message_UI_class, D_Message_UI_Base_class = uic.loadUiType('gui/DialogMessage.ui')

class DialogMessage(QDialog,D_Message_UI_class):

	def __init__(self,message,parent=None):
		QDialog.__init__(self,parent)
		self.setupUi(self)
		self.plainTextEditMessage.setPlainText(message)
		self.exec_()

D_Option_UI_class, D_Option_UI_Base_class = uic.loadUiType('gui/DialogOption.ui')

class DialogOption(QDialog,D_Option_UI_class):

	def __init__(self,parent=None):
		QDialog.__init__(self,parent)
		self.setupUi(self)

		self.connect(self.pushButtonYes,SIGNAL('clicked()'),self.set_taken_option_true)
		self.connect(self.pushButtonNo,SIGNAL('clicked()'),self.set_taken_option_false)

	def display_option_message(self,message):
		self.plainTextEditMessage.setPlainText(message)
		self.exec_()

	def set_taken_option_true(self):
		self.taken_option = True
		self.reject()

	def set_taken_option_false(self):
		self.taken_option = False
		self.reject()

	def get_taken_option(self):
		return self.taken_option



D_Editor_UI_class, D_Editor_UI_Base_class = uic.loadUiType('gui/DialogEnvironmentEditor.ui')

class DialogEnvironmentEditor(QDialog,D_Editor_UI_class):

	def __init__(self,parent=None):
		QDialog.__init__(self,parent=parent)
		self.setupUi(self)
		self.environment_size = 0
		self.environment = []
		self.dictionary_objects = {"Inicio":0,"Pared":1,"Espacio":2,"Resvaloso":3,"Personas":4,"Restrindigo":5,"Recarga":6,"Meta":7}
		self.start_position = None
		self.goal_position = None
		self.set_combobox_values()

		self.connect(self.pushButtonEnvironmentSize,SIGNAL('clicked()'),self.set_environment_size)
		self.connect(self.tableWidgetEnvironment,SIGNAL('cellClicked(int,int)'),self.set_environment)
		self.connect(self.pushButtonSave,SIGNAL('clicked()'),self.save_environment)

	def set_combobox_values(self):
		self.comboBoxEnvironmentObject.addItem("Inicio")
		self.comboBoxEnvironmentObject.addItem("Pared")
		self.comboBoxEnvironmentObject.addItem("Espacio")
		self.comboBoxEnvironmentObject.addItem("Resvaloso")
		self.comboBoxEnvironmentObject.addItem("Personas")
		self.comboBoxEnvironmentObject.addItem("Restrindigo")
		self.comboBoxEnvironmentObject.addItem("Recarga")
		self.comboBoxEnvironmentObject.addItem("Meta")

	def set_environment_size(self):
		self.environment_size = self.spinBoxEnvironmentSize.value()

		self.tableWidgetEnvironment.setEnabled(True)
		self.comboBoxEnvironmentObject.setEnabled(True)
		self.pushButtonSave.setEnabled(True)

		self.create_environment()

	def create_environment(self):
		self.environment = [[SearchModel.FREE_SPACE] * self.environment_size for i in range(self.environment_size)]
		self.draw_environment()


	def draw_environment(self):
		matrix = self.environment
		self.tableWidgetEnvironment.setRowCount(self.environment_size)
		self.tableWidgetEnvironment.setColumnCount(self.environment_size)
		for i,row in enumerate(matrix):
			for j,val in enumerate(row):
				self.tableWidgetEnvironment.setItem(i,j,QTableWidgetItem(str(val)))

	def set_environment(self,row,column):
		selected_object = self.comboBoxEnvironmentObject.currentText()
		new_value = self.dictionary_objects[str(selected_object)] 
		self.environment[row][column] = new_value

		if (row,column) == self.start_position:
			self.start_position = None
		if (row,column) == self.goal_position:
			self.goal_position = None

		if str(new_value) == str(SearchModel.START):
			if self.start_position != None:
				s_row = self.start_position[0]
				s_column = self.start_position[1]
				new_value = str(SearchModel.FREE_SPACE)
				self.environment[s_row][s_column] = new_value
			self.start_position = (row,column)
		
		if str(new_value) == str(SearchModel.GOAL):
			if self.goal_position != None:
				s_row = self.goal_position[0]
				s_column = self.goal_position[1]
				new_value = str(SearchModel.FREE_SPACE)
				self.environment[s_row][s_column] = new_value
			self.goal_position = (row,column)
		
		self.draw_environment()


	def save_environment(self):
		if self.start_position == None or self.goal_position == None:
			message = "Please insert the goal and the start values"
			DialogMessage(message,self)
		else:


			string_environment = str(self.environment_size) + "\n"
			for row in self.environment:
				for value in row:
					string_environment += str(value) + " "
				string_environment += "\n"

			env_file = open("env.txt",'w')
			env_file.write(string_environment)
			env_file.close()

			message = "A new environment save success"
			DialogMessage(message,self)




M_Window_UI_class,M_Window_UI_Base_class = uic.loadUiType('gui/MainWindow.ui')

class Window(QMainWindow,M_Window_UI_class,Observer):

	def __init__(self,parent=None):
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
		
		self.connect(self.actionUniformCostSearch,SIGNAL("triggered()"),self.select_uniform_cost_search)
		self.connect(self.actionARectDistance,SIGNAL('triggered()'),self.select_a_rect_distance_search)
		self.connect(self.actionExit,SIGNAL("triggered()"),exit)
		self.connect(self.actionCreateEnvironment,SIGNAL("triggered()"),self.display_environment_editor)
		self.connect(self.actionLookActualEnvironment,SIGNAL("triggered()"),self.look_actual_environment)


		self.queue_dimension = 0

		self.robot = None

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
		self.lineEditH.setText("")
		self.lineEditG.setText("")

	def load_environment(self):
		loadFile = LoadFile("env.txt")
		self.dimension , self.environment = loadFile.read()


	def draw_environment(self):
		matrix = self.environment
		self.tableWidgetEnvironment.setRowCount(len(matrix))
		self.tableWidgetEnvironment.setColumnCount(len(matrix[0]))
		for i,row in enumerate(matrix):
			for j,val in enumerate(row):
				if self.robot.actual_position == (i,j):
					self.tableWidgetEnvironment.setItem(i,j,QTableWidgetItem("R"))
				else:
					self.tableWidgetEnvironment.setItem(i,j,QTableWidgetItem(str(val)))

	def look_actual_environment(self):
		loadFile = LoadFile("env.txt")
		dimension , environment = loadFile.read()

		matrix = environment
		self.tableWidgetEnvironment.setRowCount(len(matrix))
		self.tableWidgetEnvironment.setColumnCount(len(matrix[0]))
		for i,row in enumerate(matrix):
			for j,val in enumerate(row):
				self.tableWidgetEnvironment.setItem(i,j,QTableWidgetItem(str(val)))

		

	def select_uniform_cost_search(self):

		self.load_environment()
		self.clear_components()

		self.optionDialog = DialogOption()
		self.optionDialog.display_option_message("Do you want avoid cycles")
		option_response = self.optionDialog.get_taken_option()
		
		self.robot = Robot(self,self.environment,self.dimension,self.queue_dimension,"UniformCost",option_response)

		if option_response:
			self.labelSelectedSearch.setText("UniformCost avoiding cycles")
		else:
			self.labelSelectedSearch.setText("UniformCost with cycles")

		self.draw_environment()
		self.plainTextEditRobotStatus.appendPlainText("Ready .......")
		self.update_tree_graph()

		self.pushButtonMoveRobot.setEnabled(False)
		self.pushButtonLookGraph.setEnabled(True)
		self.pushButtonFastSearch.setEnabled(True)
		self.pushButtonNextStep.setEnabled(True)

	def select_a_rect_distance_search(self):

		self.load_environment()
		self.clear_components()

		self.optionDialog = DialogOption()
		self.optionDialog.display_option_message("Do you want avoid cycles")
		option_response = self.optionDialog.get_taken_option()
		
		self.robot = Robot(self,self.environment,self.dimension,self.queue_dimension,"A*h1",option_response)

		if option_response:
			self.labelSelectedSearch.setText("A* Rect Disntance avoiding cycles")
		else:
			self.labelSelectedSearch.setText("A* Rect Disntance with cycles")

		self.draw_environment()
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
		return result

	def step_search(self):
		result = self.robot.iterative_step()
		if result == 1:
			self.pushButtonFastSearch.setEnabled(False)
			self.pushButtonNextStep.setEnabled(False)
			self.pushButtonMoveRobot.setEnabled(True)
		elif result == 2:
			self.pushButtonFastSearch.setEnabled(False)
			self.pushButtonNextStep.setEnabled(False)
		self.update_tree_graph()
		return result
		

	def move_robot(self):
		self.robot.move_one_step()
		self.draw_environment()

	def look_graph(self):
		self.robot.show_tree_graph()

	def printRobotMassage(self,massage):
		self.plainTextEditRobotStatus.appendPlainText(massage)

	def display_environment_editor(self):
		editor = DialogEnvironmentEditor(self)
		editor.exec_()


	def update_tree_graph(self):
		pixmap = QPixmap("serch_tree.jpeg")
		scaled_pixmap = pixmap.scaled(261,341)
		self.labelTreeGraph.setPixmap(scaled_pixmap)
		self.labelTreeGraph.show()

	def update_from_search_node(self,data):
		self.lineEditState.setText(str(data[0]))
		self.lineEditParent.setText(str(data[1]))
		self.lineEditAction.setText(str(data[2]))
		self.lineEditCost.setText(str(data[3]))
		self.lineEditDepth.setText(str(data[4]))
		self.lineEditH.setText(str(data[5]))
		self.lineEditG.setText(str(data[6]))

	def update_from_search_queue(self,data):
		self.plainTextEditDataStatus.appendPlainText(str(data))

	def update_from_robot(self,data):
		self.plainTextEditRobotStatus.appendPlainText(str(data))

