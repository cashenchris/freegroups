import networkx as nx
from networkx.classes.graph import Graph
from networkx import NetworkXException, NetworkXError
import networkx.convert as convert
from copy import deepcopy
import whiteheadgraph.build.orderedmultigraph as omg
import copy

g=omg.OrderedMultiGraph()
g.addEdge(1,2,'e')
g.addEdge(1,2,'f1')
g.addEdge(1,2,'f2')
g.addEdge(2,3,'g')
g.addVertex(4)
g.addEdge(2,3)
g.addEdge(2,3)
g.addEdge(2,3, 'h', 1, 1)
g.removeEdge('f1')

circle=omg.OrderedMultiGraph()
circle.addEdge(1,2,'e1')
circle.addEdge(2,3,'e2')
circle.addEdge(3,4,'e3')
circle.addEdge(4,1,'e4')

circle.isConnected()
circle.isCircle()

circle.findCutVertex()

h=omg.splice(g,circle,1,1,[0,1],('g',),('c',),lookforisolatedvertices=True)
k,foundfree=omg.selfsplice(circle,1,2,[0,1],lookforisolatedvertices=True,reportfreeedges=True)
