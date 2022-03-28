
class EdgeType(Enum):
    """Enumeration of different causal edges.

    Categories
    ----------
    bidirected : str
        Signifies edge is part of a "<->" edge.
    arrow : str
        Signifies ">", or "<" edge. That is a normal
        directed edge.
    circle : str
        Signifies "o" endpoint. That is an uncertain edge,
        meaning it could be a tail, or an arrow.

    Notes
    -----
    The possible edges are:

    ->, <-, <->, o->, <-o, o-o
    """

    arrow = "arrow"
    circle = "circle"
    bidirected = "bidirected"


class CausalGraphicalModel(nx.MultiDiGraph):
    def __init__(self, incoming_graph_data=None, incoming_latent_data=None, **attr):
        """Initialize a causal graphical model.

        This is a Bayesian network, where now the edges represent
        causal influences. Self loops are not allowed. This graph type
        inherits functionality from networkx. As such, different edge
        types are enabled using the edge attribute 'type', enumerated
        by `EdgeType`.

        Parameters
        ----------
        incoming_graph_data : input graph (optional, default: None)
            Data to initialize directed acyclic graph. If None (default) an empty
            graph is created.  The data can be an edge list, or any
            NetworkX graph object.  If the corresponding optional Python
            packages are installed the data can also be a 2D NumPy array, a
            SciPy sparse matrix, or a PyGraphviz graph.

        incoming_latent_data : input bidrected edge list.
            Indicates which nodes are connected with a bidirected edge.

        attr : keyword arguments, optional (default= no attributes)
            Attributes to add to graph as key=value pairs.

        See Also
        --------
        networkx.MultiDiGraph

        Notes
        -----

        """
        super(CausalGraphicalModel, self).__init__(
            incoming_graph_data=incoming_graph_data, **attr
        )

        # check if there are any repeated edges
        for u in G.nodes():
            for neighbor in G.neighbors(u):
                if G.number_of_edges(u, neighbor) > 2:
                    print(u, neighbor)

        # label all existing edges as "arrow types"
        nx.set_edge_attributes(self, EdgeType.arrow, "type")

        # add bidirected edges
        for u_node, v_node in incoming_latent_data:
            self.add_bidirected_edge(u_node, v_node, type="bidirected")

    def add_bidirected_edge(self, u_for_edge, v_for_edge, **attr):
        """Add a bidirected edge between u and v.

        The nodes u and v will be automatically added if they are
        not already in the graph.

        Parameters
        ----------
        u_for_edge, v_for_edge : nodes
            Nodes can be, for example, strings or numbers.
            Nodes must be hashable (and not None) Python objects.
        attr : keyword arguments, optional
            Edge data (or labels or objects) can be assigned using
            keyword arguments.

        Returns
        -------
        The edge key assigned to the edge.

        See Also
        --------
        nx.MultiDiGraph.add_edges_from : add a collection of edges
        nx.MultiDiGraph.add_edge       : add an edge

        Notes
        -----
        ...
        """
        if "type" in attr:
            raise ValueError('"type" cannot be a key in edge data.')

        # add bidirected edge by adding a directed edge in both
        # directions, and labeling the "type" as "bidirected"
        key = 1
        self.add_edge(u_for_edge, v_for_edge, key=key, type=EdgeType.bidirected, **attr)
        self.add_edge(u_for_edge, v_for_edge, key=key, type=EdgeType.bidirected, **attr)
        return key

    def _get_c_components(self):
        pass

    def add_unobserved_common_cause(self, observed_node_names, color="gray"):
        # Adding unobserved confounders
        current_common_causes = self.get_common_causes(
            self.treatment_name, self.outcome_name
        )
        create_new_common_cause = True
        for node_name in current_common_causes:
            if self._graph.nodes[node_name]["observed"] == "no":
                create_new_common_cause = False
        if create_new_common_cause:
            uc_label = "Unobserved Confounders"
            self._graph.add_node(
                "U",
                label=uc_label,
                observed="no",
                color=color,
                style="filled",
                fillcolor=color,
            )
            for node in self.treatment_name + self.outcome_name:
                self._graph.add_edge("U", node)
            self.logger.info(
                'If this is observed data (not from a randomized experiment), there might always be missing confounders. Adding a node named "Unobserved Confounders" to reflect this.'
            )
        return self._graph

    def compute_mag(self) -> nx.DiGraph:
        """Compute the MAG corresponding to the causal DAG.

        The Maximal Ancestral Graph maintains all conditional
        independences associated with the causal DAG and in
        place of latent variables, has

        Returns
        -------
        nx.DiGraph
            _description_
        """
        adj_mat = nx.adjacency_matrix(self)

        # get the adjacency of the graph
        mag = nx.from_numpy_matrix(adj_mat)

        # loop over all nodes
        for node in mag.nodes:
            # then for each node, loop over the adjacent
            pass
