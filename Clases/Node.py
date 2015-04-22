
#Represent a node witch kept a state of search problem
class Node:

	#Number that identify a node (static clas variable)
	serial = 0

	def __init__(self,state,parent,action,cost,depth,heuristic=0):
		self.number = Node.serial + 1
		Node.serial = Node.serial + 1
		#Componets for a common node 
		self.state = state 
		self.parent = parent
		self.action = action
		self.cost = cost 
		self.depth  = depth
		#Extracomponest inscluding heuristic h(n)
		#and total cost g(n) = h(n) + cost(n)
		self.heuristic = heuristic
		self.tota_cost = heuristic + self.cost


	def __str__(self):
		return "("+ str(self.state[0]) + "," + str(self.state[1]) + ")("+ str(self.cost) + ")"

	def __unicode__(self):
		return "("+ str(self.state[0]) + "," + str(self.state[1]) + ")"
