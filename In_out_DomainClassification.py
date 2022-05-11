from fa_chat_close import genResults
from fa_chat_close import getBertAnswer

# test_data = ['Who is behind juli?']
# test_data = ['Are there doctors in the Juli team?'] #0.8487
# test_data = ['Can we eat Juli?'] #0.5573
test_data = ['Can we smoke during asthma?'] #0.5828
# test_data = ['Do you sell our data?'] # Is my data secure? 0.6194
# test_data = ['Do you sell our data?']
# test_data = ['Who is behind juli?']


answer, score = genResults(test_data, getBertAnswer)
print(answer+ "--->with the score of: " +str(score) )

if score>0.65:
    print(answer)
else:
    print("Redirecting to the out of domain model")
