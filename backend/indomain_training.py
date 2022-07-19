import pandas as pd

data = pd.read_csv('fe_chat_full.csv')
print(type(data))
data.drop(columns=['No', 'MVP'], inplace=True)
data.dropna(inplace=True)

data.to_csv('fe_chat.csv', index=False)

from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')


def encode_questions():
    bc = model
    questions = data["Questions"].values.tolist()
    print("Questions count", len(questions))
    print("Start to calculate encoder....")
    questions_encoder = bc.encode(questions)
    np.save("questions_new", questions_encoder)
    questions_encoder_len = np.sqrt(
        np.sum(questions_encoder * questions_encoder, axis=1)
    )
    np.save("questions_len_new", questions_encoder_len)
    print("Encoder ready")

print('beginning training')
encode_questions()
print('ending training')
