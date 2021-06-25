from django.shortcuts import render
from django.views.generic import ListView
from django.conf import settings

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from .forms import SearchForm
from .models import Song


def home(request):
    form = SearchForm(request.POST or None, auto_id=False)
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


class SearchResults(ListView):
    model = Song
    template_name = 'search/show_recommendations.html'

    def get_queryset(self):
        target_id = self.kwargs['song_id']
        # Connect to Spotipy
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                                client_id=settings.SPOTIPY_CLIENT_ID,
                                client_secret=settings.SPOTIPY_CLIENT_SECRET))
        # Get features for track
        track_features = sp.audio_features(target_id)[0]
        # Keep only the columns we need
        cols = ['energy', 'danceability',
            'speechiness', 'acousticness',
            'instrumentalness', 'liveness', 'valence']
        track_profile = [track_features[col] for col in cols]
        track_profile = np.array(track_profile).reshape(1, -1)

        df = pd.read_csv('./item_profiles.csv')
        item_profiles = df[cols]
        print('Item_profiles shape: ', item_profiles.shape)
        print('Track profiles shape: ', track_profile.shape)
        # Keep ID's to use a labels
        labels = pd.DataFrame(data=df['id'].values, columns=['song_id'])
        # Add cos theta as column to labels df
        labels['similarity'] = cosine_similarity(item_profiles, track_profile).reshape(1, -1)[0]
        labels.sort_values(by=['similarity'], ascending=False, inplace=True)
        # Use most similar tracks to create a list of Song objects
        print(labels.head(10))
        queryset = [Song.objects.filter(song_id=song_id)[0] for song_id in labels['song_id'][:20]]
        return queryset

        





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
    item_profiles = df[cols]
    print('Item_profiles shape: ', item_profiles.shape)
    print('Track profiles shape: ', track_profile.shape)
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
    results_csv = sim_df.drop(columns=['id'])[:20].to_csv()

    # Update HTML for Bootstrap
    results_html = results_html.replace('class="dataframe"', 'class="table"')
    results_html = results_html.replace('thead', 'thead class="thead-dark"')
    context = {
        'results_html': results_html,
    }
    return render(request, 'search/show_recommendations.html', context)
