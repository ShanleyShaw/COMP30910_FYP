
#calucalates all the Euclidean norms of the embeddings and stores them in a file, also returns the lowest and aerage norms
import torch, numpy as np
import math

def norm(x):
	return np.linalg.norm(x)
	

#path to the embedding file
embeddingFileLocation = 'LondonEmbeddings/tax/dim10/LondonEmbeddingsTaxTrans.pth.best'
#load in the embedding file and store as a numpy array
chkpnt = torch.load(embeddingFileLocation)
embeddings = chkpnt['embeddings']
objects = np.array(chkpnt['objects'])
#create a list which will store all of the norms calculated
normList = []
#open a file which we will be writing too
normFileLocation = 'Norms/tax/normsDim10.txt'
f=open(normFileLocation, "w+")
#currvector stores the norm of the current vector 
currvector = 0

for i in objects:
	#get the index of element i
	idx = np.where(objects == i)[0]
	#get the vector assosiated with idx
	vector  = embeddings[idx]	
	#calculate the norm of the vector
	currvector = norm(vector)
	#writing to 16 decimal places in the format name : norm 
	f.write("%s : %.16f \n" %  (str(i), float(currvector))) 
	#add the norm to the list of norms
	normList.append(currvector)
	currvector = 0
	
#sort the list in ascending order
normList.sort()
d = sum(normList)/len(normList)
print("aerage : %.16f \n" % float(d))
#print the smallest norm to the console
print("lowest : %.16f" %float(normList[0]))
#close the file
f.close()