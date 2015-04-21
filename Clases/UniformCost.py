import Queue
from Node import Node
from SearchModel import SearchModel
import Queue

class UniformCost(SearchModel):

	def __init__(self,observer, enviroment, dimension, queue_dimension):
		SearchModel.__init__(self,enviroment,dimension)
		
		self.observer = observer

		self.queue = Queue.PriorityQueue(queue_dimension)
		self.init_state = self.search_start()
		self.init_node = Node(self.init_state,None,'',0,0)
		self.goal_node = None 
		self.queue.put((0,self.init_node))


	def get_goal_node(self):
		return self.goal_node

	def get_best_way(self):
		node = self.goal_node
		way = []
		
		while node != None:	
			state = node.state
			way.insert(0,state)
			node = node.parent
		return way

	def get_best_direcctions(self):
		node = self.goal_node
		direcctions = []
		
		while node != None:
			state = node.action
			direcctions.insert(0,state)
			node = node.parent
		return direcctions



	def get_init_state(self):
		return self.init_state

	def start_iterative_search(self):
		
		result = 3
		while result == 3:
			result = self.start_iteartive_step()
		return result
			

	#Funcion:start_iteartive_step:
	#Proposito:Realiza un paso de la busqueda por costo uniforme 
	#retorna: 1 si se encontro la meta
	#retorna: 2 cuando ya no hay movimientos posibles
	#retorna: 3 en cualquier oro caso 
	def start_iterarive_step(self):

		node = self.queue.get()[1]
				
		data = {0:node.state,1:node.parent,2:node.action,3:node.cost,4:node.depth}
		self.observer.update_from_search_node(data)

		self.observer.update_from_search_queue("Pop: " + str(node))
		
		if(self.is_goal(node)):
			self.goal_node = node
			return 1
		
		else:
			
			new_nodes = self.expand(node)
			new_nodes_string = "[ "
			if(self.queue.empty()) and new_nodes == []:
				return 2
			else:
				for a_new_node in new_nodes:
					self.queue.put((a_new_node.cost,a_new_node))
					new_nodes_string = new_nodes_string + str(a_new_node) + " " 

				#Se imprimen los nodos nuevos que se colocaron en la cola
				new_nodes_string = new_nodes_string + "]"
				self.observer.update_from_search_queue("Push: " + new_nodes_string)

		return 3



	
