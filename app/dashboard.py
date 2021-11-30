from pathlib import Path
from typing import Dict, List, Union

import dash_bootstrap_components as dbc
import pickle
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output
from enum import Enum

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
    return dcc.Slider(
        # html.H5(f"{title}"),
        # html.Div(
        #     children=[
        min=min_value,
        max=max_value,
        marks=available_values,
        value=default_value,
        id=html_id,
        step=None,
    )
    #     ],
    # )
    # ],
    # style={
    #     "margin-left": "5px",
    #     "margin-top": "25px",
    #     # "margin-right": "30px"
    # },
    # )


def generate_marks_for_sliders(
    values: List[Union[int, float]]
) -> Dict[Union[int, float], str]:
    return {i: str(i) for i in values}


def app_layout(app) -> dbc.Container:
    controls = dbc.Card(
        [
            # UMAP/t-SNE Selection
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
                        style={"background-color": "SkyBlue"},
                    ),
                ]
            ),
            # Dimensionality Reduction Configuration
            # html.Div(
            #     [
            # t-SNE config
            html.Div(
                [
                    dbc.Label("t-SNE Configuration"),
                    dbc.Label("Perplexity"),
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
                # style={"display": "inline-block"},
                # className="three columns",
                id="tsne-sliders",
            ),
            # UMAP config
            html.Div(
                [
                    dbc.Label("UMAP Configuration"),
                    wrapper_slider(
                        title="Number of Neighbors",
                        default_value=2,
                        available_values=generate_marks_for_sliders([2, 3, 5]),
                        html_id="slider-num-neighbors",
                    ),
                    wrapper_slider(
                        title="Minimum Distance",
                        default_value=0.1,
                        available_values=generate_marks_for_sliders([0.1, 3, 5]),
                        html_id="slider-min-distance",
                    ),
                ],
                # style={"display": "inline-block"},
                # className="three columns",
                id="umap-sliders",
            ),
        ],
        style={"background-color": "LightGreen"},
    )
    # ],
    #     body=True
    # )
    return dbc.Container(
        [
            # dbc.Row(dbc.Col(
            # html.Div(
            #     style={"background-color": "blue"},  # "#f9f9f9"
            #     children=[
            #         html.Img(
            #             src=app.get_asset_url("dash-logo.png"),
            #             className="two columns",
            #             style={"margin-left": "5%"},
            #         ),
            #         html.H3(
            #             "Interactive Dashboard for t-SNE and UMAP",
            #             style={"float": "right"},
            #             className="nine columns",
            #         ),
            #     ],
            # ))),
            html.H1("Temp"),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(controls, md=4),
                    dbc.Col(dcc.Graph(id="scatter-plot"), md=8),
                ],
                align="center",
            ),
        ],
        # style={"margin-left": "5%", "margin-right": "5%"},
        fluid=True,
    )


def generate_callbacks(app):
    @app.callback(
        # [
        Output("scatter-plot", "figure"),
        # Output("tsne-sliders", "style"),
        # Output("umap-sliders", "style"),
        Output("tsne-sliders", component_property="hidden"),
        Output("umap-sliders", component_property="hidden"),
        # ],
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
        # features = df.loc[:, :"petal_width"]

        if selected_method == DimReductionMethods.UMAP.value:
            proj_results = UMAP_PROJECTION_RESULTS["n_comp=2__n_neigh=5__min_dist=0.1"][
                "proj"
            ]
            tsne_style, umap_style = True, False
        elif selected_method == DimReductionMethods.TSNE.value:
            proj_results = TSNE_PROJECTION_RESULTS[
                "n_comp=2__perp=30.0__n_iter=100__learning_rate=200.0"
            ]["proj"]
            tsne_style, umap_style = False, True
        else:
            proj_results = UMAP_PROJECTION_RESULTS["n_comp=2__n_neigh=5__min_dist=0.1"][
                "proj"
            ]
            tsne_style, umap_style = True, False

        fig = px.scatter(
            proj_results, x=0, y=1, color=df.species, labels={"color": "species"}
        )
        return fig, tsne_style, umap_style
