
# Conversational Agent for Asthmatic Patients (Master Research Project)

This project is demonstration of a general purpose Converstaional Agent, currently
domain constrained on Asthma. However, much of the methodologies followed in this
project are extendible to different chronic diseases.

The project makes use of Sentence Transformers and GPT3 to answer user queries 
related to Asthma. Because of dependencies on different libraries like `PyTorch` that
makes the environment of the project larger, a smaller `requirements.txt` file is
attatched.

The project can be run via `docker compose up` without having to build the environment
locally, as the environment will then be setup inside the `engine` container.

Typical questions that the Converstaional Agent can answer are as follows:

    - I did not sleep well yesterday, and my Asthma has worsened. What should I do?
    - Is not a good time to go out for a walk?
    - Can I go swimming if I have Asthma?
    - What happens to my data that is collected?

The questions can be passed as `raw json body` either via postman or any other alternatives.

Since there is no UI integrated at the moment as this is just the backend, 
unfortunately sending `POST` requests is the only way to get responses from the 
Converstaional Agent.



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

1) Run via `entrypoint.py`

```bash
  cd src
  pip install -r requirements.txt
  python entrypoint.py
```

2) Run via `docker`

```bash
  docker compose up --build
```


