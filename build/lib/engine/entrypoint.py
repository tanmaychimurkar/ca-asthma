import logging
import string
import sys

from engine.In_out_DomainClassification import user_input

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:[%(filename)s:%(lineno)d] - %(message)s [%(asctime)s]",
    datefmt="%H:%M:%S",
    stream=sys.stdout,
    encoding="utf-8",
)
# todo: remove root from the logger to disable logger messages from imported modules
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

while True:
    user_query = input("Please enter your question below: \n")
    LOGGER.info(f"User has entered the input. Invoking the pipeline")

    if user_query == "Quit" or user_query == "quit" or user_query == "exit":
        print(f"It was nice talking to you. See you later :)")
        LOGGER.info(f"User session terminated")
        break

    user_query = user_query.translate(str.maketrans("", "", string.punctuation))
    inp = [user_query]
    LOGGER.info(f"User did not exit, pipeline invoked")

    answer_returned = user_input(inp)
    if isinstance(answer_returned, list):
        answer_returned = answer_returned[0]
    LOGGER.info(f"The answer for the user question is: {answer_returned}")
