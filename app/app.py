import dash

# import uvicorn as uvicorn
from dashboard import app_layout, generate_callbacks

# from fastapi import FastAPI
# from starlette.middleware.wsgi import WSGIMiddleware

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]


if __name__ == "__main__":
    # app = dash.Dash(__name__, requests_pathname_prefix="/dash/")

    app = dash.Dash("ABC", external_stylesheets=external_stylesheets)
    server = app.server
    app.layout = app_layout(app)
    generate_callbacks(app)
    app.run_server(debug=True, use_reloader=False)

    # server = FastAPI()
    # server.mount("/dash", WSGIMiddleware(app.server))
    # uvicorn.run(server)
