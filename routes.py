from flask import Flask, render_template, request, session
from forms import SpotPlay
import requests, os


####
from configparser import ConfigParser

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

import pygsheets
import pandas as pd
####


app = Flask(__name__)
app.secret_key = "TEST"


@app.route('/', methods=['GET', 'POST'] )
def index():
    form = SpotPlay()
    return render_template('index.html', form=form)



###########
@app.route('/runprogram', methods=['GET', 'POST'] )
def runprogram():

    def store_tracks(tracks):
        lst = []
        # global lst
        cols = ['track name', 'artist', 'date added']
        for i, item in enumerate(tracks['items']):
            date_time = item['added_at']
            track = item['track']
            lst.append([track['name'], track['artists'][0]['name'], date_time])
        playlist_length = len(lst)
        if playlist_length != 0 and playlist_length == (last_row - 1):
            pass
        elif last_row == 1:
            df = pd.DataFrame(lst, columns=cols)
            sh = gc.open('Introductions to Each Other')
            wks = sh[0]
            wks.set_dataframe(df,(1,1))
        else:
            del lst[0:(last_row - 1)]
            df = pd.DataFrame(lst, columns=cols)
            sh = gc.open('Introductions to Each Other')
            wks = sh[0]
            wks.set_dataframe(df,((last_row + 1),1))
            wks.delete_rows((last_row + 1),number=1)


    form = SpotPlay()
    parser = ConfigParser()
    parser.read('dev.ini')

    clientid = parser.get('settings', 'client_id')
    clientsecret = parser.get('settings', 'client_secret')
    usern = parser.get('settings', 'username')
    playlistid = parser.get('settings', 'playlist_id')

    #authorization
    gc = pygsheets.authorize(service_file='client_secret.json')

    # Spotify credentials
    client_credentials_manager = SpotifyClientCredentials(client_id=clientid, client_secret=clientsecret )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Spotify username and playlist
    username = usern
    playlist_id = playlistid

    # gets length of spreadsheet
    sh = gc.open('Introductions to Each Other')
    wks = sh[0]
    all_vals = wks.get_all_values()
    last_row = len(all_vals)

    # gets the specified playlist
    playlists = sp.user_playlists(username)
    # lst = []
    for playlist in playlists['items']:
        if playlist['id'] == playlist_id:
            results = sp.user_playlist(username, playlist_id, fields="tracks,next")
            tracks = results['tracks']
            store_tracks(tracks)
            while tracks['next']:
                tracks = sp.next(tracks)
                store_tracks(tracks)






    return render_template('index.html', form=form)



if __name__ == "__main__":
  app.run(debug=False)
