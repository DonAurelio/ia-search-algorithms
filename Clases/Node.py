class Node:

	#Number that identify a node
	serial = 0

	def __init__(self,state,parent,action,cost,depth):
		self.number = Node.serial + 1
		Node.serial = Node.serial + 1
		self.state = state 
		self.parent = parent
		self.action = action
		self.cost = cost 
		self.depth  = depth

	def get_state(self):
		return self.state

	def get_cost(self):
		return self.cost
	
	def is_goal(self, env):
		pass

	def __str__(self):
		return "("+ str(self.state[0]) + "," + str(self.state[1]) + ")("+ str(self.cost) + ")"

	def __unicode__(self):
		return "("+ str(self.state[0]) + "," + str(self.state[1]) + ")"
