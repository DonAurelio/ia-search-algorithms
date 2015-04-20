from Node import Node

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

		self.dimension = dimension
		self.env = environment
		
		
	def result_cost(self, state):
		""" Funcion que retorna el costo de pasar por un estado especificado.
		Mapea una posicion a su costo """
		i = state[0]
		j = state[1]

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

	def is_goal(self,node):
		state = node.state
		i = state[0]
		j = state[1]
		return (self.env[i][j] == self.GOAL)


	#Overrride method from SearchModel
	def expand(self, node):
		new_nodes = []
		up = (node.state[0]-1, node.state[1])
		down = (node.state[0]+1, node.state[1])
		left = (node.state[0], node.state[1]-1)
		right = (node.state[0], node.state[1]+1)
		states = (up,down,left,right)

		for i in range(len(states)):
			if self.validate_action(states[i]) == True:
				cost = node.cost + self.result_cost(states[i])
				node = Node(states[i], node, self.Action[i], cost, node.depth + 1)
				new_nodes.append(node)

		return new_nodes

				

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


	# mover a searchmodel
	def search_start(self):
    # Busca un item en la matriz, si lo encuentra retorna la  
    # primera posicion donde fue hallado, en caso contrario retorna -1 
		dim = 5
		for i in range(dim):
		    row = self.env[i]
		    for j in range(dim):
		        col = row[j]
		        if col == 0:
		            return (i, j)

		return (-1, -1)

	def start_iterative_search(self):
		pass



	def start_iterarive_step(self):
		pass
