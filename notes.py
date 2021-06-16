from scipy.spatial.distance import cdist
import numpy as np
lis = [[1,2], [3,4], [5,6], [7,8]]

y= cdist(lis, lis, 'euclidean')
# print(y)
# for i in y:
#     print(i[0])
distances = set(y[np.triu_indices_from(y)])
distances.remove(0)
distances = list(distances)
print(distances[0])