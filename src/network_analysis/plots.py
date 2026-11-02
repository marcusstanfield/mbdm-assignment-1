from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

from network_analysis.metrics import build_model_networks


def save_degree_distribution_plot(graph: nx.DiGraph, output_path: Path) -> None:
    figure, axis = plt.subplots(figsize=(8, 5))
    axis.hist(
        [degree for _, degree in graph.in_degree()],
        bins=20,
        alpha=0.65,
        label="In-degree",
    )
    axis.hist(
        [degree for _, degree in graph.out_degree()],
        bins=20,
        alpha=0.65,
        label="Out-degree",
    )
    axis.set_title("Directed degree distributions")
    axis.set_xlabel("Degree")
    axis.set_ylabel("Number of nodes")
    axis.legend()
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(output_path, dpi=200)
    plt.close(figure)


def save_model_comparison_plot(empirical: nx.Graph, output_path: Path) -> None:
    figure, axis = plt.subplots(figsize=(10, 6))
    for name, graph in build_model_networks(empirical).items():
        degrees = [degree for _, degree in graph.degree()]
        axis.hist(degrees, bins=20, alpha=0.4, label=name)
    axis.set_title("Undirected projection and reference-model degree distributions")
    axis.set_xlabel("Degree")
    axis.set_ylabel("Number of nodes")
    axis.legend()
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(output_path, dpi=200)
    plt.close(figure)
