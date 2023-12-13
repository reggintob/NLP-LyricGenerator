import requests
import api_key
import lyricsgenius
import re
import spacy

client_access_token = api_key.client_access_token
LyricsGenius = lyricsgenius.Genius(client_access_token)

nlp = spacy.load("en_core_web_md")

artist = LyricsGenius.search_artist("Kanye West", max_songs=5)

lyrics = ""
for song in artist.songs:
    lyrics += song.lyrics + "\n" 

def remove_brackets(text):

    pattern = re.compile(r'\[.*?\]')

    cleaned_text = re.sub(pattern, '', text)

    return cleaned_text

result_text = remove_brackets(lyrics)

# print(result_text)

doc = nlp(lyrics)

word_vectors = [token.vector for token in doc if token.is_alpha]
