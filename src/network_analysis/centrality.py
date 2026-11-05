import networkx as nx
import pandas as pd


def compute_centrality_table(graph: nx.DiGraph) -> pd.DataFrame:
    """
    Ranks nodes by directed degree, betweenness, outward closeness, and PageRank.

    Parameters
    ----------
    graph : networkx.DiGraph
        A directed graph with node metadata.

    Returns
    -------
    pandas.DataFrame
        The top 10 nodes for each centrality measure, with node IDs, names,
        groups, scores, and metric names.
    """
    measures: dict[str, dict[int, float]] = {
        "in_degree": dict(graph.in_degree()),
        "out_degree": dict(graph.out_degree()),
        "betweenness_centrality": nx.betweenness_centrality(graph),
        "out_closeness_centrality": nx.closeness_centrality(graph.reverse(copy=False)),
        "pagerank": nx.pagerank(graph),
    }
    rows = []
    for metric, scores in measures.items():
        for node, score in sorted(scores.items(), key=lambda item: item[1], reverse=True)[:10]:
            attributes = graph.nodes[node]
            rows.append(
                {
                    "node_id": node,
                    "name": attributes["name"],
                    "group": attributes.get("group"),
                    "score": float(score),
                    "metric": metric,
                }
            )
    return pd.DataFrame(rows)
