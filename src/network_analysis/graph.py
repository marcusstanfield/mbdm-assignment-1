import networkx as nx
import pandas as pd


def build_network(edges: pd.DataFrame, nodes: pd.DataFrame) -> nx.DiGraph:
    """
    Builds a directed graph and attaches labels from the node metadata.

    Parameters
    ----------
    edges : pandas.DataFrame
        The directed edges, with ``source`` and ``target`` columns.
    nodes : pandas.DataFrame
        The node metadata, with ``node_id``, ``name``, and ``group`` columns.

    Returns
    -------
    networkx.DiGraph
        The directed graph with node metadata attached.
    """
    if edges.duplicated(["source", "target"]).any():
        raise ValueError("Dataset contains duplicate directed edges.")
    if (edges["source"] == edges["target"]).any():
        raise ValueError("Dataset contains self-loops.")

    node_ids = set(nodes["node_id"])
    edge_node_ids = set(edges["source"]) | set(edges["target"])
    missing_metadata = edge_node_ids - node_ids
    if missing_metadata:
        raise ValueError(
            f"Dataset is missing metadata for node IDs: {sorted(missing_metadata)}"
        )
    if nodes["node_id"].duplicated().any():
        raise ValueError("Dataset metadata contains duplicate node IDs.")

    graph = nx.from_pandas_edgelist(
        edges,
        source="source",
        target="target",
        create_using=nx.DiGraph,
    )
    metadata = nodes.set_index("node_id")[["name", "group"]].to_dict("index")
    for attributes in metadata.values():
        if pd.isna(attributes["group"]):
            attributes["group"] = None
    graph.add_nodes_from((node_id, attributes) for node_id, attributes in metadata.items())
    return graph


def largest_weak_component(graph: nx.DiGraph) -> nx.DiGraph:
    """
    Returns a copy of the largest weakly connected component.

    Parameters
    ----------
    graph : networkx.DiGraph
        A directed graph.

    Returns
    -------
    networkx.DiGraph
        A copy of the largest weakly connected component.
    """
    if graph.number_of_nodes() == 0:
        raise ValueError("Graph is empty.")
    component = max(nx.weakly_connected_components(graph), key=len)
    return graph.subgraph(component).copy()


def largest_strong_component(graph: nx.DiGraph) -> nx.DiGraph:
    """
    Returns a copy of the largest strongly connected component.

    Parameters
    ----------
    graph : networkx.DiGraph
        A directed graph.

    Returns
    -------
    networkx.DiGraph
        A copy of the largest strongly connected component.
    """
    if graph.number_of_nodes() == 0:
        raise ValueError("Graph is empty.")
    component = max(nx.strongly_connected_components(graph), key=len)
    return graph.subgraph(component).copy()
