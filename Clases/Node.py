
#Represent a node witch kept a state of search problem
class Node:

	#Number that identify a node (static clas variable)
	serial = 0

	def __init__(self,state,parent,action,cost,depth,heuristic=None):
		self.number = Node.serial + 1
		Node.serial = Node.serial + 1
		#Componets for a common node 
		self.state = state 
		self.parent = parent
		self.action = action
		self.cost = cost 
		self.depth  = depth
		#Extracomponest including heuristic h(n)
		#and total cost g(n) = h(n) + cost(n)
		if heuristic == None:
			self.heuristic = None
			self.total_cost = None
		else:
			self.total_cost = heuristic + self.cost

	def __str__(self):
		if self.heuristic == None:
			return "("+ str(self.state[0]) + "," + str(self.state[1]) + ")("+ str(self.cost) + ")"
		else:
			return "("+ str(self.state[0]) + "," + str(self.state[1]) + ")("+ str(self.total_cost) + ")"

	