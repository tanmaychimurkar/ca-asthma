from fa_chat_close import genResults
from fa_chat_close import getBertAnswer
from gpt3 import answer_gpt3
from NER_POS import get_data
from NER_POS import pos_tagging
from nltk import pos_tag
from nltk import RegexpParser
import nltk
from nltk.stem import WordNetLemmatizer
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s:[%(filename)s:%(lineno)d] - %(message)s [%(asctime)s]',
                    datefmt='%H:%M:%S')

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

wordnet_lemmatizer = WordNetLemmatizer()

noun_list_final, verb_list_final, verb_noun_rel_dict, verb_token_list, noun_token_list = get_data()


def user_input(inp):
    answer, score = genResults(inp, getBertAnswer)

    if score > 0.65:
        LOGGER.info(f'The user query score is above the threshold of 0.65, so returning answer from the in-domain'
                    f'model for this user query')
        return answer
    else:
        LOGGER.info(f'The user query score for the current question is below the threshold of 0.65, so returning answer'
                    f' from the out-domain model for this query')

        text = inp[0].split()
        tokens_tag = pos_tag(text)
        pos_dict = {}
        pos_tagging(tokens_tag, pos_dict)
        LOGGER.debug(f'The pos dict for the user is {pos_dict}')
        keysList = list(pos_dict.keys())
        count_noun = 0
        count_noun_match = 0
        count_verb = 0
        count_verb_match = 0
        noun_list = []
        verb_list = []
        # print("**")
        for keys in keysList:
            if keys.startswith("N"):
                noun_list += pos_dict.get(keys)
            if keys.startswith("V"):
                verb_list += pos_dict.get(keys)

        for nouns in noun_list:
            if nouns in noun_list_final:
                count_noun_match += 1
            count_noun += 1

        count_noun_percent = 0
        count_verb_percent = 0
        if count_noun_match != 0 and count_noun != 0:
            count_noun_percent = count_noun_match / count_noun
            LOGGER.debug(f'Noun match percent is {count_noun_percent}')

        for verbs in verb_list:
            if verbs in verb_list_final:
                count_verb_match += 1
            count_verb += 1

        if count_verb_match != 0 and count_verb != 0:
            count_verb_percent = count_verb_match / count_verb
            LOGGER.debug(f'Count verb percent is {count_verb_percent}')

        if count_verb_percent >= 0.5 and count_noun_percent >= 0.5:
            temp_verb = ''
            temp_noun = ''
            for item in tokens_tag:
                if item[1] in verb_token_list:
                    temp_verb = wordnet_lemmatizer.lemmatize(item[0].lower())
                    LOGGER.debug(f'The temp verb is {temp_verb}')
                if item[1] in noun_token_list:
                    temp_noun = wordnet_lemmatizer.lemmatize(item[0].lower())
                    LOGGER.debug(f'The temp noun is {temp_noun}')
                    if temp_verb in verb_noun_rel_dict.keys():
                        temp_noun_list = verb_noun_rel_dict.get(temp_verb)
                        if temp_noun in temp_noun_list:
                            answer_returned = answer_gpt3(inp)
                            return answer_returned

        else:
            return "Sorry !! I can't answer that"

# user_input(test_data)
