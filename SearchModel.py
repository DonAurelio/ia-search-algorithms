from Node import Node
import networkx as nx 
from networkx.drawing.nx_agraph import write_dot
from networkx.drawing.nx_agraph import graphviz_layout
from os import remove
import matplotlib.pyplot as plt

#Represent the model of the problem 
class SearchModel:

	#Enviroments components 
	START = 0
	WALL = 1
	FREE_SPACE = 2
	SLIPPERY_FLOOR = 3
	PEOPLE = 4
	RESTRICTED = 5
	RELOAD = 6
	GOAL = 7
	#Enviroment costs
	START_COST = 1
	#WALL_COST = 1
	FREE_SPACE_COST = 1
	SLIPPERY_FLOOR_COST = 3
	PEOPLE_COST = 4
	RESTRICTED_COST = 6
	RELOAD_COST = 5
	GOAL_COST = 1

	#Posible actions
	Action = {0:'UP', 1:'DOWN', 2:'LEFT', 3:'RIGHT'}
	
	
	def __init__(self,observer,environment,dimension,avoid_cycles):

		#Dimension of environment problem 
		self.dimension = dimension
		#Environment
		self.env = environment
		#graphic that contain the grafical tree representation
		self.tree_graph = nx.DiGraph()
		#Is necesary to declare an observer to pass
		#the informations during the search to user interface
		self.observer = observer
		#Represents the initial position of the robot 
		#into the environment
		self.init_state = self.search_position_of(0)
		#Represents the goal node, when the algorithm find 
		#the goal, this sets this variable 
		self.goal_node = None 
		#Represents the first node of the problem 
		self.init_node = Node(self.init_state,None,'',0,0,None)
		#Include the node in the graphic
		self.add_nodes_to_tree_graph(None,self.init_node)
		#The number of expand nodes 
		self.number_expand_nodes = 0
		#The number of create nodes
		self.number_create_nodes = 0
		#is a flag that indicate if the search can avoid cycles
		self.avoid_cycles = avoid_cycles
		
	
	#Calculate the cost of state (i,j) according 
	#to the object that is in (i,j) coodinates
	def calculate_cost(self, state):

		#extract i component from starte (i,j)
		i = state[0]
		#extract j component from state (i,j)
		j = state[1]

		#Determine the cost depending what object there
		#is on the position (i,j)
		if ((self.env[i][j] == self.START)
			or (self.env[i][j] == self.FREE_SPACE)
			or (self.env[i][j] == self.GOAL)):
			return self.FREE_SPACE_COST
		
		if ((self.env[i][j]) == self.SLIPPERY_FLOOR):
			return self.SLIPPERY_FLOOR_COST

		if ((self.env[i][j]) == self.PEOPLE):
			return self.PEOPLE_COST

		if (self.env[i][j] == self.RESTRICTED):
			return self.RESTRICTED_COST

		if (self.env[i][j] == self.RELOAD):
			return self.RELOAD_COST

	#Determine if node represents a goal of the problem
	def is_goal(self,node):
		state = node.state
		i = state[0]
		j = state[1]
		return (self.env[i][j] == self.GOAL)


	#Allow to expand a node (create sons)
	def expand(self, node):
		new_nodes = []
		up = (node.state[0]-1, node.state[1])
		down = (node.state[0]+1, node.state[1])
		left = (node.state[0], node.state[1]-1)
		right = (node.state[0], node.state[1]+1)
		states = (up,down,left,right)

		if self.validate_action(up,node):
			cost = node.cost + self.calculate_cost(up)
			new_nodes.append(Node(up, node, self.Action[0], cost, node.depth + 1,None))

		if self.validate_action(down,node):
			cost = node.cost + self.calculate_cost(down)
			new_nodes.append(Node(down, node, self.Action[1], cost, node.depth + 1,None))

		if self.validate_action(left,node):
			cost = node.cost + self.calculate_cost(left)
			new_nodes.append(Node(left, node, self.Action[2], cost, node.depth + 1,None))

		if self.validate_action(right,node):
			cost = node.cost + self.calculate_cost(right)
			new_nodes.append(Node(right, node, self.Action[3], cost, node.depth + 1,None))

		#Problems with nodes cost calculation and depth
		#for i in range(len(states)):
		#	if self.validate_action(states[i]) == True:
		#		#cost = node.get_cost() + self.calculate_cost(states[i])
		#		cost = node.get_cost() + 1
		#		print(str(node)+":"+str(cost)+" - "+str(i))
		#		node = Node(states[i], node, self.Action[i], cost, node.depth + 1)
		#		new_nodes.append(node)

		return new_nodes

				
	#Evaluate if an state (i,j) is posible on the 
	#problem environment (E.g: (-1,2) is not a valid state)
	#or if there is a wall in state (i,j) then (i,j) is not valid state
	def validate_action(self,state,parent_node):
		i = state[0]
		j = state[1]
		real_dimension = self.dimension - 1
		
		if self.avoid_cycles == True:
			if self.check_cycle(state,parent_node):
				return False

		if (state[0] < 0) or (state[1] < 0):
			return False
		elif (state[0] > real_dimension) or (state[1] > real_dimension):
			return False
		elif self.env[i][j] == self.WALL:
			return False
		else:
			return True


	#Check if the state is in the node or node parents 
	#The purpose of this method is check if the given statet
	#is in the branch of a given none
	def check_cycle(self,state,parent_node):
		while parent_node != None:
			if parent_node.state == state:
				return True
			parent_node = parent_node.parent
		return False




	#Search a number into the environment and 
	#returns the position of that variable
	#if number is not into the environment
	#returns (-1,-1)
	def search_position_of(self, number):
    	
		for i in range(self.dimension):
		    row = self.env[i]
		    for j in range(self.dimension):
		        col = row[j]
		        if col == number:
		            return (i, j)

		return (-1, -1)

	#Allow to add nodes to self.tree_graph that is a
	#graphical representation of create nodes
	def add_nodes_to_tree_graph(self,parent,sons):
		# if sons dont have parent, sons is the parent
		if parent == None:
			atrributes = {'state':sons.state,'action':sons.action,'cost':sons.cost,'heuristic':sons.heuristic,'total_cost':sons.total_cost}
			self.tree_graph.add_node(sons.number,atrributes)
			
		else:
			for son in sons:
				atrributes = {'state':son.state,'action':son.action,'cost':son.cost,'heuristic':son.heuristic,'total_cost':son.total_cost}
				self.tree_graph.add_node(son.number,atrributes)
				self.tree_graph.add_edge(parent.number,son.number)
				
		
		
	
	#This is a template method that have to define 
	#the sons of this class according to the type of search
	#that the programer implements
	def show_tree_graph(self):
		write_dot(self.tree_graph,'test.dot')
		pos=graphviz_layout(self.tree_graph,prog='dot')
		nx.draw(self.tree_graph,pos,with_labels=True,arrows=False)

		for i in nx.nodes(self.tree_graph):
			x,y=pos[i]
			node_atrributes = self.tree_graph.node[i]
			text = str(node_atrributes['state']) + "\n"
			text += str(node_atrributes['action']) + "\n"
			text += "c(n)=" + str(node_atrributes['cost']) + "\n"
			text += "h(n)=" + str(node_atrributes['heuristic']) + "\n"
			text += "g(n)=" + str(node_atrributes['total_cost']) + "\n"
			#bbox=dict(facecolor='red', alpha=0)
			plt.text(x,y+10,s=text, fontsize=7,horizontalalignment='left')

		plt.savefig("serch_tree.jpeg")
		plt.show()


	#This is a template method that have to define 
	#the sons of this class accordin to the type of search
	#that the programer implements 
	def start_iterative_search(self):
		pass


	#This is a template method that have to define 
	#the sons of this class accordin to the type of search
	#that the programer implements 
	def start_iterarive_step(self):
		pass


	#This is a template method that have to define 
	#the sons of this class according to the type of search
	#that the programer implements
	def get_number_expand_nodes(self):
		pass

	#This is a template method that have to define 
	#the sons of this class according to the type of search
	#that the programer implements
	def get_number_create_nodes(self):
		pass

	#This is a template method that have to define 
	#the sons of this class according to the type of search
	#that the programer implements
	#Allow return the goal node 
	def get_goal_node(self):
		pass

	#This is a template method that have to define 
	#the sons of this class according to the type of search
	#that the programer implements
	#Create a list with the best states (i,j)
	#solution. (E.g. [(0,0),(1,2),(1,3)]
	def get_best_way(self):
		pass

	#This is a template method that have to define 
	#the sons of this class according to the type of search
	#that the programer implements
	#Create a list with the best direcction "UP","DOWN","LEFT","RIGHT"
	#solution
	def get_best_direcctions(self):
		pass


	#This is a template method that have to define 
	#the sons of this class according to the type of search
	#that the programer implements
	#Allow to get the variable self.init_state
	def get_init_state(self):
		pass

	