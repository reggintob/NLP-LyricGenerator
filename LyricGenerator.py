import requests
import lyricsgenius
import re
import spacy
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
import api_key
import random
import nltk
from nltk.corpus import cmudict

# spacy.cli.download("en_core_web_md")
client_access_token = api_key.client_access_token

LyricsGenius = lyricsgenius.Genius(client_access_token)

nlp = spacy.load("en_core_web_md")

artist = LyricsGenius.search_artist("Taylor swift", max_songs=20)

lyrics = ""
for song in artist.songs:
    lyrics += song.lyrics + "\n" 

def remove_brackets(input_string):

    square_brackets_pattern = re.compile(r'\[.*?\]')

    
    parentheses_pattern = re.compile(r'\([^)]*\)')

    output_string = re.sub(square_brackets_pattern, '', input_string)

    output_string = re.sub(parentheses_pattern, '', output_string)

    output_string = ' '.join(output_string.split())

    return output_string

result_text = remove_brackets(lyrics)

tokens = word_tokenize(result_text)

artist = input()
title = input()

mahesh = LyricsGenius.search_song(title, artist)
ramesh = mahesh.lyrics

ganesh = remove_brackets(ramesh)
suresh = word_tokenize(ganesh)
length = len(suresh)


pronouncing_dict = cmudict.dict()


def count_syllables(word):
    if word in pronouncing_dict:
        return max([len(list(y for y in x if y[-1].isdigit())) for x in pronouncing_dict[word]])
    else:
        return 0

def build_markov_model(corpus, order=2):
    markov_model = {}
    for i in range(len(corpus) - order):
        context = tuple(corpus[i:i + order])
        next_word = corpus[i + order]
        if context in markov_model:
            markov_model[context].append(next_word)
        else:
            markov_model[context] = [next_word]
    return markov_model

markov_model = build_markov_model(tokens, order=3)
def generate_poetry(markov_model, length):
    poetry = []
    for i in suresh:
        line = []
        context = random.choice(list(markov_model.keys()))
            
        if context in markov_model:
            for _ in range(1):  # Add a limit to the number of attempts to avoid infinite loop
                next_word = random.choice(markov_model[context])

                line_syllables = count_syllables(' '.join(line))
                next_word_syllables = count_syllables(next_word)

                if line_syllables + next_word_syllables <= length:
                    line.append(next_word)
                    context = tuple(list(context[1:]) + [next_word])
                else:
                    break
            poetry.extend(line)

    return ' '.join(poetry)
    
generated_poetry = generate_poetry(markov_model,length)
print(generated_poetry)
