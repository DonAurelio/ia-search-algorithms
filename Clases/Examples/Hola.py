class Hola:
	hola = 0
	def __init__(self):
		self.l = Hola.hola + 1
		Hola.hola = Hola.hola + 1


if __name__ == '__main__':
	h = Hola()
	a = Hola()
	c = Hola()
	print(h.l)
	print(a.l)
	print(c.l)