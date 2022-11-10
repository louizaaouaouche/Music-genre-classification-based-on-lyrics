import lyricsgenius
import pandas as pd
import sys
import progressbar


def get_lyrics(token):

    genius = lyricsgenius.Genius(token, timeout=400)

    genius.verbose = False  # Turn off status messages
    # Remove section headers (e.g. [Chorus]) from lyrics when searching
    genius.remove_section_headers = True
    # Include hits thought to be non-songs (e.g. track lists)
    genius.skip_non_songs = False
    # Exclude songs with these words in their title
    genius.excluded_terms = ["(Live)"]

    data = []
    genres = ['country']

    k = 1
    widgets = ['Getting lyrics: ', progressbar.Percentage(), ' ',
                progressbar.Bar(marker='=',left='[',right=']'),
                ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
    bar = progressbar.ProgressBar(widgets=widgets, maxval=len(genres)*1000)
    bar.start()

    for genre in genres:
        page = 1
        while page:
            res = genius.tag(genre, page=page)
            for hit in res['hits']:
                bar.update(k)
                song_lyrics = genius.lyrics(song_url=hit['url'])
                data.append([hit['artists'][0], hit['title'],
                            song_lyrics, genre, hit['url']])
                k += 1
            page = res['next_page']

    df = pd.DataFrame(
        data, columns=['artist', 'title', 'lyrics', 'genre', 'url'])
    df.to_csv('countryLyrics.csv', index=False, sep='#')

    bar.finish()


if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print("Usage: python3 geniusScrapping.py <token>")
        exit(1)
    get_lyrics(sys.argv[1])
    exit(1)
