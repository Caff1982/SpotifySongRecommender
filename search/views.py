from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.conf import settings

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from .forms import SearchForm, OptionsForm
from .models import Song


def home(request):
    form = SearchForm(request.GET or None, auto_id=False)
    search_results = []

    if request.method == 'GET' and form.is_valid():
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
    form_class = OptionsForm

    def get(self, request, **kwargs):
        form = OptionsForm(self.request.GET or None, auto_id=False)
        # Update search preferences if form is submitted
        if self.request.method == 'GET' and form.is_valid():
            features = form.cleaned_data['search_options']
        else:
            features = ['energy', 'danceability',
                    'speechiness', 'acousticness',
                    'instrumentalness', 'liveness', 'valence']

        print('q: ', self.request.GET.get('search_options'))
        target_id = self.kwargs['song_id']
        # Connect to Spotipy
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                                client_id=settings.SPOTIPY_CLIENT_ID,
                                client_secret=settings.SPOTIPY_CLIENT_SECRET))
        # Get features for track
        track_features = sp.audio_features(target_id)[0]
        
        track_profile = [track_features[feat] for feat in features]
        track_profile = np.array(track_profile).reshape(1, -1)

        df = pd.read_csv('./item_profiles.csv')
        item_profiles = df[features]
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
        
        context = {
            'queryset': queryset,
            'form': form,
            'features': features
        }

        return render(request, self.template_name, context)

    # def get_context_data(self, *args, **kwargs):
    #     context = super(SearchResults, self).get_context_data(**kwargs)
    #     context['form'] = OptionsForm()
    #     print('context form: ', context['form']['search_options'])
    #     return context
