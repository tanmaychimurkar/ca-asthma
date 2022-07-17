import logging
import sys

from In_out_DomainClassification import user_input

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s:[%(filename)s:%(lineno)d] - %(message)s [%(asctime)s]',
                    datefmt='%H:%M:%S', stream=sys.stdout, encoding='utf-8')
# todo: remove root from the logger to disable logger messages from imported modules
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

while True:
    user_query = input("Please enter your question below: \n")
    LOGGER.info(f'User has entered the input. Invoking the pipeline')

    if user_query == 'Quit' or user_query == 'quit' or user_query == 'exit':
        print(f'It was nice talking to you. See you later :)')
        LOGGER.info(f'User session terminated')
        break

    inp = [user_query]
    LOGGER.info(f'User did not exit, pipeline invoked')

    answer_returned = user_input(inp)
    LOGGER.info(f'The answer for the user question is: {answer_returned}')
    print(answer_returned)

    # append_interaction_to_chat_log(inp1,answer_returned,None)

# todo: indexing files for not retrianing, indomain and verb noun pair, weather integration, api for entrypoint,
#  todo: pipeline 2: default context for all outdomain questions. So verb-noun pair not necessary, but more testing
#   might be needed


# todo: @prasun: api deployment + pipeline2, @tanmay: cleanup, weather, no retraining,
#  todo new tomorrow: joris questions


# todo: done so far, pipeline 1 changes made, maybe a bit of speed stuff done.
