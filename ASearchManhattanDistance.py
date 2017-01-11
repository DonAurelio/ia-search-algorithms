from UniformCost import UniformCost
from Node import Node
from math import sqrt

class ASearchManhattanDistance(UniformCost):

	def __init__(self,observer, enviroment, dimension, queue_dimension,avoid_cycle,numerator,denominator):
		UniformCost.__init__(self,observer, enviroment, dimension, queue_dimension,avoid_cycle)
		self.numerator = numerator
		self.denominator = denominator
		
		self.goal_state = self.search_position_of(7)
		distance_to_goal = self.calculate_distance_to_goal(self.init_state)
		heuristic = (distance_to_goal*self.numerator)/self.denominator
			

	def expand(self,node):
		new_nodes = []
		up = (node.state[0]-1, node.state[1])
		down = (node.state[0]+1, node.state[1])
		left = (node.state[0], node.state[1]-1)
		right = (node.state[0], node.state[1]+1)
		states = (up,down,left,right)

		if self.validate_action(up,node):
			cost = node.cost + self.calculate_cost(up)
			distance_to_goal = self.calculate_distance_to_goal(up)
			heuristic = (distance_to_goal*self.numerator)/self.denominator
			new_nodes.append(Node(up, node, self.Action[0], cost, node.depth + 1,heuristic))

		if self.validate_action(down,node):
			cost = node.cost + self.calculate_cost(down)
			distance_to_goal = self.calculate_distance_to_goal(down)
			heuristic = (distance_to_goal*self.numerator)/self.denominator
			new_nodes.append(Node(down, node, self.Action[1], cost, node.depth + 1,heuristic))

		if self.validate_action(left,node):
			cost = node.cost + self.calculate_cost(left)
			distance_to_goal = self.calculate_distance_to_goal(left)
			heuristic = (distance_to_goal*self.numerator)/self.denominator
			new_nodes.append(Node(left, node, self.Action[2], cost, node.depth + 1,heuristic))

		if self.validate_action(right,node):
			cost = node.cost + self.calculate_cost(right)
			distance_to_goal = self.calculate_distance_to_goal(right)
			heuristic = (distance_to_goal*self.numerator)/self.denominator
			new_nodes.append(Node(right, node, self.Action[3], cost, node.depth + 1,heuristic))

		return new_nodes

	# The cost of heuristics corresponds to the Manhattan Distance
	# between the target node and the current node
	def calculate_distance_to_goal(self,state):

		goal_node_position_x = self.goal_state[0]
		goal_node_position_y = self.goal_state[1]
		state_x = state[0]
		state_y = state[1]

		distance = abs(goal_node_position_x - state_x) +abs(goal_node_position_y - state_y)
		print("Distancia manhattan: " + str(distance))
		return distance


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
					#this part was modifing to include the total const like 
					#criteria to the priority queue
					self.queue.put((a_new_node.total_cost,a_new_node))
					new_nodes_string = new_nodes_string + str(a_new_node) + " " 

				#Se imprimen los nodos nuevos que se colocaron en la cola
				new_nodes_string = new_nodes_string + "]"
				self.observer.update_from_search_queue("Push: " + new_nodes_string)

				self.number_create_nodes += len(new_nodes)

			self.add_nodes_to_tree_graph(node,new_nodes)
		return 3


