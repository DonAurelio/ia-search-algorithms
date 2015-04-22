import networkx as nx
import matplotlib.pyplot as plt


G = nx.DiGraph()

#G.add_node("ROOT")

#for i in xrange(5):
	#G.add_node("Child_%i" % i)
	#G.add_node("Grandchild_%i" % i)
	#G.add_node("Greatgrandchild_%i" % i)

	#G.add_edge("ROOT", "Child_%i" % i)
	#G.add_edge("Child_%i" % i, "Grandchild_%i" % i)
	#G.add_edge("Grandchild_%i" % i, "Greatgrandchild_%i" % i)

#G.add_node((1,2))
G.add_node(1)
G.add_node(2)
G.add_edge(1,2)
G.add_node(3)
G.add_edge(1,3)
G.add_node(4)
G.add_edge(3,4)
G.add_node(5)
G.add_edge(3,5)

# write dot file to use with graphviz
# run "dot -Tpng test.dot >test.png"
nx.write_dot(G,'test.dot')

# same layout using matplotlib with no labels
plt.title("draw_networkx")
pos=nx.graphviz_layout(G,prog='dot')
nx.draw(G,pos,with_labels=False,arrows=False)
plt.show()
#plt.savefig('nx_test.png')
