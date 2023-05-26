import logging
import os

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:[%(filename)s:%(lineno)d] - %(message)s [%(asctime)s]",
    datefmt="%H:%M:%S",
)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

current_path = os.path.dirname(os.path.abspath(__file__))
model = SentenceTransformer("all-mpnet-base-v2", cache_folder='./cache')
question_embedding = np.load(current_path + "/../../model_checkpoints/question_emb.npy")
question_embedding_length = np.load(
    current_path + "/../../model_checkpoints/question_len_embedding.npy"
)

data = pd.read_csv(current_path + "/../../model_checkpoints/fe_chat.csv")
data.fillna("placeholder for answers", inplace=True)
LOGGER.debug(f"Successfully loaded all model and data objects")


def genResults(questions, fn):
    def genresult(q):
        answer, score, prediction = fn(q)
        return [q, prediction, answer, score]

    result_df = pd.DataFrame(
        list(map(genresult, questions)),
        columns=["question", "question_closest", "answer", "score"],
    )
    LOGGER.debug(
        "The score of the closest question to the user query in the in-domain "
        f"dataset is {result_df['score'].values[0]}"
    )
    LOGGER.debug(
        "The closest matched question to the user query in the in-domain "
        f"dataset is `{result_df['question_closest'].values[0]}`"
    )
    return result_df["answer"].values[0], result_df["score"].values[0]


# def encode_questions():
#     bc = model
#     questions = data["Questions"].values.tolist()
#     print("Questions count", len(questions))
#     print("Start to calculate encoder....")
#     questions_encoder = bc.encode(questions)
#     np.save("v2tanmay_question_emb", questions_encoder)
#     questions_encoder_len = np.sqrt(
#         np.sum(questions_encoder * questions_encoder, axis=1)
#     )
#     np.save("v2tanmay_question_len_embedding", questions_encoder_len)
#     return questions_encoder, questions_encoder_len
#     print("Encoder ready")


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


# genResults('Who is Juli?', getBertAnswer)
