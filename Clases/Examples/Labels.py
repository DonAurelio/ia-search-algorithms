import networkx as nx


G=nx.path_graph(3)
G.add_node(0,{'state':'Hola'})
print(nx.number_of_nodes(G))
print(nx.nodes(G))
pos=nx.spring_layout(G)

nx.draw(G,pos)



import matplotlib.pyplot as plt

for i in range(nx.number_of_nodes(G)):
	x,y=pos[i]
	plt.text(x,y+0.1,s='some text', bbox=dict(facecolor='red', alpha=0.5),horizontalalignment='center')
plt.show()
