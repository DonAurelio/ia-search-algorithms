import networkx as nx 
import matplotlib.pyplot as plt

graph = nx.Graph()
graph.add_node(1,{'title':"one",'age':23})
graph.add_node(2, {'title':"two",'age':11})
graph.add_edge(2,1)
#graph.add_nodes_from([2,3])
#graph.add_edge(1,2)
#graph.add_edges_from([(1,2),(1,3)])
#graph.clear()
#graph.add_node("spam")       # adds node "spam"
#graph.add_nodes_from("spam") # adds 4 nodes: 's', 'p', 'a', 'm'
graph.number_of_nodes()
graph.number_of_edges()
#G.nodes() #['a', 1, 2, 3, 'spam', 'm', 'p', 's']
#graph.neighbors(1) #[2, 3]
print graph.nodes(data=True)
graph.nodes(data=True)
nx.draw(graph,hold=True)
#nx.draw_networkx_labels(graph,pos=nx.spring_layout(graph))
#nx.draw_networkx_edge_labels(graph,pos=nx.spring_layout(graph))
#plt.savefig("path.png")
plt.show()
graph.add_node(1,{'title':"one",'age':2})