import requests
import api_key
import lyricsgenius
import re
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import spacy



client_access_token = api_key.client_access_token
LyricsGenius = lyricsgenius.Genius(client_access_token)

nlp = spacy.load("en_core_web_md")

artist = "Taylor Swift"

artist = LyricsGenius.search_artist(artist, max_songs=30)

lyrics = ""
for song in artist.songs:
    lyrics += song.lyrics + "\n" 

def remove_brackets(text):
    pattern = re.compile(r'\[.*?\]')
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

# Collect lyrics
lyrics = ""
for song in artist.songs:
    lyrics += remove_brackets(song.lyrics) + "\n"

# Tokenize and preprocess the lyrics data
tokenizer = Tokenizer()
tokenizer.fit_on_texts([lyrics])
total_words = len(tokenizer.word_index) + 1

input_sequences = []
token_list = tokenizer.texts_to_sequences([lyrics])[0]
for i in range(1, len(token_list)):
    n_gram_sequence = token_list[:i+1]
    input_sequences.append(n_gram_sequence)

max_sequence_length = max([len(x) for x in input_sequences])
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_length, padding='pre')

X, y = input_sequences[:, :-1], input_sequences[:, -1]
y = tf.keras.utils.to_categorical(y, num_classes=total_words)

# Build a simple LSTM model
model = Sequential()
model.add(Embedding(total_words, 50, input_length=max_sequence_length-1))
model.add(Bidirectional(LSTM(100, return_sequences=True)))
model.add(Bidirectional(LSTM(100, return_sequences=True)))
model.add(Bidirectional(LSTM(100)))
model.add(Dense(total_words, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


# Train for more epochs
more_epochs = 10
for epoch in range(more_epochs):
    print(f"Epoch {epoch + 1}/{more_epochs}")
    model.fit(X, y, epochs=1, verbose=1)
    
    # Generate lyrics at each epoch
    seed_text = "love"
    next_words = 50

    generated_lyrics = seed_text
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_length-1, padding='pre')
        predicted = np.argmax(model.predict(token_list, verbose=0))
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
        generated_lyrics += " " + output_word

    print(generated_lyrics)
