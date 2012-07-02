import numpy as np
from numpy.random import random_integers as rnd
import matplotlib.pyplot as plt
 
def maze(width=81, height=51, complexity=.75, density =.75):
    # Only odd shapes
    shape = ((height//2)*2+1, (width//2)*2+1)
    # Adjust complexity and density relative to maze size
    complexity = int(complexity*(5*(shape[0]+shape[1])))
    density    = int(density*(shape[0]//2*shape[1]//2))
    # Build actual maze
    Z = np.zeros(shape, dtype=bool)
    # Fill borders
    Z[0,:] = Z[-1,:] = 1
    Z[:,0] = Z[:,-1] = 1
    for i in range(shape[0]):
        for j in range(shape[1]):
            a = lambda x: rnd(x)
            Z[i,j] = (a(3) == 1)
    return Z
 
plt.figure(figsize=(10,5))
plt.imshow(maze(80,40),cmap=plt.cm.binary,interpolation='nearest')
plt.xticks([]),plt.yticks([])
plt.show()