from pathlib import Path
from typing import Dict, List, Union

import dash_bootstrap_components as dbc
import pickle
import plotly.express as px
from dash import Input, Output, callback_context, dcc, html
from plotly.graph_objs import Figure  # Only used for type hint!
from prepare_results import TSNE_PARAMS, UMAP_PARAMS

DATA_DIR = Path(".")
TSNE_RESULTS_FILEPATH = DATA_DIR.joinpath("tsne_projection_results.pkl")
UMAP_RESULTS_FILEPATH = DATA_DIR.joinpath("umap_projection_results.pkl")

_BADGE_COLOR = "#0000cd"

html_anchor_attrs = dict(
    target="_blank",  # Open in a new tab/window
    rel="noreferrer noopener",  # Prevent malicious attacks
)

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
                    dbc.Label(
                        "Projection technique",
                        className="card_title",
                        style={"margin-left": "4%"},
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Button(
                                    "tSNE",
                                    id="tsne-button",
                                    color="warning",
                                    outline=True,
                                    active=True,
                                    className="me-1",
                                ),
                                width=4,
                            ),
                            dbc.Col(
                                dbc.Button(
                                    "UMAP",
                                    id="umap-button",
                                    color="danger",
                                    outline=True,
                                    active=False,
                                    className="me-1",
                                ),
                                width=4,
                            ),
                        ],
                        justify="center",
                    ),
                ],
                className="control_box",
                style={"margin-bottom": "20px"},
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
                    className="control_box params_box",
                ),
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
                    className="control_box params_box",
                ),
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
                    **html_anchor_attrs,
                ),
                width=3,
                align="left",
            ),
            dbc.Col(
                html.H1(
                    "Interactive Dashboard for t-SNE and UMAP",
                ),
                width=9,
                align="center",
            ),
        ]
    )
    return dbc.Container(
        [
            header,
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.P(
                                    """
                                    This page contains an interactive app using the ubiquitous Iris data.
                                    The main goal here was to deploy a containerized Dash app.
                                    The app uses two popular dimensionality reduction techniques, namely
                                    t-SNE and UMAP to project higher dimensional data into a 2D plane. 
                                    You can choose between different configurations for each technique. 
                                    Custom CSS style in Dash
                                """
                                ),
                                html.A(
                                    dbc.Badge(
                                        "Python",
                                        color=_BADGE_COLOR,
                                        className="me-1",
                                    ),
                                    href="https://www.python.org/",
                                    **html_anchor_attrs,
                                ),
                                html.A(
                                    dbc.Badge(
                                        "Dash by Plotly",
                                        color=_BADGE_COLOR,
                                        className="me-1",
                                    ),
                                    href="https://dash.plotly.com/",
                                    **html_anchor_attrs,
                                ),
                                html.A(
                                    dbc.Badge(
                                        "Plotly", color=_BADGE_COLOR, className="me-1"
                                    ),
                                    href="https://plotly.com/",
                                    **html_anchor_attrs,
                                ),
                                html.A(
                                    dbc.Badge(
                                        "Docker", color=_BADGE_COLOR, className="me-1"
                                    ),
                                    href="https://www.docker.com/",
                                    **html_anchor_attrs,
                                ),
                                html.A(
                                    dbc.Badge(
                                        "Heroku", color=_BADGE_COLOR, className="me-1"
                                    ),
                                    href="https://www.heroku.com/",
                                    **html_anchor_attrs,
                                ),
                                dbc.Badge(
                                    "Custom CSS", color=_BADGE_COLOR, className="me-1"
                                ),
                                html.A(
                                    dbc.Button(
                                        "Go to source code",
                                        color="dark",
                                        active=True,
                                        style={
                                            "float": "right",
                                            "background-color": "#333333",
                                            "margin-top": "-6px",
                                        },
                                    ),
                                    href="https://github.com/e-alizadeh/dash-app",
                                    **html_anchor_attrs,
                                )
                            ]
                        ),
                        className="text_box",
                    ),
                    width=8,
                ),
                justify="center",
            ),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(controls, md=3),
                    dbc.Col(
                        dbc.Card(dcc.Graph(id="scatter-plot", config={"displaylogo": False}), className="plot_box"),
                        md=8,
                    ),
                ],
                align="center",
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Label("© 2021 Esmaeil Alizadeh", style={"font-weight": "bold"}),
                    width={"size": 4, "offset": 5},
                    style={"margin-top": "40px"},
                )
            ),
        ],
        style={"margin-top": "50px"},
        fluid=True,
    )


def _update_plot_style(fig: Figure) -> Figure:
    """Caution: This function changes the input object

    :param fig:
    :return:
    """
    fig.update_traces(
        marker=dict(size=18, line=dict(width=2, color="black")),
        opacity=0.5,
        # font_family="Courier New"
    )
    fig.update_layout(legend_font_size=18)

    axes_style = dict(title_font_size=24, title_text="", tickfont_size=18)
    fig.update_xaxes(axes_style)
    fig.update_yaxes(axes_style)
    return fig


def generate_callbacks(app):
    @app.callback(
        [
            Output("scatter-plot", "figure"),
            Output("tsne-sliders", component_property="hidden"),
            Output("umap-sliders", component_property="hidden"),
            Output("tsne-button", "active"),
            Output("umap-button", "active"),
        ],
        [
            # Input("selected-method-radio-item", "value"),
            Input("tsne-button", "n_clicks"),
            Input("umap-button", "n_clicks"),
            Input("slider-perplexity", "value"),
            Input("slider-learning-rate", "value"),
            Input("slider-num-iterations", "value"),
            Input("slider-num-neighbors", "value"),
            Input("slider-min-distance", "value"),
        ],
    )
    def add_graph(
        tsne_button,
        umap_button,
        tsne_perplexity,
        tsne_learning_rate,
        tsne_num_iterations,
        umap_num_neighbors,
        umap_min_distance,
    ):
        # Even thought tsne_button and umap_button input arguments are not explictly used in this function,
        #   however, they should be present in order to trigger this callback whenever they are clicked,
        #   and hence, they will be present in the callback_context as an element that was changed!
        changed_id = [p["prop_id"] for p in callback_context.triggered][0]

        if "umap-button" in changed_id:
            proj_results = UMAP_PROJECTION_RESULTS[
                f"n_comp=2__n_neigh={umap_num_neighbors}__min_dist={umap_min_distance:.1f}"
            ]["proj"]
            hide_tsne_params_box, hide_umap_params_box = True, False
            tsne_button_active, umap_button_active = False, True
        else:
            # By default, it's t-SNE
            proj_results = TSNE_PROJECTION_RESULTS[
                f"n_comp=2__perp={tsne_perplexity}__n_iter={tsne_num_iterations}__learning_rate={tsne_learning_rate}"
            ]["proj"]
            hide_tsne_params_box, hide_umap_params_box = False, True
            tsne_button_active, umap_button_active = True, False

        df = px.data.iris()
        fig = px.scatter(
            proj_results, x=0, y=1, color=df.species, labels={"color": "Species"}
        )

        return (
            _update_plot_style(fig),
            hide_tsne_params_box,
            hide_umap_params_box,
            tsne_button_active,
            umap_button_active,
        )
