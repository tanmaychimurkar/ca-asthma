import os

import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("openai_api_key")
completion = openai.Completion()
os.environ["TOKENIZERS_PARALLELISM"] = "false"

start_sequence = "\nJuli:"
restart_sequence = "\n\nPerson:"
chat_log = "Context is Asthma."


# chat_log = ''
# chat_log += session_prompt


def ask(question):
    global chat_log
    prompt_text = f"{chat_log}{restart_sequence}: {question}{start_sequence}:"
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt_text,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"],
    )
    story = response["choices"][0]["text"]
    return str(story)


def ask_curie(question, chat_log=None):
    prompt_text = f"{chat_log}{restart_sequence}: {question}{start_sequence}:"
    response = openai.Completion.create(
        engine="text-curie-001",
        prompt=prompt_text,
        temperature=0.8,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.3,
        stop=["\n"],
    )
    story = response["choices"][0]["text"]
    return str(story)


def ask_ada(question, chat_log=None):
    prompt_text = f"{chat_log}{restart_sequence}: {question}{start_sequence}:"
    response = openai.Completion.create(
        engine="text-ada-001",
        prompt=prompt_text,
        temperature=0.8,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.3,
        stop=["\n"],
    )
    story = response["choices"][0]["text"]
    return str(story)


def ask_babbage(question, chat_log=None):
    prompt_text = f"{chat_log}{restart_sequence}: {question}{start_sequence}:"
    response = openai.Completion.create(
        engine="text-babbage-001",
        prompt=prompt_text,
        temperature=0.8,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.3,
        stop=["\n"],
    )
    story = response["choices"][0]["text"]
    return str(story)


def append_interaction_to_chat_log(question, answer):
    global chat_log
    chat_log += question[0] + answer
    return chat_log


def answer_gpt3(incoming_msg, curie_flag=0):
    if curie_flag == 0:
        answer = ask(incoming_msg)
    else:
        answer = ask_curie(incoming_msg)
    if answer == incoming_msg:
        answer_gpt3(incoming_msg, curie_flag)
    return answer
