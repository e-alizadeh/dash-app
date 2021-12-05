import dash
import dash_bootstrap_components as dbc
from dashboard import app_layout, generate_callbacks


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.ZEPHYR],
    external_scripts=[
        "https://gist.githubusercontent.com/e-alizadeh/4b86f02ae6f6ea2a0c39a7e2ac1659eb/raw/023b713f2bf32a78a0282e4de8875e5efc2c9d58/gtag.js"
    ]
)
app.title = "Simple Dash App"
server = app.server

if __name__ == "__main__":
    app.layout = app_layout(app)
    generate_callbacks(app)
    app.run_server(debug=True, host="0.0.0.0", port=8000, use_reloader=False)
