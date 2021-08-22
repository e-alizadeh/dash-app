from enum import Enum

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
from sklearn.manifold import TSNE
from umap import UMAP

SEED = 0


class DimReductionMethods(Enum):
    UMAP = "umap"
    TSNE = "t-sne"


def app_layout() -> html.Div:
    return html.Div(
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
                value="tsne",
            ),
            dcc.Loading(
                id="loading-1",
                type="default",
                children=html.Div(dcc.Graph(id="scatter-plot")),
            ),
        ]
    )


def app_callbacks(app):
    @app.callback(
        Output("scatter-plot", "figure"), [Input("selected-method-radio-item", "value")]
    )
    def add_graph(selected_method):
        df = px.data.iris()
        features = df.loc[:, :"petal_width"]

        if selected_method == DimReductionMethods.UMAP.value:
            umap = UMAP(n_components=2, init="random", random_state=SEED)
            projections = umap.fit_transform(features)
        elif selected_method == DimReductionMethods.TSNE.value:
            tsne = TSNE(n_components=2, random_state=SEED)
            projections = tsne.fit_transform(features)
        else:
            umap = UMAP(n_components=2, init="random", random_state=SEED)
            projections = umap.fit_transform(features)

        fig = px.scatter(
            projections, x=0, y=1, color=df.species, labels={"color": "species"}
        )
        return fig


if __name__ == "__main__":
    app = dash.Dash()
    app.layout = app_layout()
    app_callbacks(app)
    app.run_server(debug=True, use_reloader=False)
