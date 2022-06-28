from socketIO_client import SocketIO, LoggingNamespace
import socketio
sio = socketio.Client()

# def receivedMessage(args):
#     print('Bot: ', args)

socketIO = SocketIO('localhost', 8000, LoggingNamespace)
# socketIO.on('message', receivedMessage)
print("User: "+"Who are you??")
socketIO.emit('message',"Who are you?")
# # socketIO.wait(seconds=5)   
print("User: "+"What is the meaning of Juli name?")
socketIO.emit('message',"What is the meaning of Juli name?")
# # socketIO.wait(seconds=1)   
print("User: "+"How many members are there in Juli?")
socketIO.emit('message',"How many members are there in Juli?")
# # socketIO.wait(seconds=1)   
# print("User: "+"Can I get health recommendation from Juli?")
# socketIO.emit('message',"Can I get health recommendation from Juli??")
# # socketIO.wait(seconds=1)   