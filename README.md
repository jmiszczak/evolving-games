# evolving-games

Collection of scripts implementing models from papers on evolutionary game theory.

Code in Python is organized in three directories:
- `games` includes implementation of some games used as the model of dynamics, eg. Prisoner's dillema,
- `models` contains implementation of various models,
- `varia` contains some scripts related to network properties.

NetLogo models are in `netlogo` directory.


# Requirements

## For running Python simulations
Graphs are implemented using [NetworkX](http://networkx.github.io/). [Numpy](https://www.numpy.org/) and [Matplotlib](https://matplotlib.org/) are also required.

Agent based models in python are implemented using [Mesa](https://github.com/projectmesa).

## For running NetLogo
NetLogo is a multi-agent programmable modeling environment. It can be obtained from <a href="http://ccl.northwestern.edu/netlogo/">NetLogo hompepage</a>. Models can be also run via <a href="http://www.netlogoweb.org/">NetLogo Web</a>.

# Relevant papers

Models implemented in this repo were described in the following papers.

- K. Sznajd-Weron, J. Sznajd, *Opinion evolution in closed community*, Int. J. Mod. Phys. C, Vol.11, No.6(2000) 1157-1165, DOI: <a href='https://doi.org/10.1142/S0129183100000936'>10.1142/S0129183100000936</a>, arXiv:[cond-mat/0101130v2](https://arxiv.org/abs/cond-mat/0101130)

- J. Wu, C. Zhao, *Cooperation on the Monte Carlo Rule: Prisoner’s Dilemma Game on the Grid*. In: Sun X., He K., Chen X. (eds) Theoretical Computer Science. NCTCS 2019. Communications in Computer and Information Science, vol 1069. Springer, Singapore. <a href="https://doi.org/10.1007/978-981-15-0105-0_1">10.1007/978-981-15-0105-0_1</a>, arXiv:<a href="https://arxiv.org/abs/1904.06949">1904.06949</a>
