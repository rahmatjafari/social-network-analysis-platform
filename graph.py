import networkx as nx
import matplotlib.pyplot as plt

#Nodes represent the pages and edges are mutual likes among them.  ==> LikeNetwork.txt    delimiter=','
#Nodes represent the profiles and edges are friendship among them. ==> FriendNetwork.txt  delimiter=None

g = nx.read_edgelist('FriendNetwork.txt' , create_using = nx.Graph() , nodetype=int)

print (nx.info(g))

sp=nx.spring_layout(g)

plt.axis('off')
plt.axis('equal')
nx.draw_networkx(g,post=sp,with_labels=False,node_size=20)

plt.show()