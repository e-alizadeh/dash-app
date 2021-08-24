import pickle
from dataclasses import dataclass
from pathlib import Path

import plotly.express as px
from dataclasses_json import dataclass_json
from sklearn.manifold import TSNE
from umap import UMAP

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


TSNE_MODELS = [TSNEobj(perplexity=30.0, num_iteration=100, learning_rate=200.0)]

UMAP_MODELS = [UMAPobj(n_neighbors=5)]


def save_umap_results(data, out_filepath: Path):
    results = {}
    for model in UMAP_MODELS:
        umap = UMAP(init="random", random_state=SEED)
        projections = umap.fit_transform(data)
        results[model.get_properties_str()] = {"proj": projections, "model": model}
    with open(out_filepath, "wb") as f:
        pickle.dump(results, f)


def save_tsne_results(data, out_filepath: Path):
    results = {}
    for model in TSNE_MODELS:
        tsne = TSNE(n_components=2, random_state=SEED)
        projections = tsne.fit_transform(data)
        results[model.get_properties_str()] = {"proj": projections, "model": model}
    with open(out_filepath, "wb") as f:
        pickle.dump(results, f)


def generate_results(data) -> None:
    save_tsne_results(data, TSNE_RESULTS_FILEPATH)
    save_umap_results(data, UMAP_RESULTS_FILEPATH)


if __name__ == "__main__":

    df = px.data.iris()
    features = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]]

    save_tsne_results(features, TSNE_RESULTS_FILEPATH)
    save_umap_results(features, UMAP_RESULTS_FILEPATH)
