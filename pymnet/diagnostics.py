from .net import MultilayerNetwork,MultiplexNetwork
from .transforms import subnet,aggregate,threshold
import heapq,itertools

def degs(net,degstype="distribution"):
    """Returns the degree distribution of a multilayer network.

    If the network has more than 1 aspect the degree distribution is returned for
    node-layer tuples.

    Parameters
    ----------
    net : MultilayerNetwork
       A multilayer network object.

    degstype : string
       If 'distribution', then degs dicts give the degree distributions. I.e.,
       keys are degrees, and corresponding values are number of nodes with the given degree.
       If 'nodes', then degs dicts give node degrees. I.e, keys are node names and
       corresponding values are degrees of those nodes.

    """
    if net.aspects==0:
        the_iterator=net
    else:
        the_iterator=net.iter_node_layers()
    degs={}
    if degstype=="distribution":
        for node in the_iterator:
            d=net[node].deg()
            degs[d]=degs.get(d,0)+1
    elif degstype=="nodes":
        for node in the_iterator:
            degs[node]=net[node].deg()
    else:
        raise Exception("Invalid degstype parameter.")
    return degs

def density(net):
    """Returns the density of the network.

    Density is defined as the number of edges in the network divided by the number
    of possible edges in a general multilayer network with the same set of nodes and
    layers.
    """
    if len(net)==0:
        return 0

    if net.fullyInterconnected:        
        nl=len(net.get_layers(0))
        for a in range(net.aspects):
            nl=nl*len(net.get_layers(a+1))
        if net.directed:
            pedges=nl*(nl-1)
        else:
            pedges=(nl*(nl-1))/2
            
    return len(net.edges)/float(pedges)


def multiplex_density(net):
    """Returns a dictionary of densities of each intra-layer network of a multiplex network.
    """
    assert isinstance(net,MultiplexNetwork)
    d={}
    for layer in net.iter_layers():
        d[layer]=density(net.A[layer])
    return d

def multiplex_degs(net,degstype="distribution"):
    """Returns a dictionary of degree distributions of each intra-layer network of a multiplex network.
    
    Parameters
    ----------
    net : MultiplexNetwork
       A multiplex network object.

    degstype : string
       If 'distribution', then degs dicts give the degree distributions. I.e.,
       keys are degrees, and corresponding values are number of nodes with the given degree.
       If 'nodes', then degs dicts give node degrees. I.e, keys are node names and
       corresponding values are degrees of those nodes.

    """
    assert isinstance(net,MultiplexNetwork)
    
    d={}
    for layer in net.iter_layers():
        d[layer]=degs(net.A[layer],degstype=degstype)
    return d

def overlap_degs(net):
    """ Returns a dictionary of overlap degree distributions of each layer combination
    of an unweighted multiplex network.

    The overlap degree distribution will contain every layer combination, including the
    one where there is only a single layer, and the key of each of those is another
    dictionary giving the overlap degrees of nodes.

    The overlap degrees of nodes for a given layer combination give the number of links that
    are shared between exactly the layers in the combination. If the link is in an additional
    layer, or it is missing from one layer, then it is not included in the degree of the
    corresponding layer combination.
    
    Parameters
    ----------
    net : MultiplexNetwork
       An unweighted multiplex network object (i.e. edge weigths equal to 1).
    """
    ol_degs = {}
    nodes = net.slices[0]
    layers = net.slices[1]
    
    net0 = subnet(net, nodes, layers)
    
    for n_l in range(len(layers), 0, -1):
        for layer_comb in itertools.combinations(layers, n_l):
            sub_net = subnet(net0, nodes, layer_comb)
            agg_net = aggregate(sub_net, 1)
            thr_net = threshold(agg_net, n_l)
            ol_degs[layer_comb] = degs(thr_net, degstype='nodes')
            
            if n_l > 1:
                for e in thr_net.edges:
                    for layer in layer_comb:
                        net0[e[0], e[1], layer] = 0
                        
    return ol_degs
    

def dijkstra(net,sources):
    """Return the forest giving shortest paths from a set of source nodes.

    Parameters
    ----------
    net : MultilayerNetwork
    sources : iterable
    """
    forest=MultilayerNetwork(aspects=net.aspects,
                             fullyInterconnected=False,
                             directed=True,
                             noEdge=-1)
    d=dict([(s,0) for s in sources])

    queue=[]
    for s in sources:
        heapq.heappush(queue,(0,s,s)) #distance, source, dest
    
    while len(queue)>0:
        dist,source,dest=heapq.heappop(queue)
        if d[dest]>=dist: #could be ==
            assert d[dest]==dist, " ".join(map(str,[dist,source,dest,d[dest]]))
            forest[source][dest]=net[source][dest]
            for neigh in net[dest].iter_out():
                ndist=dist+net[dest][neigh]
                if neigh not in d or d[neigh]>=ndist:
                    d[neigh]=ndist      
                    heapq.heappush(queue,(ndist,dest,neigh))


    return d,forest

def dijkstra_mlayer_prune(net,sources,aaspects):
    nsources=[]
    for s in sources:    
        layers=[]
        for a in range(net.aspects+1):
            if a in aaspects:
                assert s[a]==None
                layers.append(list(net.slices[a]))                
            else:
                layers.append([s[a]])
        for nl in itertools.product(*layers):
            if net[nl].deg()>0:
                nsources.append(nl)
                
    d,forest=dijkstra(net,nsources)

    def select_aspects(nl,aaspects):
        nnl=[]
        for a in range(len(nl)):
            if a not in aaspects:
                nnl.append(nl[a])
        return tuple(nnl)

    nd={}
    #for nl,dist in d.iteritems():
    for nl in d:
        dist=d[nl]
        nnl=select_aspects(nl,aaspects)
        if nnl not in nd or nd[nnl]>dist:
            nd[nnl]=dist


    def build_path(otree,ntree,node):
        for neigh in otree[node].iter_in():
            ntree[neigh][node]=otree[neigh][node]
            if ntree[neigh].deg_in()==0:
                build_path(otree,ntree,neigh)

    nforest=MultilayerNetwork(aspects=net.aspects,
                             fullyInterconnected=False,
                             directed=True,
                             noEdge=-1)

    #for nl,dist in d.iteritems():
    for nl in d:
        dist=d[nl]
        nnl=select_aspects(nl,aaspects)
        if nd[nnl]==d[nl]:
            build_path(forest,nforest,nl)

                        
    return nd,nforest


