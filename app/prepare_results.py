from pathlib import Path
from typing import Dict

import logging
import pickle
import plotly.express as px
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from itertools import product
from sklearn.manifold import TSNE
from umap import UMAP

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

TSNE_PARAMS = {
    "perplexity": [10, 30, 50],
    "n_iterations": [300, 500, 1000],
    "learning_rates": [2, 10, 50],
}
UMAP_PARAMS = {"n_neighbors": [2, 3, 5, 10], "min_dist": [0.1, 0.2, 0.5]}

DATA_DIR = Path(".")
TSNE_RESULTS_FILEPATH = DATA_DIR.joinpath("tsne_projection_results.pkl")
UMAP_RESULTS_FILEPATH = DATA_DIR.joinpath("umap_projection_results.pkl")

SEED = 0


@dataclass_json
@dataclass
class TSNEobj:
    perplexity: float
    num_iteration: int
    learning_rate: float
    n_components: int = 2

    def get_properties_str(self):
        return f"n_comp={self.n_components}__perp={self.perplexity}__n_iter={self.num_iteration}__learning_rate={self.learning_rate}"


@dataclass_json
@dataclass
class UMAPobj:
    n_neighbors: int
    min_dist: float = 0.1
    n_components: int = 2

    def get_properties_str(self):
        return f"n_comp={self.n_components}__n_neigh={self.n_neighbors}__min_dist={self.min_dist}"


tsne_model_params = list(
    product(
        TSNE_PARAMS["perplexity"],
        TSNE_PARAMS["n_iterations"],
        TSNE_PARAMS["learning_rates"],
    )
)
TSNE_MODELS = [
    TSNEobj(perplexity=perp, num_iteration=n_iter, learning_rate=eta)
    for perp, n_iter, eta in tsne_model_params
]

umap_model_params = list(product(UMAP_PARAMS["n_neighbors"], UMAP_PARAMS["min_dist"]))
UMAP_MODELS = [
    UMAPobj(n_neighbors=n_neigh, min_dist=dist) for n_neigh, dist in umap_model_params
]


def convert_param_str_to_dict(s: str) -> Dict[str, float]:
    """Convert parameters string to a dictionary
    Example:
        s = 'n_comp=2__perp=30.0__n_iter=100__learning_rate=200.0'

        Step 1: Split parameters by "__"
            >> ['n_comp=2', 'perp=30.0', 'n_iter=100', 'learning_rate=200.0']
        Step 2: Split by "="
            >> [ ['n_comp', '2'], ['perp', '30.0'], ['n_iter', '100'], ['learning_rate', '200.0'] ]
        Step 3: Convert to dictionary
            >> {'n_comp': 2.0, 'perp': 30.0, 'n_iter': 100.0, 'learning_rate': 200.0}
    :param s:
    :return:
    """
    s_ = s.split("__")
    s_ = [s.split("=") for s in s_]
    return {s[0]: float(s[1]) for s in s_}


def save_umap_results(data, out_filepath: Path):
    results = {}
    for model in UMAP_MODELS:
        logger.info(f"Working on UMAP model: {model}")
        umap = UMAP(
            n_components=model.n_components,
            n_neighbors=model.n_neighbors,
            min_dist=model.min_dist,
            random_state=SEED,
        )
        projections = umap.fit_transform(data)
        results[model.get_properties_str()] = {
            "proj": projections,
            "model": model.to_dict(),
        }
    with open(out_filepath, "wb") as f:
        pickle.dump(results, f)


def save_tsne_results(data, out_filepath: Path):
    results = {}
    for model in TSNE_MODELS:
        logger.info(f"Working on t-SNE model: {model}")
        tsne = TSNE(
            n_components=model.n_components,
            perplexity=model.perplexity,
            learning_rate=model.learning_rate,
            n_iter=model.num_iteration,
            init="random",
            random_state=SEED,
        )
        projections = tsne.fit_transform(data)
        results[model.get_properties_str()] = {
            "proj": projections,
            "model": model.to_dict(),
        }
    with open(out_filepath, "wb") as f:
        pickle.dump(results, f)


if __name__ == "__main__":

    df = px.data.iris()
    features = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]]

    save_tsne_results(features, TSNE_RESULTS_FILEPATH)
    save_umap_results(features, UMAP_RESULTS_FILEPATH)
