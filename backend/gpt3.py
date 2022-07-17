import logging

import openai
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s:[%(filename)s:%(lineno)d] - %(message)s [%(asctime)s]',
                    datefmt='%H:%M:%S')

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

openai.api_key = os.getenv('openai_api_key')
completion = openai.Completion()
os.environ["TOKENIZERS_PARALLELISM"] = "false"

start_sequence = "\n\n"
restart_sequence = "\n\n"
default_session_prompt = "Conversation for Asthma"

chat_log = ''
chat_log += default_session_prompt


def ask(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt_text,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]
    )
    story = response['choices'][0]['text']
    return str(story)


def append_interaction_to_chat_log(question, answer, chat_log):
    if chat_log is None:
        chat_log = default_session_prompt
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'


def answer_gpt3(incoming_msg):
    global chat_log
    answer = ask(incoming_msg, chat_log)
    # session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer,chat_log)
    chat_log = append_interaction_to_chat_log(incoming_msg, answer, chat_log)
    # LOGGER.info(f'The chat log is {chat_log}')
    print(chat_log, "#"*10)
    print(answer)
    return answer


# answer_returned = answer_gpt3("Where is China?")
# print(answer_returned)
