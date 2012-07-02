import numpy as np

myMap = np.zeros( (10,10) )

np.save( "emptyMap.txt", myMap )

print myMap