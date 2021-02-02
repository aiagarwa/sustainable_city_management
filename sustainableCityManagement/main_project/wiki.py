import wikipedia
import random

def WikiDetails(Input):
    try:
        Summary = wikipedia.summary(Input, sentences = 1)
    except wikipedia.DisambiguationError as e:
        randPage = random.choice(e.options)
        Summary = wikipedia.summary(randPage, sentences = 1)
    return(Summary)
