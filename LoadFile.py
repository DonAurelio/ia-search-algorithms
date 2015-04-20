class LoadFile:

	def __init__(self, file_name):
		self.file_name = file_name
		self.env = []
		self.dimension = 0

	def read(self):
		env_file = open(self.file_name)
		self.dimension = int(env_file.readline()) 

		# INICIALIZAR MATRIZ
		for i in range(self.dimension):
		    self.env.append([])
		    for j in range(self.dimension):
	       		self.env[i].append(0)

	    # CARGAR MATRIZ DEL FICHERO
		for i in range(self.dimension):
			line = env_file.readline()
			colums = line.split(" ")
			for j in range(self.dimension):
				self.env[i][j] = int(colums[j])

		return self.dimension , self.env



