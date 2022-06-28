#!/usr/bin/env python
# coding: utf-8

# In[10]:


import pandas as pd
import numpy as np
from nltk import pos_tag
from nltk import RegexpParser
import nltk
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()


# In[4]:


df = pd.read_csv("nerList.csv")


# In[5]:


df


# In[ ]:





# In[76]:


pos_dict = {}
verb_noun_rel_dict = {}
verb_token_list = ["VB", "VBG", "VBD", "VBN", "VBP", "VBZ"]
noun_token_list = ["NN", "NNS", "NNP", "NNPS"]

def pos_tagging(tokens_tag, pos_dict):
    for item in tokens_tag:
        if item[1] in pos_dict.keys():
            val_list = pos_dict.get(item[1])
            val_list.append(item[0])
        else:
            temp_list = []
            temp_list.append(item[0])
            pos_dict[item[1]] = temp_list

def find_vn_relation(tokens_tag):
    temp_verb = ''
    temp_noun = ''
    for item in tokens_tag:
        if item[1] in verb_token_list:
            temp_verb = wordnet_lemmatizer.lemmatize(item[0].lower())
        if item[1] in noun_token_list:
            temp_noun = wordnet_lemmatizer.lemmatize(item[0].lower())
            # print(temp_verb,'->', temp_noun)
            if temp_verb != '' and temp_verb != None:
                # print(temp_verb)
                if temp_noun!='' and temp_noun!=None:
                    # print(temp_noun)
                    if temp_verb in verb_noun_rel_dict.keys():
                        val_list = verb_noun_rel_dict.get(temp_verb)
                        # print(val_list)
                        # print(temp_verb,'->', temp_noun)
                        val_list.append(temp_noun)
                    else:
                        temp_list = []
                        temp_list.append(temp_noun)
                        verb_noun_rel_dict[temp_verb] = temp_list
                        # if temp_verb == 'severe':
                        #     print("its here")
                        #     print(temp_noun)
                        #     print("aaa")
                        #     print(verb_noun_rel_dict['severe'])
                        #     break

for index, row in df.iterrows():
    text = row['selftext'].split()
    tokens_tag = pos_tag(text)
    find_vn_relation(tokens_tag)
    pos_tagging(tokens_tag, pos_dict)




# In[77]:


# print(pos_dict)


# In[ ]:





# In[24]:


# pos_dict = {}
# for item in tokens_tag:
#     if item[1] in pos_dict.keys():
#         val_list = pos_dict.get(item[1])
#         val_list.append(item[0])
#     else:
#         temp_list = []
#         temp_list.append(item[0])
#         pos_dict[item[1]] = temp_list


# 
# should include - NN, NNS, NNP, NNPS, VB, VBG, VBD, VBN, VBP, VBZ

# In[88]:


noun_list = []
verb_list = []


# In[89]:


noun_list = pos_dict.get('NN')+pos_dict.get('NNS')+pos_dict.get('NNP')+pos_dict.get('NNPS')


# In[90]:


# print(noun_list)


# In[92]:


verb_list = pos_dict.get('VB') + pos_dict.get('VBG') + pos_dict.get('VBD') + pos_dict.get('VBN') + pos_dict.get('VBP') + pos_dict.get('VBZ')
# verb_list = pos_dict.get('VBG'))
# verb_list.append(pos_dict.get('VBD'))
# verb_list.append(pos_dict.get('VBN'))
# verb_list.append(pos_dict.get('VBP'))
# verb_list.append(pos_dict.get('VBZ'))


# In[83]:


# print(noun_list)


# In[84]:


# print(verb_list)


# In[91]:


pd.Series(noun_list).value_counts()



from collections import Counter
counts = Counter(noun_list)
# print(counts)


# ## Compare Noun and verb separately.

def get_data():
	noun_list_final = set(noun_list)
	verb_list_final = set(verb_list)
	return noun_list_final,verb_list_final, verb_noun_rel_dict
