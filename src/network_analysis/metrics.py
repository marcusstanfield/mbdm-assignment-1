from typing import TypedDict

import networkx as nx
import numpy as np
import pandas as pd

from network_analysis.config import RANDOM_SEED
from network_analysis.graph import largest_strong_component, largest_weak_component


class NetworkSummary(TypedDict):
    nodes: int
    edges: int
    average_in_degree: float
    average_out_degree: float
    density: float
    reciprocity: float
    directed_clustering: float
    undirected_clustering: float
    largest_wcc_size: int
    largest_wcc_share: float
    largest_scc_size: int
    largest_scc_share: float
    average_path_length_scc: float
    diameter_scc: int


def describe_network(graph: nx.DiGraph) -> NetworkSummary:
    """
    Computes direction-aware measures and path metrics on the largest SCC.

    Parameters
    ----------
    graph : networkx.DiGraph
        A directed graph.

    Returns
    -------
    NetworkSummary
        Direction-aware network metrics and path metrics for the largest
        strongly connected component.
    """
    if graph.number_of_nodes() == 0:
        raise ValueError("Cannot compute metrics for an empty graph.")

    weak_component = largest_weak_component(graph)
    strong_component = largest_strong_component(graph)
    undirected_projection = graph.to_undirected()
    node_count = graph.number_of_nodes()

    return {
        "nodes": node_count,
        "edges": graph.number_of_edges(),
        "average_in_degree": float(np.mean([degree for _, degree in graph.in_degree()])),
        "average_out_degree": float(np.mean([degree for _, degree in graph.out_degree()])),
        "density": float(nx.density(graph)),
        "reciprocity": float(nx.reciprocity(graph)),
        "directed_clustering": float(nx.average_clustering(graph)),
        "undirected_clustering": float(nx.average_clustering(undirected_projection)),
        "largest_wcc_size": weak_component.number_of_nodes(),
        "largest_wcc_share": weak_component.number_of_nodes() / node_count,
        "largest_scc_size": strong_component.number_of_nodes(),
        "largest_scc_share": strong_component.number_of_nodes() / node_count,
        "average_path_length_scc": float(nx.average_shortest_path_length(strong_component)),
        "diameter_scc": int(nx.diameter(strong_component)),
    }


def build_model_networks(empirical: nx.Graph) -> dict[str, nx.Graph]:
    """
    Builds ER, WS, and BA reference graphs for an undirected projection.

    Parameters
    ----------
    empirical : networkx.Graph
        The undirected empirical network projection.

    Returns
    -------
    dict[str, networkx.Graph]
        The empirical projection and generated reference graphs.
    """
    node_count = empirical.number_of_nodes()
    if node_count < 3:
        raise ValueError("At least three nodes are required to generate benchmarks.")

    average_degree = float(np.mean([degree for _, degree in empirical.degree()]))
    ws_degree = min(node_count - 1, max(2, int(round(average_degree))))
    if ws_degree % 2:
        ws_degree = ws_degree - 1 if ws_degree == node_count - 1 else ws_degree + 1
    ba_edges_per_node = min(
        node_count - 1, max(1, int(round(average_degree / 2)))
    )
    return {
        "Empirical projection": empirical,
        "Erdos-Renyi": nx.erdos_renyi_graph(node_count, average_degree / (node_count - 1), seed=RANDOM_SEED),
        "Watts-Strogatz": nx.watts_strogatz_graph(node_count, k=ws_degree, p=0.05, seed=RANDOM_SEED),
        "Barabasi-Albert": nx.barabasi_albert_graph(node_count, m=ba_edges_per_node, seed=RANDOM_SEED),
    }


def compute_model_comparison(empirical: nx.Graph) -> pd.DataFrame:
    """
    Compares undirected structural baselines with the empirical projection.

    Parameters
    ----------
    empirical : networkx.Graph
        The undirected empirical network projection.

    Returns
    -------
    pandas.DataFrame
        Network metrics for the empirical projection and reference graphs.
    """
    rows = []
    for name, graph in build_model_networks(empirical).items():
        rows.append(
            {
                "Network": name,
                "Nodes": graph.number_of_nodes(),
                "Edges": graph.number_of_edges(),
                "AverageDegree": round(float(np.mean([degree for _, degree in graph.degree()])), 3),
                "Density": round(float(nx.density(graph)), 4),
                "AverageClustering": round(float(nx.average_clustering(graph)), 4),
                "AveragePathLength": round(float(nx.average_shortest_path_length(graph)), 3),
                "Diameter": nx.diameter(graph),
            }
        )
    return pd.DataFrame(rows)


def summarize_groups(graph: nx.DiGraph) -> pd.DataFrame:
    """
    Summarizes node count and mean in/out degree by available group label.

    Parameters
    ----------
    graph : networkx.DiGraph
        A directed graph with node group labels.

    Returns
    -------
    pandas.DataFrame
        Node counts and average in- and out-degree for each group.
    """
    rows = []
    for node in graph:
        attributes = graph.nodes[node]
        rows.append(
            {
                "group": attributes.get("group") or "Unclassified",
                "in_degree": graph.in_degree(node),
                "out_degree": graph.out_degree(node),
            }
        )
    return (
        pd.DataFrame(rows)
        .groupby("group", as_index=False)
        .agg(
            Nodes=("group", "size"),
            AverageInDegree=("in_degree", "mean"),
            AverageOutDegree=("out_degree", "mean"),
        )
        .sort_values(["Nodes", "group"], ascending=[False, True])
    )
