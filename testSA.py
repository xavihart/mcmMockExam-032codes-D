from SAplanning import *
import numpy as np
import time
t = time.time()
test = np.random.random((100, 200000))


print(SA(test))
print(time.time() - t)