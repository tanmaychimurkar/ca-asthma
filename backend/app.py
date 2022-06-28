from flask import Flask, render_template
from flask_socketio import SocketIO, emit
# from In_out_DomainClassification import user_input
# from fa_chat_close import genResults
# from fa_chat_close import getBertAnswer


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('connect')
def test_connect():
    print("Connected")

@socketio.on('message')
def test_connect(data):
    print("Welcome, messages received")
    print(data)
    return_data=""
    if data == "Who are you?":
        return_data = "We are Juli"
    if data == "How many members are there in Juli?":
        return_data = "There are currently 1000 members in Juli"
    # else:
    #     return_data = user_input(data)
    print("Bot: ", return_data)
    emit('message', "return_data")

@socketio.on('disconnect')
def test_disconnect(): 
    print('Client disconnected')

if __name__ == '__main__':
    app.run(port=8000)
