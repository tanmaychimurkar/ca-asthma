import logging

from nltk import pos_tag
from nltk.stem import WordNetLemmatizer

from NER_POS import get_data
from NER_POS import pos_tagging
from engine.fa_chat_close import genResults
from engine.fa_chat_close import getBertAnswer
from gpt3 import answer_gpt3
from outdoor_activity import get_question_type, current_response

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:[%(filename)s:%(lineno)d] - %(message)s [%(asctime)s]",
    datefmt="%H:%M:%S",
)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

wordnet_lemmatizer = WordNetLemmatizer()

(
    noun_list_final,
    verb_list_final,
    verb_noun_rel_dict,
    verb_token_list,
    noun_token_list,
) = get_data()


def user_input(inp, model_flag=0):
    activity_type = get_question_type(inp[0])
    if activity_type == "current time":
        return current_response()
    answer, score = genResults(inp, getBertAnswer)

    if score > 0.65:
        LOGGER.info(
            f"The user query score is above the threshold of 0.65, so returning answer from the in-domain"
            f"model for this user query"
        )
        LOGGER.debug(
            f"The score of the closest question to the user query in the in-domain "
            f"dataset is {score}"
        )
        LOGGER.debug(
            f"The closest matched question to the user query in the in-domain "
            f"dataset is `{answer}`"
        )
        return answer
    else:
        LOGGER.info(
            f"The user query score for the current question is below the threshold of 0.65, so returning answer"
            f" from the out-domain model for this query"
        )

        text = inp[0].split()
        tokens_tag = pos_tag(text)
        pos_dict = {}
        pos_tagging(tokens_tag, pos_dict)
        LOGGER.debug(f"The pos dict for the user is {pos_dict}")
        keysList = list(pos_dict.keys())
        LOGGER.debug(f"Distinct POS tags for the user query are {keysList}")
        # todo: remove special characters from the user query, and retrain the pickle files
        count_noun = 0
        count_noun_match = 0
        count_verb = 0
        count_verb_match = 0
        noun_list = []
        verb_list = []

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
            LOGGER.info(f"Noun match percent is {count_noun_percent}")

        for verbs in verb_list:
            if verbs in verb_list_final:
                count_verb_match += 1
            count_verb += 1

        if count_verb_match != 0 and count_verb != 0:
            count_verb_percent = count_verb_match / count_verb
            LOGGER.debug(f"Count verb percent is {count_verb_percent}")

        LOGGER.info(
            f"Checking if the user query has the verb noun pair present in the master verb-noun list"
        )
        if count_verb_percent >= 0.5 and count_noun_percent >= 0.5:
            temp_verb_list = []
            temp_noun_list = []
            for item in tokens_tag:
                if item[1] in verb_token_list:
                    temp_verb_list.append(
                        wordnet_lemmatizer.lemmatize(item[0].lower())
                    )  # todo: add append instead of replace in the tempverb and tempnoun pair
                    LOGGER.info(f"The temp verb is {temp_verb_list}")

                if item[1] in noun_token_list:
                    temp_noun_list.append(wordnet_lemmatizer.lemmatize(item[0].lower()))
                    LOGGER.info(f"The temp noun is {temp_noun_list}")

            for temp_verb in temp_verb_list:
                for temp_noun in temp_noun_list:
                    if temp_verb in verb_noun_rel_dict.keys():
                        temp_noun_list = verb_noun_rel_dict.get(temp_verb)
                        if temp_noun in temp_noun_list:
                            LOGGER.info(f"Getting the answer from the gpt3 API")
                            if model_flag == 0:
                                answer_returned = answer_gpt3(inp)
                            else:
                                answer_returned = answer_gpt3(inp, curie_flag=1)
                            return answer_returned

            return f"Hey there. Sorry, I can't quite answer that."

        else:
            LOGGER.info(
                f"The user query matches neither the in-domain nor the out-domain model criteria to fetch an"
                f"answer. Exiting with the default template message."
            )
            return "Hey there. Sorry, I can't quite answer that."
