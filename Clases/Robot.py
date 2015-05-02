from Observer import Observer
from UniformCost import UniformCost
from ASearchRectDistance import ASearchRectDistance

class Robot:

	def __init__(self,observer,environment,dimension,queue_dimension,search_tipe,avoid_cycle,numerator=1,denominator=1):
		
		self.search_algorithm = None
		if search_tipe == "UniformCost":
			self.search_algorithm = UniformCost(observer,environment,dimension,queue_dimension,avoid_cycle)
		elif search_tipe == "A*h1":
			self.search_algorithm = ASearchRectDistance(observer,environment,dimension,queue_dimension,avoid_cycle,numerator,denominator)
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
				if self.environment[int(x_coodinate)][int(y_coordinate)] == self.search_algorithm.RELOAD:
					self.reload_battery()
					self.observer.update_from_robot("Reload battery: " + str(self.battery))
				if self.environment[int(x_coodinate)][int(y_coordinate)] == self.search_algorithm.GOAL:
					self.observer.update_from_robot("I already be on the goal")
			else:
				self.observer.update_from_robot("I can't move, battery state: " + str(self.battery))

		



	def get_best_direcctions(self):
		return self.search_algorithm.get_best_direcctions()

	def iterative_step(self):
		result = self.search_algorithm.start_iterarive_step()
		if result == 1:
		
			way = self.get_best_way()
			directions = self.get_best_direcctions()
			number_expand_nodes = self.search_algorithm.get_number_expand_nodes()
			number_create_nodes = self.search_algorithm.get_number_create_nodes()

			self.observer.update_from_robot("I already find the goal")
			self.observer.update_from_robot("The minimal cost way is: " + str(way))
			self.observer.update_from_robot("The route that I have to do is: " + str(directions))
			self.observer.update_from_robot("The number of expand nodes is: " + str(number_expand_nodes))
			self.observer.update_from_robot("The number of create nodes is: " + str(number_create_nodes))
		
		elif result == 2:
			self.observer.update_from_robot("The Queue is empty, I can't find solution")
		
		return result
		
	def iterative_search(self):
		result =  self.search_algorithm.start_iterative_search()
		
		if result == 1:

			way = self.get_best_way()
			directions = self.get_best_direcctions()
			number_expand_nodes = self.search_algorithm.get_number_expand_nodes()
			number_create_nodes = self.search_algorithm.get_number_create_nodes()

			self.observer.update_from_robot("I already find the goal")
			self.observer.update_from_robot("The minimal cost way is: " + str(way))
			self.observer.update_from_robot("The route that I have to do is: " + str(directions))
			self.observer.update_from_robot("The number of expand nodes is: " + str(number_expand_nodes))
			self.observer.update_from_robot("The number of create nodes is: " + str(number_create_nodes))
		
		elif result == 2:
			self.observer.update_from_robot("The Queue is empty, I can't find solution")
		
		return result

	def show_tree_graph(self):
		self.search_algorithm.show_tree_graph()

	
