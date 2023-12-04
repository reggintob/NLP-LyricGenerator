import requests
import api_key
import lyricsgenius

def remove_brackets(text):

    pattern = re.compile(r'\[.*?\]')

    cleaned_text = re.sub(pattern, '', text)

    return cleaned_text

client_access_token = api_key.client_access_token

LyricsGenius = lyricsgenius.Genius(client_access_token)

artist = input()
title = input()

song = LyricsGenius.search_song(title, artist)

lyrics = song.lyrics

result_text = remove_brackets(lyrics)

print(result_text)

