import urllib.request

import pandas as pd

from network_analysis.config import (
    DATASET_METADATA_PATH,
    DATASET_METADATA_URL,
    DATASET_PATH,
    DATASET_URL,
)


def load_dataset() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load the directed edge list and node metadata, downloading missing files.
    """
    for path, url in (
        (DATASET_PATH, DATASET_URL),
        (DATASET_METADATA_PATH, DATASET_METADATA_URL),
    ):
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            with urllib.request.urlopen(url, timeout=60) as response:
                path.write_bytes(response.read())

    edges = pd.read_csv(
        DATASET_PATH,
        sep=r"\s+",
        comment="#",
        names=["source", "target"],
    )
    nodes = pd.read_csv(DATASET_METADATA_PATH)
    required_edge_columns = {"source", "target"}
    required_node_columns = {"node_id", "name", "group"}
    if not required_edge_columns.issubset(edges.columns):
        raise ValueError("Dataset edge list must contain source and target columns.")
    if not required_node_columns.issubset(nodes.columns):
        raise ValueError("Dataset metadata must contain node_id, name, and group columns.")
    return edges, nodes
