import logging

from nltk import pos_tag
from nltk.stem import WordNetLemmatizer

from src.indomain.sbert_model import genResults, getBertAnswer
from src.outdomain.gpt3_model import answer_gpt3
from src.outdomain.ner_pos import get_data, pos_tagging
from src.outdomain.outdoor_activity import current_response, get_question_type

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
            f"The user query score is above the threshold of 0.65, so returning answer"
            f" from the in-domainmodel for this user query"
        )
        LOGGER.debug(
            "The score of the closest question to the user query in the in-domain "
            f"dataset is {score}"
        )
        LOGGER.debug(
            "The closest matched question to the user query in the in-domain "
            f"dataset is `{answer}`"
        )
        return answer
    else:
        LOGGER.info(
            f"The user query score for the current question is below the threshold of"
            f" 0.65, so returning answer from the out-domain model for this query"
        )

        text = inp[0].split()
        tokens_tag = pos_tag(text)
        pos_dict = {}
        pos_tagging(tokens_tag, pos_dict)
        LOGGER.debug(f"The pos dict for the user is {pos_dict}")
        keysList = list(pos_dict.keys())
        LOGGER.debug(f"Distinct POS tags for the user query are {keysList}")
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
            LOGGER.debug(f"Noun match percent is {count_noun_percent}")

        for verbs in verb_list:
            if verbs in verb_list_final:
                count_verb_match += 1
            count_verb += 1

        if count_verb_match != 0 and count_verb != 0:
            count_verb_percent = count_verb_match / count_verb
            LOGGER.debug(f"Count verb percent is {count_verb_percent}")

        LOGGER.debug(
            f"Checking if the user query has the verb noun pair present in the master"
            f" verb-noun list"
        )
        if count_verb_percent >= 0.5 and count_noun_percent >= 0.5:
            temp_verb_list = []
            temp_noun_list = []
            for item in tokens_tag:
                if item[1] in verb_token_list:
                    temp_verb_list.append(
                        wordnet_lemmatizer.lemmatize(item[0].lower())
                    )  # todo: add append instead of replace in the tempverb and tempnoun pair
                    LOGGER.debug(f"The temp verb is {temp_verb_list}")

                if item[1] in noun_token_list:
                    temp_noun_list.append(wordnet_lemmatizer.lemmatize(item[0].lower()))
                    LOGGER.debug(f"The temp noun is {temp_noun_list}")

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
                f"The user query matches neither the in-domain nor the out-domain model"
                f" criteria to fetch ananswer. Exiting with the default template"
                f" message."
            )
            return "Hey there. Sorry, I can't quite answer that."
