import json
import logging
import string
import time

from flask import Flask, request, g as app_ctx
from flask_pymongo import PyMongo

from src.indomain.question_classifier import user_input

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:[%(filename)s:%(lineno)d] - %(message)s [%(asctime)s]",
    datefmt="%H:%M:%S",
)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

app = Flask(__name__)
mongodb_client = PyMongo(app, uri="mongodb://mongo:27017/juli-chat")
db = mongodb_client.db
LOGGER.info(f'Db available is {db}')
time_in_ms = 0
input_global = ""
answer_global = ""
flag = 0

LOGGER.info(f'Ready to listen for request \n')


@app.route("/")
def hello_world():
    print("Get method")
    return "Hello Juli!"


@app.before_request
def logging_before():
    app_ctx.start_time = time.perf_counter()


@app.after_request
def logging_after(response):
    total_time = time.perf_counter() - app_ctx.start_time
    time_in_ms = int(total_time * 1000)
    LOGGER.info(
        f"The total execution time for the request is: {time_in_ms} ms {request.method}"
    )
    LOGGER.info(f"The input is {input_global} and the answer is {answer_global}")

    if flag == 0:
        LOGGER.info(
            f"Inserting the question-answer and response time in the Davinci collection"
        )
        db.davinci_avg.insert_one(
            {"question": input_global[0], "answer": answer_global, "time": time_in_ms}
        )

    else:
        LOGGER.info(
            f"Inserting the question-answer and response time in the Curie collection"
        )
        db.curie_avg.insert_one(
            {"question": input_global[0], "answer": answer_global, "time": time_in_ms}
        )

    return response


@app.route("/api/v1/answer_davinci", methods=["POST"])
def get_gpt3_answer():
    global input_global
    global answer_global
    global flag
    record = json.loads(request.data)
    inp = [record["question"]]
    LOGGER.info(f"The original input is {inp}")
    inp = [inp[0].translate(str.maketrans("", "", string.punctuation))]
    LOGGER.info(f"The cleaned input is {inp}")
    answer_returned = user_input(inp)
    LOGGER.info(f"Answer returned is {answer_returned}")
    if "[" in answer_returned:
        answer_returned = answer_returned.replace("[", "").replace("]", "")
    input_global = inp
    answer_global = answer_returned
    flag = 0
    return answer_returned, 200


@app.route("/api/v1/answer_curie", methods=["POST"])
def get_gpt3_answer_curie():
    global input_global
    global answer_global
    global flag
    record = json.loads(request.data)
    inp = [record["question"]]
    LOGGER.info(f"The original input is {inp}")
    inp = [inp[0].translate(str.maketrans("", "", string.punctuation))]
    LOGGER.info(f"The cleaned input is {inp}")
    answer_returned = user_input(inp, model_flag=1)
    LOGGER.info(f"Answer returned is {answer_returned}, {type(answer_returned)}")
    if "[" in answer_returned:
        answer_returned = answer_returned.replace("[", "").replace("]", "")
    print(answer_returned)
    input_global = inp
    answer_global = answer_returned
    flag = 1
    return answer_returned, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
