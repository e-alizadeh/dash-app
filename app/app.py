import dash
import dash_bootstrap_components as dbc
from dashboard import app_layout, generate_callbacks

app = dash.Dash("ABC", external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


if __name__ == "__main__":
    app.layout = app_layout(app)
    generate_callbacks(app)
    app.run_server(debug=True, host="0.0.0.0", port=8080, use_reloader=False)
