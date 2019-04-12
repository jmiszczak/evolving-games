import numpy as np
import matplotlib.pyplot as plt

dim1 = 20
dim2 = 20

payoffs = np.load("results/grid_payoffs.npz")
strategies = np.load("results/grid_strategies.npz")

for i in range(len(payoffs['g1'])):
   plt.cla()
   plt.imshow(payoffs['g1'][i])
   plt.savefig("plots/grid-g1-payoffs_" + str(i).zfill(4) + ".png")

for i in range(len(strategies['g1'])):
   plt.cla()
   plt.imshow(strategies['g1'][i])
   plt.savefig("plots/grid-g1-strategies_" + str(i).zfill(4) + ".png")

#   print(payoffs['g1'][i])

#vals1 = np.zeros([dim1, dim2])

# for n in g1.nodes:
#     print(g1.nodes[n]['s'])

#fig = plt.figure()
#ax = fig.add_subplot(1,1,1)
#ax.set_aspect('equal')
#plt.imshow(vals1)
#plt.colorbar()
#plt.show()