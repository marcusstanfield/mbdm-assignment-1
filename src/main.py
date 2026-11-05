import pandas as pd

from network_analysis.centrality import compute_centrality_table
from network_analysis.config import RESULTS_DIR
from network_analysis.data import load_dataset
from network_analysis.graph import build_network
from network_analysis.metrics import (
    compute_model_comparison,
    describe_network,
    summarize_groups,
)
from network_analysis.plots import (
    save_degree_distribution_plot,
    save_model_comparison_plot,
)


def main() -> None:
    csv_dir = RESULTS_DIR / "csv"
    image_dir = RESULTS_DIR / "img"
    RESULTS_DIR.mkdir(exist_ok=True)
    csv_dir.mkdir(exist_ok=True)
    image_dir.mkdir(exist_ok=True)

    edges, nodes = load_dataset()
    graph = build_network(edges, nodes)
    undirected_graph = graph.to_undirected()

    summary = describe_network(graph)
    comparison = compute_model_comparison(undirected_graph)
    centrality_table = compute_centrality_table(graph)
    group_summary = summarize_groups(graph)

    summary_columns = [
        "nodes",
        "edges",
        "average_in_degree",
        "average_out_degree",
        "density",
        "reciprocity",
        "directed_clustering",
        "undirected_clustering",
        "largest_wcc_size",
        "largest_wcc_share",
        "largest_scc_size",
        "largest_scc_share",
        "average_path_length_scc",
        "diameter_scc",
    ]
    summary_df = pd.DataFrame([{key: summary[key] for key in summary_columns}])
    summary_df.columns = [
        "Nodes",
        "Edges",
        "AverageInDegree",
        "AverageOutDegree",
        "Density",
        "Reciprocity",
        "DirectedClustering",
        "UndirectedClustering",
        "LargestWCCSize",
        "LargestWCCShare",
        "LargestSCCSize",
        "LargestSCCShare",
        "AveragePathLengthSCC",
        "DiameterSCC",
    ]
    summary_df.to_csv(csv_dir / "summary_metrics.csv", index=False)
    comparison.to_csv(csv_dir / "model_comparison.csv", index=False)
    centrality_table.to_csv(csv_dir / "centrality_table.csv", index=False)
    group_summary.to_csv(csv_dir / "group_summary.csv", index=False)

    save_degree_distribution_plot(graph, image_dir / "degree_distribution.png")
    save_model_comparison_plot(undirected_graph, image_dir / "model_comparison.png")

    print("Network analysis complete.")
    print(summary_df.to_string(index=False))
    print("\nTop ranking nodes by centrality:")
    print(centrality_table.head(15).to_string(index=False))
    print("\nGroup-level summary:")
    print(group_summary.to_string(index=False))


if __name__ == "__main__":
    main()
