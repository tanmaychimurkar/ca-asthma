import json
from flask import Flask, request
from In_out_DomainClassification import user_input

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello Juli!'


@app.route('/api/v1/answer', methods=['POST'])
def get_gpt3_answer():
    record = json.loads(request.data)
    print(record['answer']['question'])
    inp = [record['answer']['question']]
    answer_returned = user_input(inp)
    print(answer_returned)
    return answer_returned, 200


if __name__ == '__main__':
    app.run(port=8452, debug=True)
