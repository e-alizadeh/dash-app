FROM continuumio/miniconda3:4.7.12

# Make sure that the Python output is sent straight to terminal w/o being first buffered. This way we can see the output of the app in real-time.
ENV PYTHONUNBUFFERED 1

COPY ./environment.yaml /

RUN apt-get --allow-releaseinfo-change update && apt-get install -y curl
RUN conda env create -qn dash_app -f /environment.yaml

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | POETRY_VERSION=1.1.11 python
ENV PATH "/root/.poetry/bin:${PATH}"

SHELL ["conda", "run", "-n", "dash_app", "/bin/bash", "-c"]

COPY pyproject.toml poetry.lock /
RUN poetry install --no-dev --no-root

RUN mkdir /app
WORKDIR /app
COPY ./app/ ./

