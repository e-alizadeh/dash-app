import pickle
from enum import Enum
from pathlib import Path
from typing import Dict, List, Union

import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output

# from app.prepare_results import UMAP_RESULTS_FILEPATH, TSNE_RESULTS_FILEPATH

DATA_DIR = Path(".")
TSNE_RESULTS_FILEPATH = DATA_DIR.joinpath("tsne_projection_results.pkl")
UMAP_RESULTS_FILEPATH = DATA_DIR.joinpath("umap_projection_results.pkl")
SEED = 0


class DimReductionMethods(Enum):
    UMAP = "UMAP"
    TSNE = "t-SNE"


with open(UMAP_RESULTS_FILEPATH, "rb") as f:
    UMAP_PROJECTION_RESULTS = pickle.load(f)


with open(TSNE_RESULTS_FILEPATH, "rb") as f:
    TSNE_PROJECTION_RESULTS = pickle.load(f)


def wrapper_slider(
    title: str,
    available_values: Dict[Union[int, float], str],
    default_value: Union[int, float],
    html_id: str,
) -> html.Div:
    min_value, max_value = min(available_values.keys()), max(available_values.keys())
    return html.Div(
        children=[
            html.Div([f"{title}"]),
            html.Div(
                children=[
                    dcc.Slider(
                        min=min_value,
                        max=max_value,
                        marks=available_values,
                        value=default_value,
                        id=html_id,
                    )
                ],
            ),
        ],
        style={
            "margin-left": "5px",
            "margin-top": "25px",
            # "margin-right": "30px"
        },
    )


def generate_marks_for_sliders(
    values: List[Union[int, float]]
) -> Dict[Union[int, float], str]:
    return {i: str(i) for i in values}


def app_layout(app) -> html.Div:
    return html.Div(
        [
            html.Div(
                style={"background-color": "#f9f9f9"},
                children=[
                    html.Img(
                        src=app.get_asset_url("favicon.ico"),
                        className="two columns",
                    ),
                    html.H3(
                        "t-SNE Explorer",
                        style={"float": "right"},
                        className="nine columns",
                    ),
                ],
            ),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.RadioItems(
                                id="selected-method-radio-item",
                                options=[
                                    {
                                        "label": DimReductionMethods.UMAP.value,
                                        "value": DimReductionMethods.UMAP.value,
                                    },
                                    {
                                        "label": DimReductionMethods.TSNE.value,
                                        "value": DimReductionMethods.TSNE.value,
                                    },
                                ],
                                value=DimReductionMethods.TSNE.value,
                            ),
                        ],
                        style={"margin-left": "5px"},
                        className="twelve columns",
                    ),
                    html.Div(
                        [
                            wrapper_slider(
                                title="Perplexity",
                                default_value=2,
                                available_values=generate_marks_for_sliders([2, 3, 5]),
                                html_id="slider-perplexity",
                            ),
                            wrapper_slider(
                                title="Learning Rate",
                                default_value=2,
                                available_values=generate_marks_for_sliders([2, 3, 5]),
                                html_id="slider-learning-rate",
                            ),
                            wrapper_slider(
                                title="Number of Iterations",
                                default_value=2,
                                available_values=generate_marks_for_sliders([2, 3, 5]),
                                html_id="slider-num-iterations",
                            ),
                        ],
                        style={"display": "inline-block"},
                        className="three columns",
                    ),
                    html.Div(
                        [
                            dcc.Loading(
                                id="loading-1",
                                type="default",
                                children=html.Div(dcc.Graph(id="scatter-plot")),
                            ),
                        ],
                        style={"display": "inline-block"},
                        className="nine columns",
                    ),
                ]
            ),
        ]
    )


def generate_callbacks(app):
    @app.callback(
        Output("scatter-plot", "figure"), [Input("selected-method-radio-item", "value")]
    )
    def add_graph(selected_method):
        df = px.data.iris()
        features = df.loc[:, :"petal_width"]

        if selected_method == DimReductionMethods.UMAP.value:
            proj_results = UMAP_PROJECTION_RESULTS["n_comp=2__n_neigh=5__min_dist=0.1"][
                "proj"
            ]
        elif selected_method == DimReductionMethods.TSNE.value:
            proj_results = TSNE_PROJECTION_RESULTS[
                "n_comp=2__perp=30.0__n_iter=100__learning_rate=200.0"
            ]["proj"]
        else:
            proj_results = UMAP_PROJECTION_RESULTS["n_comp=2__n_neigh=5__min_dist=0.1"][
                "proj"
            ]

        fig = px.scatter(
            proj_results, x=0, y=1, color=df.species, labels={"color": "species"}
        )
        return fig
