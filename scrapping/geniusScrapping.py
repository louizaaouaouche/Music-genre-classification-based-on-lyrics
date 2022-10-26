import lyricsgenius
import pandas as pd

token = "tLsFmYYTavBNOqshrCO3VbGyyNoqw6lOTSndQP3JRnfWX7hceOzz0HzcdoAgOQUU"

genius = lyricsgenius.Genius(token, timeout=20)

genius.verbose = False  # Turn off status messages
# Remove section headers (e.g. [Chorus]) from lyrics when searching
genius.remove_section_headers = True
# Include hits thought to be non-songs (e.g. track lists)
genius.skip_non_songs = False
# Exclude songs with these words in their title
genius.excluded_terms = ["(Live)"]

data = []

genres = ['rap', 'hip-hop', 'country', 'rock', 'pop', 'r-b']
for genre in genres:
    page = 1
    print(genre)
    while page < 2:
        res = genius.tag(genre, page=page)
        for hit in res['hits']:
            song_lyrics = genius.lyrics(song_url=hit['url'])
            data.append([hit['artists'][0], hit['title'], song_lyrics, genre, hit['url']])
        page = res['next_page']


df = pd.DataFrame(data, columns=['artists', 'title', 'lyrics', 'genre', 'url'])

df.to_csv('lyrics_small.csv', index=False, sep='#')