
# Project Title

A brief description of what this project does and who it's for


# Conversational Agent for Asthmatic Patients (Master Research Project)

This project is demonstration of a general purpose Conversational Agent, currently
domain constrained on Asthma. However, much of the methodologies followed in this
project are extendable to different chronic diseases.

The project makes use of Sentence Transformers and GPT3 to answer user queries 
related to Asthma. Because of dependencies on different libraries like `PyTorch` that
makes the environment of the project larger, a smaller `requirements.txt` file is
attached.

The project can be run via `docker compose up` without having to build the environment
locally, as the environment will then be setup inside the `engine` container.

Typical questions that the Conversational Agent can answer are as follows:

    - I did not sleep well yesterday, and my Asthma has worsened. What should I do?
    - Is not a good time to go out for a walk?
    - Can I go swimming if I have Asthma?
    - What happens to my data that is collected?

The questions can be passed as `raw json body` either via postman or any other alternatives. Below is the format of 
the `json` body that has to be passed:

API endpoint: `127.0.0.1:5000/api/v1/answer_davinci` (Note: The endpoint can be changed to use the `curie` model by
modifying it to `answer_curie`)

`NOTE`: It is advisable to keep the default port `5000` open for the application to run, as this port is set in a custom docker image that is created. If the port is occupied, you may open it with the following command:

```bash
sudo kill -9 `sudo lsof -t -i:5000`
```

JSON body:

```
{
    "question": "Can I go outside to play if I don't have asthma?"
}
```


Since there is no UI integrated at the moment as this is just the backend, 
unfortunately sending `POST` requests is the only way to get responses from the 
Conversational Agent.



## Installation

Clone the project

```bash
  git clone https://github.com/tanmaychimurkar/ca-asthma
```

Go to the project directory

```bash
  cd ca-asthma
```

Note: Before running the script, we need to make sure to create a `.env` file 
which contains the following API keys as variables:

`weather_api_key`: (key from here: https://docs.ambeedata.com/) 

`openai_api_key`: (key from here: https://beta.openai.com/signup)

The `.env` file has to be created in the project root where the `docker-compose.yaml` file exists


1) Run via `entrypoint.py`

```bash
  cd src
  pip install -r requirements.txt
  python entrypoint.py
```

Note: If running via entrypoint gives the error `ModuleError: No module named src`, then the following commands have 
to be run from the project root (from inside the activated virtual environment):

```bash
  python -m pip install --upgrade pip
  python -m pip install build
  python -m build --sdist
  python -m build --wheel
  pip install -e .
  python -m nltk.downloader all
```

After these steps, re-run the entrypoint and the code should then be working.

2) Run via `docker`

```bash
  docker compose up --build
```

Note: For running via docker, the default Flask port `5000` has to be open to accept connections, since the flask application 
is being run from the custom docker image that we have uploaded to docker hub.

Responses and the API execution time can be seen on mongo-express UI when run via `docker` at `http://localhost:8081/`


