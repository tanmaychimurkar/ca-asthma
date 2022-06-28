from In_out_DomainClassification import user_input
from fa_chat_close import genResults
from fa_chat_close import getBertAnswer
from gpt3 import append_interaction_to_chat_log

while(True):
    inp1 = input()
    if(inp1 == 'Quit' or inp1 == "quit"):
        break
    inp = []
    inp.append(inp1)
    answer_returned = user_input(inp)
    print(answer_returned)
    # append_interaction_to_chat_log(inp1,answer_returned,None)

   