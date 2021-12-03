import dash
import dash_bootstrap_components as dbc
from dashboard import app_layout, generate_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR])
app.title = "Simple Dash App"
server = app.server


if __name__ == "__main__":
    app.layout = app_layout(app)
    generate_callbacks(app)
    app.run_server(debug=True, host="0.0.0.0", port=8000, use_reloader=False)
