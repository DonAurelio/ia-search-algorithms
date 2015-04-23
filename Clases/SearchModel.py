from Node import Node
import networkx as nx 
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

	
	def __init__(self, environment, dimension):

		#Dimension of environment problem 
		self.dimension = dimension
		#Environment
		self.env = environment
		#graphic that contain the grafical tree representation
		self.tree_graph = nx.DiGraph()
		
	
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

		if self.validate_action(up):
			cost = node.cost + self.calculate_cost(up)
			new_nodes.append(Node(up, node, self.Action[0], cost, node.depth + 1))

		if self.validate_action(down):
			cost = node.cost + self.calculate_cost(down)
			new_nodes.append(Node(down, node, self.Action[1], cost, node.depth + 1))

		if self.validate_action(left):
			cost = node.cost + self.calculate_cost(left)
			new_nodes.append(Node(left, node, self.Action[2], cost, node.depth + 1))

		if self.validate_action(right):
			cost = node.cost + self.calculate_cost(right)
			new_nodes.append(Node(right, node, self.Action[3], cost, node.depth + 1))

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
	def validate_action(self, state):
		i = state[0]
		j = state[1]
		if self.env[i][j] == self.WALL:
			return False
		elif (state[0] < 0) or (state[1] < 0):
			return False
		elif (state[0] > self.dimension) or (state[1] > self.dimension):
			return False
		else:
			return True


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
			self.tree_graph.add_node(sons.number)
			
		else:
			for son in sons:
				self.tree_graph.add_node(son.number)
				self.tree_graph.add_edge(parent.number,son.number)
				
		
		nx.write_dot(self.tree_graph,'test.dot')
		pos=nx.graphviz_layout(self.tree_graph,prog='dot')
		nx.draw(self.tree_graph,pos,with_labels=True,arrows=False)
		
			
		plt.savefig("serch_tree.jpeg")
		#plt.show()
		#plt.draw()

		
	def show_tree_graph(self):
		plt.show()


	#This a template method that have to define 
	#the sons of this class accordin to the type of search
	#that the programer implements 
	def start_iterative_search(self):
		pass


	#This a template method that have to define 
	#the sons of this class accordin to the type of search
	#that the programer implements 
	def start_iterarive_step(self):
		pass
