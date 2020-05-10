
import torch, numpy as np
import itertools 
import math
import networkx as nt
import time 
from tqdm import tqdm
import random

#function to caclualte the hyperbolic distane between 2 elements in an embedding
#takes 2 elements as input and produces the hyperbolic distance as output based on the formula in our paper
def hyperbolicDistance(x, y):
	topLine = np.linalg.norm(x-y)**2
	bottomLine = (1-np.linalg.norm(x)**2)*(1-np.linalg.norm(y)**2)
	return np.arccosh(1+2*(topLine/bottomLine))

#returns a numpy array of eery possible pair of elements in the ontology, each element in the array
#is of size 2
#takes an array as input
def combinations(array = [], *args):
	return np.array(list(itertools.combinations(array,2)))

#returns the shortest path between 2 elements of a graph
#takes a graph and 2 of its elements as input
def shortestPath(G, a, b):
	return nt.shortest_path_length(G,a,b)


contribution = 0
sum_up = 0
graph_diameter = 0
max_hyperbolic_distance = 0
scaling_factor = 0
#path to the embedding 
EmbeddingFileName = 'LondonEmbeddings/tax/dim10/LondonGeonamesTaxTransDim10.pth.best'
#path to the ontology
OntologyFileName = 'wordnet/LondonGeonamesTaxTrans.csv'
size_of_sample = 0

#loads the embedding file and creates a numpy array of its elements
chkpnt = torch.load('EmbeddingFileName')
embeddings = chkpnt['embeddings']
objects = np.array(chkpnt['objects'])

#loads in the graph from the graph file
Data = open('OntologyFileName', 'r')
GraphType = nt.Graph()
G = nt.parse_edgelist(Data, delimiter = ',', create_using = GraphType, nodetype = str, data = (('weight', int),))
#calculates the diameter of the graph
graph_diameter = nt.diameter(G)

#generates all possible pairs of objects from the embedding
allPairs = combinations(objects)

#randomly selects the specified number of elements from the list of all possible pairs of elements with no replication

list_of_sample = random.sample(list(allPairs), size_of_sample)

#tqdm to proide a progress bar
for i in tqdm(list_of_sample):
	#calculate the shortest path
	shortest_path = shortestPath(G, i[0], i[1])

	#get the index of the first element in the pair
	idx = np.where(objects == i[0])[0]
	#get the index of the second element in the pair
	idy = np.where(objects == i[1])[0]
	#ge the vector assosiated with the element at index idx
	vectorX = embeddings[idx]
	#get the ector assosiated with the element at index idy
	vectorY = embeddings[idy]
	#calculate the hyperbolic distnace bewtween vector X and Y
	hyperbolic_distance = hyperbolicDistance(vectorX, vectorY)
	#check to see if its the maximum hyperbolic distance encountered so far
	max_hyperbolic_distance = max(max_hyperbolic_distance,hyperbolic_distance)

	contribution = (abs(shortest_path-hyperbolic_distance)/shortest_path)
	sum_up = sum_up + contribution
	contribution = 0
	shortest_path = 0
	hyperbolic_distance = 0

#scaling factor is the greates shortest path which is the diameter of the graph diided by max hyperbolic distance oer all pairs 
scaling_factor = graph_diameter/max_hyperbolic_distance
print("Scaling factor = ", scaling_factor)
#calculates distortion before the scaling factor is applied
no_scaling = sum_up/len(list_of_sample)	
print("distorion without scaling = ", no_scaling)
#applies scaling factor to calculate the actual distortion
distorion = no_scaling*scaling_factor
print("Distortion = ", distorion)

