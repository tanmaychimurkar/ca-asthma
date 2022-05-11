#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer
import numpy as np


data = pd.read_csv('fe_Chat_full.csv')
data.drop(columns=['No'], inplace=True)
data.drop('MVP', axis=1, inplace=True)
data.fillna('placeholder for answers', inplace=True)
#data

test_data = [
    "What is the meaning of juli name"]
#     "Can I speak to someone at juli?",
#     "Who is behind juli?",
#     "Who is juli"
# ]

# master fn for getting answers to questions

def genResults(questions, fn):
    def genresult(q):
        answer, score, prediction = fn(q)
        return [q, prediction, answer, score]
    result_df = pd.DataFrame(list(map(genresult, questions)), columns=['question', 'question_closest', 'answer', 'score'])
    return result_df['answer'].values, result_df['score'].values

def generate_results(question):
    answer, score, prediction = 'test','test','test'
    pass


# ## Bert QA system

model = SentenceTransformer('all-mpnet-base-v2')


# In[7]:


# def encode_questions():
#     bc = model
#     questions = data["Questions"].values.tolist()
#     print("Questions count", len(questions))
#     print("Start to calculate encoder....")
#     questions_encoder = bc.encode(questions)
#     np.save("question_emb", questions_encoder)
#     questions_encoder_len = np.sqrt(
#         np.sum(questions_encoder * questions_encoder, axis=1)
#     )
#     np.save("question_len_embedding", questions_encoder_len)
#     print("Encoder ready")

# encode_questions()


# In[24]:


class BertAnswer:
    def __init__(self):
        self.bc = model
        self.q_data = data["Questions"].values.tolist()
        self.a_data = data["Answers"].values.tolist()
        self.questions_encoder = np.load("question_emb.npy")
        self.questions_encoder_len = np.load("question_len_embedding.npy")

    def get(self, q):
        query_vector = self.bc.encode([q])[0]
        score = np.sum((query_vector * self.questions_encoder), axis=1) / (
            self.questions_encoder_len * (np.sum(query_vector * query_vector) ** 0.5)
        )
        top_id = np.argsort(score)[::-1][0]
        return self.a_data[top_id], score[top_id], self.q_data[top_id]

bm = BertAnswer()

def getBertAnswer(q):
    return bm.get(q)





