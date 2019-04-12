import numpy as np
import matplotlib.pyplot as plt

dim1 = 20
dim2 = 20

strategies = np.load("results/grid_strategies.npz")

fc = list()

for i in range(len(strategies['g1'])):
    fc.append(np.mean(strategies['g1'][i]))

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.plot(fc)
plt.show()