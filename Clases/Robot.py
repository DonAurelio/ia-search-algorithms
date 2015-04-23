from Observer import Observer
from UniformCost import UniformCost

class Robot:

	def __init__(self,observer,environment,dimension,queue_dimension, search_tipe="UniformCost"):
		
		self.search_algorithm = None
		if search_tipe == "UniformCost":
			self.search_algorithm = UniformCost(observer,environment,dimension,queue_dimension)
		elif search_tipe == "A*h1":
			pass
		elif search_tipe == "A*h2":
			pass
		
		self.battery = 6
		self.observer = observer
		self.environment = environment
		self.actual_position =  self.search_algorithm.get_init_state()
		self.best_way = []



	def download_battery(self):
		self.battery = self.battery - 1
	
	def reload_battery(self):
		self.battery = 6

	def get_best_way(self):
		self.best_way = self.search_algorithm.get_best_way()
		return self.best_way

	def move_one_step(self):
		if self.best_way != []:
			if self.battery != 0:
				self.actual_position = self.best_way.pop(0)
				self.download_battery()
				self.observer.update_from_robot("Battery state: " + str(self.battery))
				x_coodinate = self.actual_position[0]
				y_coordinate = self.actual_position[1]
				print(x_coodinate)
				print(y_coordinate)
				if self.environment[int(x_coodinate)][int(y_coordinate)] == self.search_algorithm.RELOAD:
					self.reload_battery()
					self.observer.update_from_robot("Reload battery: " + str(self.battery))
			else:
				self.observer.update_from_robot("I can't move, battery state: " + str(self.battery))



	def get_best_direcctions(self):
		return self.search_algorithm.get_best_direcctions()
		

	def iterative_step(self):
		return self.search_algorithm.start_iterarive_step()

	def iterative_search(self):
		return self.search_algorithm.start_iterative_search()

	def show_tree_graph(self):
		self.search_algorithm.show_tree_graph()

	
