import os
import pickle

import pandas as pd
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()

current_path = os.path.dirname(os.path.abspath(__file__))


df = pd.read_csv(current_path + "/../../model_checkpoints/nerList.csv")
df1 = pd.read_csv(current_path + "/../../model_checkpoints/Asthma-QA.csv")
verb_token_list = ["VB", "VBG", "VBD", "VBN", "VBP", "VBZ"]
noun_token_list = ["NN", "NNS", "NNP", "NNPS"]


def pos_tagging(tokens_tag, pos_dict):
    for item in tokens_tag:
        if item[1] in pos_dict.keys():
            val_list = pos_dict.get(item[1])
            val_list.append(item[0])
        else:
            temp_list = [item[0]]
            pos_dict[item[1]] = temp_list


def find_vn_relation(tokens_tag):
    temp_verb = ""
    temp_noun = ""
    for item in tokens_tag:
        if item[1] in verb_token_list and item[1] != "" and item[1] is not None:
            temp_verb = wordnet_lemmatizer.lemmatize(item[0].lower())
        if item[1] in noun_token_list:
            temp_noun = wordnet_lemmatizer.lemmatize(item[0].lower())
            # print(temp_verb,'->', temp_noun)
            if temp_verb != "" and temp_verb is not None:
                # print(temp_verb)
                if temp_noun != "" and temp_noun is not None:
                    # print(temp_noun)
                    if temp_verb in verb_noun_rel_dict.keys():
                        val_list = verb_noun_rel_dict.get(temp_verb)
                        # print(val_list)
                        # print(temp_verb,'->', temp_noun)
                        val_list.append(temp_noun)
                    else:
                        temp_list = [temp_noun]
                        verb_noun_rel_dict[temp_verb] = temp_list


# for index, row in df.iterrows():
#     row['selftext'] = row['selftext'].translate(str.maketrans('', '', string.punctuation))
#     text = row['selftext'].split()
#     tokens_tag = pos_tag(text)
#     find_vn_relation(tokens_tag)
#     pos_tagging(tokens_tag, pos_dict)
#
# for index, row in df1.iterrows():
#     row['Question'] = row['Question'].translate(str.maketrans('', '', string.punctuation))
#     text = row['Question'].split()
#     tokens_tag = pos_tag(text)
#     find_vn_relation(tokens_tag)
#     pos_tagging(tokens_tag, pos_dict)


# with open('model_objects/pos_dict_new.pkl', 'wb') as f:
#     # pos_dict = pickle.load(f)
#     pickle.dump(pos_dict, f)
#
# with open('model_objects/verb_noun_relation_dict_new.pkl', 'wb') as f:
#     pickle.dump(verb_noun_rel_dict, f)


with open(current_path + "/../../model_checkpoints/pos_dict_new.pkl", "rb") as f:
    pos_dict = pickle.load(f)

with open(
    current_path + "/../../model_checkpoints/verb_noun_relation_dict.pkl", "rb"
) as f:
    verb_noun_rel_dict = pickle.load(f)

noun_list = (
    pos_dict.get("NN")
    + pos_dict.get("NNS")
    + pos_dict.get("NNP")
    + pos_dict.get("NNPS")
)

verb_list = (
    pos_dict.get("VB")
    + pos_dict.get("VBG")
    + pos_dict.get("VBD")
    + pos_dict.get("VBN")
    + pos_dict.get("VBP")
    + pos_dict.get("VBZ")
)


def get_data():
    noun_list_final = set(noun_list)
    verb_list_final = set(verb_list)
    return (
        noun_list_final,
        verb_list_final,
        verb_noun_rel_dict,
        verb_token_list,
        noun_token_list,
    )
