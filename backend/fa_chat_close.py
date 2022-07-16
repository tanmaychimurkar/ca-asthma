import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s:[%(filename)s:%(lineno)d] - %(message)s [%(asctime)s]',
                    datefmt='%H:%M:%S')

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

model = SentenceTransformer('all-mpnet-base-v2')
question_embedding = np.load("model_objects/question_emb.npy")
question_embedding_length = np.load("model_objects/question_len_embedding.npy")
data = pd.read_csv('fe_chat_full.csv')
data.drop(columns=['No'], inplace=True)
data.drop('MVP', axis=1, inplace=True)
data.fillna('placeholder for answers', inplace=True)


def genResults(questions, fn):
    def genresult(q):
        answer, score, prediction = fn(q)
        return [q, prediction, answer, score]

    result_df = pd.DataFrame(list(map(genresult, questions)),
                             columns=['question', 'question_closest', 'answer', 'score'])
    LOGGER.info(f'The score of the closest question to the user query in the in-domain '
                f'dataset is {result_df["score"].values[0]}')
    LOGGER.info(f'The closest matched question to the user query in the in-domain '
                f'dataset is `{result_df["question_closest"].values[0]}`')
    return result_df['answer'].values[0], result_df['score'].values[0]


def generate_results(question):
    answer, score, prediction = 'test', 'test', 'test'
    pass


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


class BertAnswer:
    def __init__(self):
        self.bc = model
        self.q_data = data["Questions"].values.tolist()
        self.a_data = data["Answers"].values.tolist()
        self.questions_encoder = question_embedding
        self.questions_encoder_len = question_embedding_length

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
