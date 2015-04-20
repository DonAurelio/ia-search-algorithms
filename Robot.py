from Observer import Observer

class Robot:

	def __init__(self,observer,environment,dimension,queue_dimension, search_tipe="UniformCost"):
		
		battery = 6
		self.observer = observer
		self.search_algorithm = None
		if search_tipe == "UniformCost":
			self.search_algorithm = UniformCost(environment,dimension,queue_dimension)
		elif search_tipe == "A*h1":
			pass
		elif search_tipe == "A*h2":
			pass
		


	def get_battery_state(self):
		return self.battery

	def download_battery(self):
		self.battery = self.battery - 1
	
	def reload_battery(self):
		self.battery = 6

	def iterative_step(self):
		return self.search_algorithm.start_iterative_step()

	def iterative_search(self):
		return self.search_algorithm.start_iterative_search()

	
