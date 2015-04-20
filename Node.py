class Node:

	def __init__(self,state,parent,action,cost,depth):
		self.state = state 
		self.parent = parent
		self.action = action
		self.cost = cost 
		self.depth  = depth

	def apply_action(self,action):
		pass

	def is_goal(self, env):
		pass

	def get_state(self):
		return self.state

	def __str__(self):
		return "("+ str(self.state[0]) + "," + str(self.state[1]) + ")"