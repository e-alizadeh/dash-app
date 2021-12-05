# dash-app

This repo contains the code to generate an interactive dashboard in Python using the Dash library. 

# Development Environment
For development purpose, I'd like to use [conda](https://docs.conda.io/en/latest/) environment 
with [Poetry](https://python-poetry.org/) as the package dependency resolver. 
You can check my post below if you're curious about the reasons for this development environment.
[A Guide to Python Environment, Dependency and Package Management: Conda + Poetry](https://ealizadeh.com/blog/guide-to-python-env-pkg-dependency-using-conda-poetry)

## Create conda environment
Assuming that you have conda and poetry installed and you're in the root directory of the repo, 
you need to do the following:

- Create conda environment: `conda env create -f dev-env.yaml`. 
- Activate the conda environment: `conda activate <env_name>`.
- Install the packages: `poetry install`

# Deployment Environment
Only for simplicity, the way I'm creating the deployment environment is different. 
I've basically created a deploy-env.txt file that I will use Pip to install. 
The main reason for this approach is:
- To reduce the Docker image size since conda usually makes the docker image size larger.
- To have a simpler Dockerfile 

Ideally, the above deployment environment should be created in a virtual environment!!

A reminder, this is just a proof-of-concept 😁 

# Running the app
## Locally (outside the container)
- Activate the environment: `conda activate dash_app`
- Go to `app/` directory.
- Run `python app.py`
- Go to http://localhost:8000/

## Run from the Docker container
- Run `docker build -t app-image .` (don't forget the last dot in the command!!)
- Run `docker run -d --name app-container -p 7000:8000 app-image`

Few points:
First time running `docker build` may take time since it downloads a docker image from DockerHub and then installs the environment. 
This will be cached, so next times will be much faster. 
In the `docker run`, the host port (8080) is mapped to the Docker container port 8000 (the port that Dash app is using).
Hence, to check the app, you need to go to http://localhost:7000/


### If you have any question, feel free to contact me [here](https://ealizadeh.com/contact).