import networkx as nx
import pandas as pd


def build_network(edges: pd.DataFrame, nodes: pd.DataFrame) -> nx.DiGraph:
    """
    Build a directed graph and attach labels from the node metadata.
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
    Return a copy of the largest weakly connected component.
    """
    if graph.number_of_nodes() == 0:
        raise ValueError("Graph is empty.")
    component = max(nx.weakly_connected_components(graph), key=len)
    return graph.subgraph(component).copy()


def largest_strong_component(graph: nx.DiGraph) -> nx.DiGraph:
    """
    Return a copy of the largest strongly connected component.
    """
    if graph.number_of_nodes() == 0:
        raise ValueError("Graph is empty.")
    component = max(nx.strongly_connected_components(graph), key=len)
    return graph.subgraph(component).copy()
