
# Conversational Agent for Asthamtic Patients (Research Project)

This project is demonstration of a general purpose Conversational Agent, currently
domain constrained on Asthma. However, much of the methodologies followed in this
project are extensible to different chronic diseases.

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

As this is a research project, not all answers will have a definitive answer, and 
might sometimes return a response which contains `placeholder by ..`. These will be
fixed in a future version of the release.

The questions can be passed as `raw json body` either via postman or any other alternatives.

Since there is no UI integrated at the moment as this is just the backend, 
unfortunately sending `POST` requests is the only way to get responses from the 
Conversational Agent.



## Run Locally

Clone the project

```bash
  git clone https://github.com/tanmaychimurkar/ca-asthma
```

Go to the project directory

```bash
  cd ca-asthma
```

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

