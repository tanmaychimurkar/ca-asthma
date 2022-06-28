import os
import openai
openai.api_key = "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"
completion = openai.Completion()
os.environ["TOKENIZERS_PARALLELISM"] = "false"

start_sequence = "\nJuli:"
restart_sequence = "\n\nPerson:"
session_prompt = ""

chat_log = ''
chat_log += session_prompt

def ask(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = openai.Completion.create(
    engine="davinci",
    prompt=prompt_text,
    temperature=0.8,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.3,
    stop=["\n"]
    )
    story = response['choices'][0]['text']
    return str(story)

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None: 
        chat_log = session_prompt
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'


def answer_gpt3(incoming_msg):
    global chat_log
    answer = ask(incoming_msg, chat_log)
    #session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer,chat_log)
    chat_log = append_interaction_to_chat_log(incoming_msg, answer,chat_log)
    return answer

# answer_returned = answer_gpt3("Where is China?")
# print(answer_returned)