# imports Whitehead garph stuff and sets up some basic examples.
import group
import freegroup 
import networkx as nx
import whiteheadgraph.build.orderedmultigraph as omg
import whiteheadgraph.build.wgraph as wg
import whiteheadgraph.split.split as split
import whiteheadgraph.draw.draw as wdraw
import AutF as aut
import graphofgroups as gog
import whiteheadgraph.build.whiteheadreduce as wreduce
from whiteheadgraph.test.knownexamples import *
import whiteheadgraph.split.partition as part
import whiteheadgraph.test.checkcutpair
import whiteheadgraph.test.rjsj

whiteheadgraph.test.checkcutpair.testall()
whiteheadgraph.test.rjsj.testall()
