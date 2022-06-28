


import pandas as pd
data = pd.read_csv('fe_chat.csv')
# data.drop(columns=['No'], inplace=True)
data.dropna(inplace=True)
data


test_data = [
    "What is the meaning of juli name",
    "Can I speak to someone at juli?",
    "Who is behind juli?",
    "Who is juli"
]


# master fn for getting answers to questions

def genResults(questions, fn):
    def genresult(q):
        answer, score, prediction = fn(q)
        return [q, prediction, answer, score]
    result_df = pd.DataFrame(list(map(genresult, questions)), columns=['question', 'question_closest', 'answer', 'score'])
    return result_df['answer'].values


# ## Bert QA system


from sentence_transformers import SentenceTransformer
import numpy as np
model = SentenceTransformer('all-MiniLM-L6-v2')

# def encode_questions():
#     bc = model
#     questions = data["Questions"].values.tolist()
#     print("Questions count", len(questions))
#     print("Start to calculate encoder....")
#     questions_encoder = bc.encode(questions)
#     np.save("questions", questions_encoder)
#     questions_encoder_len = np.sqrt(
#         np.sum(questions_encoder * questions_encoder, axis=1)
#     )
#     np.save("questions_len", questions_encoder_len)
#     print("Encoder ready")

# encode_questions()



import numpy as np

class BertAnswer():
    def __init__(self):
        self.bc = model
        self.q_data = data["Questions"].values.tolist()
        self.a_data = data["Answers"].values.tolist()
        self.questions_encoder = np.load("questions.npy")
        self.questions_encoder_len = np.load("questions_len.npy")

    def get(self, q):
        query_vector = self.bc.encode([q])[0]
        score = np.sum((query_vector * self.questions_encoder), axis=1) / (
            self.questions_encoder_len * (np.sum(query_vector * query_vector) ** 0.5)
        )
        top_id = np.argsort(score)[::-1][0]
        # if float(score[top_id]) > 0.94:
        #     return self.a_data[top_id], score[top_id], self.q_data[top_id]
        # return "Sorry, I didn't get you.", score[top_id], self.q_data[top_id]
        return self.a_data[top_id], score[top_id], self.q_data[top_id]

bm = BertAnswer()

def getBertAnswer(q):
    return bm.get(q)

genResults([test_data[0]], getBertAnswer)


# bert approach and lrvensthein distance method both seem to be good, present results to Andy


