from fa_chat_close import genResults
from fa_chat_close import getBertAnswer
from gpt3 import answer_gpt3
from NER_POS import get_data
from NER_POS import pos_tagging
from nltk import pos_tag
from nltk import RegexpParser
import nltk
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

# test_data = ['Who is behind juli?']
# test_data = ['Are there doctors in the Juli team?'] #0.8487
# test_data = ['Can we eat in Juli?'] #0.5573
# test_data = ['Can we smoke during asthma?'] #0.5828
# test_data = ['Do you sell our data?'] # Is my data secure? 0.6194
# test_data = ['Do you sell our data?']
# test_data = ['Who is behind juli?']

noun_list_final, verb_list_final,verb_noun_rel_dict = get_data()
# print(len(verb_noun_rel_dict))
# print(verb_noun_rel_dict['kick'])

verb_token_list = ["VB", "VBG", "VBD", "VBN", "VBP", "VBZ"]
noun_token_list = ["NN", "NNS", "NNP", "NNPS"]

def user_input(inp):
    answer, score = genResults(inp, getBertAnswer)
    # print(answer+ "--->with the score of: " +str(score) )
    print("The score is ", score)

    if score>0.65:
        # print(answer)
        return answer
    else:
        print(inp)
        text = inp[0].split()
        tokens_tag = pos_tag(text)
        pos_dict = {}
        pos_tagging(tokens_tag,pos_dict)
        print(pos_dict)
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

        # noun_list = pos_dict.get('NN')+pos_dict.get('NNS')+pos_dict.get('NNP')+pos_dict.get('NNPS')
        # verb_list = pos_dict.get('VB') + pos_dict.get('VBG') + pos_dict.get('VBD') + pos_dict.get('VBN') + pos_dict.get('VBP') + pos_dict.get('VBZ')
        # print(noun_list,verb_list)
        for nouns in noun_list:
            if nouns in noun_list_final:
                count_noun_match += 1
            count_noun += 1

        count_noun_percent = 0
        count_verb_percent = 0
        if count_noun_match != 0 and count_noun != 0:
            count_noun_percent = count_noun_match/count_noun
            print("Noun match percent is ", count_noun_percent)

        for verbs in verb_list:
            if verbs in verb_list_final:
                count_verb_match += 1
            count_verb += 1

        if count_verb_match != 0 and count_verb != 0:
            count_verb_percent = count_verb_match/count_verb
            print("Count verb percent is ", count_verb_percent )

        if count_verb_percent >= 0.5 and count_noun_percent >= 0.5:
            temp_verb = ''
            temp_noun = ''
            for item in tokens_tag:
                if item[1] in verb_token_list:
                    temp_verb = wordnet_lemmatizer.lemmatize(item[0].lower())
                    print(temp_verb)
                if item[1] in noun_token_list:
                    temp_noun = wordnet_lemmatizer.lemmatize(item[0].lower())
                    print(temp_noun)
                    if temp_verb in verb_noun_rel_dict.keys():
                        temp_noun_list = verb_noun_rel_dict.get(temp_verb)
                        print("*****nnnnaaa")
                        # print(temp_noun_list)
                        if temp_noun in temp_noun_list:
                            answer_returned = answer_gpt3(inp)
                            return answer_returned
                        
        # print(answer_returned)
            
        else:
            return("Sorry !! I can't answer that")


# user_input(test_data)
