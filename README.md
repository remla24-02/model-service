# REMLA TEAM 2 Phishing Model Service
This is Team 2's model service for Release Engineering in Machine Learning Applications 2023/24. It operates as a FastAPI-based REST API. It predicts URL legitimacy, handling POST requests containing URLs and promptly returning phishing predictions from the model.

## Prerequisites
Python 3.12 is required to run the code.  
To install the required packages a pyproject.toml has been provided for use with [Poetry](https://python-poetry.org/docs/).
This has been testing using Poetry version 1.7.1.
Poetry can be installed with pip with the following command:
``` console
pip install poetry
```

To run on a NVidia GPU

``` console
sudo apt-get install -y nvidia-container-toolkit nvidia-docker2
sudo systemctl restart docker
```


## Configuration
For running locally or when building the Dockerfile, create a `.env` file containing:

``` file
APP_NAME=               (default: Client API)
IS_DEBUG=               (default: False)
HOST=                   (default: 0.0.0.0)
PORT=                   (default: 8080)
API_KEY=                (secret)
DEFAULT_MODEL_PATH=     (default: ./model/trained_model.joblib)
ALLOWED_HOSTS=          (default: *)
```


## Installation

### Docker

From the Github Package registry:

``` console
docker pull ghcr.io/remla24-02/model_service:latest
docker run -p 8080:8080 --name model_service -it ghcr.io/remla24-02/model_service:latest
```

Build from source:

``` console
docker build . -t model_service
docker run -p 8080:8080 --name model_service -it model_service
```

### Local
To run the application without using Docker:

``` console
git clone https://github.com/remla24-02/model-service.git
cd model
poetry install --no-root
```

This cloned the repository and installed all the packages into an environment.
Next, open a new shell for the environment with the following command:
``` console
poetry shell
python ./app/main.py
```

## Usage

1. Then go to [http://localhost:8000/docs](http://localhost:8000/docs).

2. Click `authorize` and enter the API key

3. Use the prediction POST API to do a prediction on a URL.

### POST Request
To perform a POST request on `/predict` you must include the API key as `token` in the header. The body must look like this:

``` json
{
    "url": "<URL>"
}
```

Your then get back a JSON response containing:

``` json
{
  "prediction": <0|1>
}
```

## Project structure
``` console
$ tree
.
├── app
│   ├── api                     # <-- Entry points (routes)
│   │   ├── health.py           # <-- Heartbeat to check if server is online
│   │   └── prediction.py       # <-- Prediction API
│   ├── core
│   │   ├── app.py              # <-- Creates the FastAPI app
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── event_handlers.py
│   │   └── security.py         # <-- Secures API with token
│   ├── main.py
│   ├── models                  # <-- Data definitions
│   │   ├── heartbeat.py
│   │   ├── payload.py
│   │   └── prediction.py
│   ├── services                
│   │   └── model_service.py    # <-- Queries model
│   └── utils
│       ├── get_model.py        # <-- Download trained model
│       ├── logging.py
│       └── singleton.py
├── config.ini                  # <-- Logging configuration
├── LICENSE
├── model                       # <-- Contains model
├── pyproject.toml
└── README.md
```