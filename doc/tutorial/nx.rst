Using NetworkX functions
========================

`NetworkX <https://networkx.github.io/>`_ is an excellent tool for network analysis and there is no need to reinvent the wheel when working on monoplex networks with Pymnet. If you have NetworkX installed you can use its functions directly with the multilayer network objects produced with Pymnet. 

Start by importing the library:

>>> from pymnet import *

You can then run any NetworkX function from the pymnet.nx module. For example, you can produce the Karate Club network with the following command.

>>> net=nx.karate_club_graph()

This will produce native Pymnet multilayer network object with 0 aspects (i.e., a monoplex network). To confirm this, try:

>>> print net
<pymnet.net.MultilayerNetwork at 0x7f5b550eaa10>

You can also give Pymnet objects as arguments for NetworkX functions in similar way. This is handy for example when analysing monoplex structures of intra-layer networks of multiplex networks. For example, producing a multiplex network with 3 Erdos-Renyi intra-layer networks using Pymnet and calculating the number of connected components in each layer can be done with the following command:

>>> print map(nx.number_connected_components,models.er(1000,3*[0.005]).A.values())
[9, 11, 8]
