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
		
		battery = 6
		self.observer = observer
		self.environment = environment
		self.actual_position =  self.search_algorithm.get_init_state()



	def download_battery(self):
		self.battery = self.battery - 1
	
	def reload_battery(self):
		self.battery = 6

	def get_best_way(self):
		return self.search_algorithm.get_best_way()

	def get_best_direcctions(self):
		return self.search_algorithm.get_best_direcctions()
		

	def iterative_step(self):
		return self.search_algorithm.start_iterarive_step()

	def iterative_search(self):
		return self.search_algorithm.start_iterative_search()

	
