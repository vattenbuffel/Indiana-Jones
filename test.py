import networkx as nx

G = nx.Graph()
G.add_node((0,0))
G.add_node((1,0))
G.add_node((0,1))
G.add_edge((0,0), (1,0))
G.add_edge((0,0), (0,1))



# test = nx.bfs_tree(G, source=(0,0))
path = nx.dijkstra_path(G, (0,0), (0,1))
bajs = 5