Network types
=============


Monoplex networks
-----------------

Start by importing the library:

>>> from pymnet import *

MultilayerNetwork is the basic network class in the library -- all other types of networks are special case of it. In order to get a monoplex network object
you can simply construct a MultilayerNetwork with 0 aspects.

>>> net = MultilayerNetwork(aspects=0)

You can now start adding nodes to the network with the 'add_node' method:

>>> net.add_node(1)
>>> net.add_node(2)

Iterating the network object will yield all the nodes.

>>> list(net)
[1, 2]

You can access node objects of the network with the get syntax. The node objects can be used for example to get the degree or strength of the node.

>>> net[1].deg()
0

You can now start adding edges to your network. There are two basic ways of doing this. First is the syntax which resembles setting elements in an adjacency matrix:

>>> net[1,2] = 1

In the second way, you first access a node object and then get the edge pointing to a neighbor of that node:

>>> net[1][2] = 1

These to ways are equivalent, but the difference will become important when we move on to networks which are not monoplex ones. You can also add edges between nodes that you have not explicitly created, and in this case the missing nodes are created automatically:

>>> net[1,3] = 1
>>> list(net)
[1, 2, 3]

You can use similar syntax to check if the edges exist and access their weights. The default weight value for non-existing edge is 0.

>>> net[1,2]
1
>>> net[1][3]
1
>>> net[2,3]
0

The network is undirected by default which means that adding an edge in one direction adds it automatically to both directions.

>>> net[2,1]
1

The node objects can be iterated, which will yield the list of neighbors of the node:

>>> list(net[1])
[2, 3]

The edges can be removed by simply setting their value to 0:

>>> net[1,3] = 0
>>> list(net[1])
[2]

The edges of the networks can also be weighted with arbitrary numbers (except with the one corresponding to a missing edge). In the weighted networks
the degree and the weighted degree, i.e. strength, of a node are different:

>>> net[1,3] = 2
>>> net[1].deg()
2
>>> net[1].str()
3

By default, all the network objects are undirected. The directed network objects can be accessed by giving a keyword parameter 'directed' to True in the constructor
of the network object:

>>> dirnet = MultilayerNetwork(aspects=0,directed=True)
>>> dirnet[1,2]=1
>>> dirnet[1,2]
1
>>> dirnet[2,1]
0
>>> net[2,1]
1


Multilayer networks
-------------------

We are now ready to move to more general multilayer networks with arbitrary number of aspects. For simplicity, we will start with a network with a single aspect.

>>> mnet = MultilayerNetwork(aspects=1)

In these type of networks are similar to the monoplex ones, but now you have layers in addition of nodes. You can add new layers with the 'add_layer' method:

>>> mnet.add_node(1)
>>> mnet.add_layer('a')

Now, the node objects of the network need to be accessed by giving both the node and the layer:

>>> mnet[1,'a'].deg()
0

Again, the edges can be accessed in two ways. First one is similar to the tensor notation where the indices of nodes and layers are grouped together. The following command
will add an edge between node 1 in layer 'a' to node 2 in layer 'b' (again, the nodes and layers are implicitly created):

>>> mnet[1,2,'a','b'] = 1

In the syntax where you first access a node object and then it's neighbor the order of the indices is different. In this syntax the following command is equivalent to the one shown above:

>>> mnet[1,'a'][2,'b'] = 1

You can again iterate over a node object, but this time tuples with both node and layer are returned. Note that iterating over the network still returns only the nodes.

>>> list(mnet[1,'a'])
[(2, 'b')]
>>> list(mnet)
[1, 2]

You can create networks with arbitrary number of aspects. The syntax for this type of networks is straight forward extension of the one described above.

>>> mnet2 = MultilayerNetwork(aspects=2)
>>> mnet2[1,2,'a','b','x','y']=1
>>> mnet2[1,'a','x'][2,'b','y']
1

Sometimes new syntax is needed. For example, the aspect must be specified when adding layers.

>>> mnet2.add_layer('c',1)
>>> mnet2.add_layer('z',2)

.. more aspects
.. next: Slicing notation


Multiplex networks
------------------

The multilayer networks can in theory be used to represented multiplex networks, but in practise it is often better to use a specialized class MultiplexNetwork to 
when dealing with multiplex networks. There few reason for this. First, the MultiplexNetwork class offers an additional convenient interface for handling intra-layer networks.
Second, the MultiplexNetwork class can take coupling rules as an input when it's constructed and use them to implicitly create the inter-layer edges when they are needed. This
saves some memory and makes it easier to create networks with such coupling structures. Third, this will let the functions in the library to know that your multilayer network is
a multiplex network. Some of the functions only work for multiplex networks, but even the ones that work for general multilayer networks can use the information to speed up the
processing. 

The simplest multiplex network is the one with no coupling edges. You would create such object with the following command:

>>> mplex = MultiplexNetwork(couplings="none")

The nodes and edges can be accessed and added as usual:

>>> mplex[1,'a'][2,'a']=1

The difference to the MultilayerNetwork object (in addition to not being able to add cross-layer links) is that you can now access the intra-layer networks as follows:

>>> mplex.A['a'][1,2]
1
>>> mplex.A['a'][1,3] = 1

You can construct MultiplexNetworks with given coupling rules and have categorical or ordinal multiplex networks, where the inter-layer edges are filled in automatically.
In categorical networks all the diagonal inter-layer edges are present.

>>> cnet = MultiplexNetwork(couplings='categorical')
>>> cnet.add_node(1)
>>> cnet.add_layer('a')
>>> cnet.add_layer('b')
>>> cnet[1,1,'a','b']
1

In ordinal networks only adjacent layers are connected to each other. In MultiplexNetwork object the layer in ordinal aspect must be integers.

>>> onet = MultiplexNetwork(couplings='ordinal')
>>> onet.add_node('node')
>>> onet.add_layer(1)
>>> onet.add_layer(2)
>>> onet.add_layer(3)
>>> onet['node','node',1,2]
1
>>> onet['node','node',1,3]
0

You can also give the coupling strength, i.e. the weight of the inter-layer edges as a parameter

>>> cnet = MultiplexNetwork(couplings=('categorical',10))
>>> cnet.add_node(1)
>>> cnet.add_layer('a')
>>> cnet.add_layer('b')
>>> cnet[1,1,'a','b']
10

Multiplex networks with multiple aspects can be constructed by a list of coupling rules as the coupling parameter in the constructor. For example,
the following code constructs a multiplex network where the first aspect is categorical and the second is ordinal

>>> conet = MultiplexNetwork(couplings=['categorical','ordinal'])
>>> conet.add_node('node')
>>> conet.add_layer('a',1)
>>> conet.add_layer('b',1)
>>> conet.add_layer(1,2)
>>> conet.add_layer(2,2)
>>> conet.add_layer(3,3)
>>> conet['node','node','a','a',1,2]
1

In this case the intra-layer network must be accessed by giving a combination of layers.

>>> conet.A[('a',1)]['node','node2']=1

