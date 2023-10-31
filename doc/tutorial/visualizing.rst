.. _visualization_tutorial:

Visualizing networks
====================

The Multilayer Network Library can produce high quality images of multilayer and multiplex networks. The main method of producing network images in the library uses Matplotlib as a backend. These images can be saved both in vector formats (such as pdf or svg) and raster formats (such as png). Alternatively, one can produce pictures of networks using a method that uses Javascript and D3 as a backend for displaying figures. These interactive figures can be viewed with any modern browser. (Also, NetworkX is used for some layouts).

Drawing networks with the library is easy and is usually done with the "draw" method. Consider, for example, the following code:

>>> from pymnet import *
>>> net = models.er_multilayer(5,2,0.2)
>>> fig = draw(net)

The first line of this code imports the multilayer network. The second line creates a random node-aligned multilayer network with 5 nodes and 2 layers with each node-layer tuple connected to each other with a probability of 0.2. The third line then creates a picture of that network. 

Note that running this code doesn't actually show the figure, but it's stored in the computers memory at this point. You can save the figure to a file, for example with the following command:

>>> fig.savefig("net.pdf")

Alternatively you can view the network straight away by telling the draw method that you want the figure to be shown:

>>> fig = draw(net,show=True)

The produced figure looks like this:

.. figure::  ermlayer1.png
   :align:   center

Multiplex network figures can also be produced. For example running the following code...

>>> fig=draw(er(10,3*[0.4]),layout="spring")

produces a following picture of multiplex ER network:

.. figure:: ermplex1.png
   :align:   center

There are multiple ways of customizing the figures. For documentation look at the reference for the draw method. Here is an example usage of the draw methods that uses several of the customization options:

>>> fig=draw(er(10,3*[0.3]),
             layout="circular",
             layershape="circle",
       	     nodeColorDict={(0,0):"r",(1,0):"r",(0,1):"r"},
             layerLabelRule={},
             nodeLabelRule={},
             nodeSizeRule={"rule":"degree","propscale":0.05})

produces a following figure:

.. figure:: ermplex2.png
   :align:   center

If the network is large, then it is often desirable not to plot the coupling edges. Simply create a network without coupling edges and plot it. For example, the `Bernard & Killworth fraternity network <http://vlado.fmf.uni-lj.si/pub/networks/data/ucinet/ucidata.htm#bkfrat>`_ might be plotted like this:

>>> net=read_ucinet("bkfrat.dat",couplings="none")
>>> net=transforms.threshold(net,4)
>>> fig=draw(net,
             show=True,
             layout="spring",
             layerColorRule={},
             defaultLayerColor="gray",
             nodeLabelRule={},
             edgeColorRule={"rule":"edgeweight","colormap":"jet","scaleby":0.1}
             )

Which then produces the following figure:

.. figure:: bkfrat.png
   :align:   center
