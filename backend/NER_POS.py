import pandas as pd
import pickle
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()

df = pd.read_csv("nerList.csv")

# pos_dict = {}
# verb_noun_rel_dict = {}
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
    temp_verb = ''
    temp_noun = ''
    for item in tokens_tag:
        if item[1] in verb_token_list and item[1] != '' and item[1] is not None:
            temp_verb = wordnet_lemmatizer.lemmatize(item[0].lower())
        if item[1] in noun_token_list:
            temp_noun = wordnet_lemmatizer.lemmatize(item[0].lower())
            # print(temp_verb,'->', temp_noun)
            if temp_verb != '' and temp_verb is not None:
                # print(temp_verb)
                if temp_noun != '' and temp_noun is not None:
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
#     text = row['selftext'].split()
#     text_lemmatized = [wordnet_lemmatizer.lemmatize(w) for w in text]
#     tokens_tag = pos_tag(text_lemmatized)
#     find_vn_relation(tokens_tag)
#     pos_tagging(tokens_tag, pos_dict)


with open('model_objects/pos_dict.pkl', 'rb') as f:
    pos_dict = pickle.load(f)

with open('model_objects/verb_noun_relation_dict.pkl', 'rb') as f:
    verb_noun_rel_dict = pickle.load(f)

noun_list = pos_dict.get('NN') + pos_dict.get('NNS') + pos_dict.get('NNP') + pos_dict.get('NNPS')

verb_list = pos_dict.get('VB') + pos_dict.get('VBG') + pos_dict.get('VBD') + pos_dict.get('VBN') + pos_dict.get(
    'VBP') + pos_dict.get('VBZ')


def get_data():
    noun_list_final = set(noun_list)
    verb_list_final = set(verb_list)
    return noun_list_final, verb_list_final, verb_noun_rel_dict, verb_token_list, noun_token_list
