from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"
DATASET_URL = "https://snap.stanford.edu/data/Florida-bay.txt.gz"
DATASET_METADATA_URL = "https://snap.stanford.edu/data/Florida-bay-meta.csv.gz"
DATASET_PATH = DATA_DIR / "dataset.txt.gz"
DATASET_METADATA_PATH = DATA_DIR / "dataset-meta.csv.gz"
RANDOM_SEED = 42
