import networkx as nt 
import matplotlib.pyplot as plt

#path to the graph
graphFileLocation = 'wordnet/LondonGeonamesTaxonomy.csv'
outputGraphLocation = 'wordnet/LondonGeonamesTaxTrans.csv'
#open the graph
Data = open(graphFileLocation, "r")

#set the graph type to directed graph
GraphType = nt.DiGraph()

#parse the edgelist from the origal data
G = nt.parse_edgelist(Data, delimiter = ',', create_using = GraphType, nodetype = str, data = (('weight', int),))

#pass it into the trastie closure function
G2 = nt.transitive_closure(G)
#write it to a new file
nt.write_edgelist(G2, outputGraphLocation, comments = '#', delimiter = ',', data = ['id1','id2','weight'])
