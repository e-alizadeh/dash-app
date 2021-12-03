from pathlib import Path
from typing import Dict, List, Union

import dash_bootstrap_components as dbc
import pickle
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output
from enum import Enum

# from app.prepare_results import UMAP_RESULTS_FILEPATH, TSNE_RESULTS_FILEPATH
from prepare_results import TSNE_PARAMS, UMAP_PARAMS

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
    available_values: Dict[Union[int, float], str],
    default_value: Union[int, float],
    html_id: str,
) -> html.Div:
    min_value, max_value = min(available_values.keys()), max(available_values.keys())
    return html.Div(
        [
            dcc.Slider(
                min=min_value,
                max=max_value,
                marks=available_values,
                value=default_value,
                id=html_id,
                step=None,
            )
        ],
        className="slider",
    )


def generate_marks_for_sliders(
    values: List[Union[int, float]]
) -> Dict[Union[int, float], str]:
    return {i: str(i) for i in values}


def app_layout(app) -> dbc.Container:
    controls = html.Div(
        [
            # UMAP/t-SNE Selection
            dbc.Card(
                [
                    dbc.Label("Projection technique", className="card_title"),
                    dcc.RadioItems(
                        id="selected-method-radio-item",
                        options=[
                            {
                                "label": " " + DimReductionMethods.UMAP.value,
                                "value": DimReductionMethods.UMAP.value,
                            },
                            {
                                "label": " " + DimReductionMethods.TSNE.value,
                                "value": DimReductionMethods.TSNE.value,
                            },
                        ],
                        value=DimReductionMethods.TSNE.value,
                        className="radio_item",
                    ),
                ],
                className="control_box",
                style={"margin-bottom": "10px", "padding-left": "4%"},
            ),
            # Dimensionality Reduction Configuration
            # ------
            # t-SNE config
            html.Div(
                dbc.Card(
                    [
                        dbc.Label("t-SNE Configuration", className="card_title"),
                        dbc.Label("Perplexity", className="param_headers"),
                        wrapper_slider(
                            default_value=min(TSNE_PARAMS["perplexity"]),
                            available_values=generate_marks_for_sliders(
                                TSNE_PARAMS["perplexity"]
                            ),
                            html_id="slider-perplexity",
                        ),
                        dbc.Label("Learning Rate", className="param_headers"),
                        wrapper_slider(
                            default_value=min(TSNE_PARAMS["learning_rates"]),
                            available_values=generate_marks_for_sliders(
                                TSNE_PARAMS["learning_rates"]
                            ),
                            html_id="slider-learning-rate",
                        ),
                        dbc.Label("Number of Iterations", className="param_headers"),
                        wrapper_slider(
                            default_value=min(TSNE_PARAMS["n_iterations"]),
                            available_values=generate_marks_for_sliders(
                                TSNE_PARAMS["n_iterations"]
                            ),
                            html_id="slider-num-iterations",
                        ),
                    ],
                    style={"padding-left": "4%"},
                ),
                className="control_box",
                id="tsne-sliders",
            ),
            # UMAP config
            html.Div(
                dbc.Card(
                    [
                        dbc.Label("UMAP Configuration", className="card_title"),
                        dbc.Label("Number of Neighbors", className="param_headers"),
                        wrapper_slider(
                            default_value=min(UMAP_PARAMS["n_neighbors"]),
                            available_values=generate_marks_for_sliders(
                                UMAP_PARAMS["n_neighbors"]
                            ),
                            html_id="slider-num-neighbors",
                        ),
                        dbc.Label("Minimum Distance", className="param_headers"),
                        wrapper_slider(
                            default_value=min(UMAP_PARAMS["min_dist"]),
                            available_values=generate_marks_for_sliders(
                                UMAP_PARAMS["min_dist"]
                            ),
                            html_id="slider-min-distance",
                        ),
                    ],
                    style={"padding-left": "4%"},
                ),
                className="control_box",
                id="umap-sliders",
            ),
        ],
    )
    header = dbc.Row(
        [
            dbc.Col(
                html.A(
                    href="https://ealizadeh.com",
                    children=[
                        html.Img(
                            src=app.get_asset_url("favicon.png"),
                            style={"width": "30%"},
                        )
                    ],
                ),
                width=3,
                align="left",
            ),
            dbc.Col(
                html.H1(
                    "Interactive Dashboard for t-SNE and UMAP",
                    # style={"float": "right"},
                ),
                width=9,
                align="center",
            ),
        ]
    )
    return dbc.Container(
        [
            header,
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            dcc.Markdown(
                                """
                        This page contains an interactive web-app that shows the 
                    """
                            ),
                            dbc.Button("Click", color="success", className="mt-auto"),
                        ]
                    ),
                    className="control_box",
                ),
                width={"size": 6, "offset": 2},
            ),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(controls, md=3),
                    dbc.Col(
                        dbc.Card(dcc.Graph(id="scatter-plot"), className="plot_box"),
                        md=8,
                    ),
                ],
                align="center",
            ),
        ],
        style={"margin-left": "5%", "margin-right": "5%", "margin-top": "50px"},
        fluid=True,
    )


def generate_callbacks(app):
    @app.callback(
        [
            Output("scatter-plot", "figure"),
            Output("tsne-sliders", component_property="hidden"),
            Output("umap-sliders", component_property="hidden"),
        ],
        [
            Input("selected-method-radio-item", "value"),
            Input("slider-perplexity", "value"),
            Input("slider-learning-rate", "value"),
            Input("slider-num-iterations", "value"),
            Input("slider-num-neighbors", "value"),
            Input("slider-min-distance", "value"),
        ],
    )
    def add_graph(
        selected_method,
        tsne_perplexity,
        tsne_learning_rate,
        tsne_num_iterations,
        umap_num_neighbors,
        umap_min_distance,
    ):
        df = px.data.iris()

        if selected_method == DimReductionMethods.UMAP.value:
            proj_results = UMAP_PROJECTION_RESULTS[
                f"n_comp=2__n_neigh={umap_num_neighbors}__min_dist={umap_min_distance:.1f}"
            ]["proj"]
            tsne_style, umap_style = True, False
        else:
            # By default, it's t-SNE
            proj_results = TSNE_PROJECTION_RESULTS[
                f"n_comp=2__perp={tsne_perplexity}__n_iter={tsne_num_iterations}__learning_rate={tsne_learning_rate}"
            ]["proj"]
            tsne_style, umap_style = False, True

        fig = px.scatter(
            proj_results, x=0, y=1, color=df.species, labels={"color": "species"}
        )
        return fig, tsne_style, umap_style
