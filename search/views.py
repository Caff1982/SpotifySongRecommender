from django.shortcuts import render
from django.views.generic import ListView
from django.conf import settings

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from .forms import SearchForm


def home(request):
    form = SearchForm(request.POST or None)
    search_results = []

    if request.method == 'POST' and form.is_valid():
        song_title = form.cleaned_data['song_title']
        print('song_title: ', song_title)
        # Connect to Spotipy
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                                client_id=settings.SPOTIPY_CLIENT_ID,
                                client_secret=settings.SPOTIPY_CLIENT_SECRET))
        results = sp.search(q=song_title, type='track')
        
        for item in results['tracks']['items']:
            # Concatenate artist name and track name to display
            song_string = item['artists'][0]['name'] + ': ' + item['name']
            # Store track name and track ID as tuple for each song
            search_results.append((song_string, item['id']))

    context = {
        'form': form,
        'search_results': search_results,
    }

    return render(request, 'search/home.html', context)


def show_recommendations(request, track_id):
    # Connect to Spotipy
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                            client_id=settings.SPOTIPY_CLIENT_ID,
                            client_secret=settings.SPOTIPY_CLIENT_SECRET))
    # Get features for track
    track_features = sp.audio_features(track_id)[0]
    # Keep only the columns we need
    cols = ['energy', 'danceability',
        'speechiness', 'acousticness',
        'instrumentalness', 'liveness', 'valence']
    track_profile = [track_features[col] for col in cols]
    track_profile = np.array(track_profile).reshape(1, -1)
    # Load DataFrame to create item-profiles DataFrame
    df = pd.read_csv('./tracks.csv')
    df.drop(columns=['duration_ms', 'explicit', 'key',
                 'popularity', 'mode', 'release_date',
                 'tempo'], inplace=True)
    item_profiles = df[cols]
    # labels is a DataFrame matching item-profiles to trakc& artis names
    labels = df[['id', 'artists', 'name']]
    labels['artists'] = labels['artists'].str.replace(r'[^A-Za-z\s]+', '')

    sim_df = pd.DataFrame(data=labels, columns=['id', 'artists', 'name'])
    sim_df['similarity'] = cosine_similarity(item_profiles, track_profile)
    sim_df.sort_values(by=['similarity'], ascending=False, inplace=True)
    # Rename columns for displaying on website
    sim_df.columns = ['id', 'Artist', 'Song', 'Similarity']
    # Drop ID column and convert DataFrame to html 
    results_html = sim_df.drop(columns=['id'])[:20].to_html(index=False,
                                                            justify='center')
    # print(results_html)
    # Update HTML for Bootstrap
    results_html = results_html.replace('class="dataframe"', 'class="table"')
    results_html = results_html.replace('thead', 'thead class="thead-dark"')
    context = {
        'results_html': results_html,
    }
    return render(request, 'search/show_recommendations.html', context)


