import Queue
from Node import Node
from SearchModel import SearchModel
import Queue


#Allow to do, uniform cost search algoritm
#according to the SearchModel, this contains the model of de problem
class UniformCost(SearchModel):

	def __init__(self,observer, enviroment, dimension, queue_dimension):
		SearchModel.__init__(self,observer,enviroment,dimension)
		
		#Queue is an especific data estructure to implement
		#uniform cost search
		self.queue = Queue.PriorityQueue(queue_dimension)

		#Is necesary to put the fisrt node into the queue
		self.queue.put((0,self.init_node))


	#Allow to get the number of expands nodes
	def get_number_expand_nodes(self):
		return self.number_expand_nodes

	#Allow to get the number of create nodes
	def get_number_create_nodes(self):
		return self.number_create_nodes

	#Allow return the goal node 
	def get_goal_node(self):
		return self.goal_node

	#Create a list with the best states (i,j)
	#solution. (E.g. [(0,0),(1,2),(1,3)]
	def get_best_way(self):
		node = self.goal_node
		way = []
		
		while node != None:	
			if node == self.init_node:
				node = node.parent
			else:
				state = node.state
				way.insert(0,state)
				node = node.parent
		return way

	#Create a list with the best direcction "UP","DOWN","LEFT","RIGHT"
	#solution
	def get_best_direcctions(self):
		node = self.goal_node
		direcctions = []
		
		while node != None:
			if node == self.init_node:
				node = node.parent
			else:
				state = node.action
				direcctions.insert(0,state)
				node = node.parent
		return direcctions


	#Allow to get the variable self.init_state
	def get_init_state(self):
		return self.init_state

	#Allow to call repeat times to the function 
	#start_iterarive_step to do a fast search
	def start_iterative_search(self):
		result = 3
		while result == 3:
			result = self.start_iteartive_step()
		return result
	
					

	#Allo to do the serach by step
	#return: 1 if this finds the goal
	#return: 2 when is not posible more movements 
	#return: 3 otherwise
	def start_iterarive_step(self):

		node = self.queue.get()[1]

				
		data = {0:node.state,1:node.parent,2:node.action,3:node.cost,
		4:node.depth,5:node.heuristic,6:node.total_cost}

		self.observer.update_from_search_node(data)

		self.observer.update_from_search_queue("Pop: " + str(node))
		self.number_expand_nodes += 1
		
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

				self.number_create_nodes += len(new_nodes)

			self.add_nodes_to_tree_graph(node,new_nodes)
		return 3



	
