# Directed Network Analysis

This project analyzes a directed ecological network. Each node represents a food-web compartment, and an edge from node `i` to node `j` means carbon flows from `i` to `j` (typically because `j` consumes `i`). The edge list is binary and unweighted: it does not report the amount of carbon exchanged.

The supplied [SNAP Florida Bay food-web data](https://snap.stanford.edu/data/Florida-bay.html) describe one ecosystem. Node metadata includes names and group labels; some compartments do not have a group label. The data also include special compartments such as input, output, and respiration, so high centrality should not automatically be interpreted as ecological importance of a species. The network source is Ulanowicz, Bondavalli, and Egnotovich (1997); the group labels are attributed by SNAP to ATLSS and Benson, Gleich, and Leskovec (2016).

## Run

From the project root:

```bash
python -m pip install -r requirements.txt
PYTHONPATH=src python src/main.py
```

The loader uses `data/dataset.txt.gz` and `data/dataset-meta.csv.gz`, downloading either file from SNAP when it is missing.

## Analysis

- Direction-aware counts and degrees, reciprocity, directed clustering, weak/strong components, and shortest paths within the largest strongly connected component.
- In-degree, out-degree, directed betweenness, outward closeness, and PageRank rankings.
- Mean in/out degree by available node group.
- ER, Watts--Strogatz, and Barabasi--Albert reference comparisons on the **undirected projection**. These comparisons do not preserve edge direction.

## Source modules

- `src/network_analysis/data.py`: read the edge list and node metadata
- `src/network_analysis/graph.py`: construct the labeled directed graph
- `src/network_analysis/metrics.py`: network measures, group summaries, and reference models
- `src/network_analysis/centrality.py`: directed node rankings
- `src/network_analysis/plots.py`: analysis figures
- `src/main.py`: analysis entry point

## Outputs

- `results/csv/summary_metrics.csv`
- `results/csv/model_comparison.csv`
- `results/csv/centrality_table.csv`
- `results/csv/group_summary.csv`
- `results/img/degree_distribution.png`
- `results/img/model_comparison.png`
- `report/main.tex` and `report/main.pdf`
