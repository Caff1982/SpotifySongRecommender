## Spotify Song Recommender

I made this application to help me find music similar to the music that I like. As much as I enjoy using Spotify I find that the music it recommends to me is mainly from arists that I've already heard. For this project I used Spotify's "hidden" features ('energy', 'danceability', 'speechiness', 'acousticness', 'instrumentalness', 'liveness' and 'valence') and found the cosine simlarity between the features for the a target track and a dataset of around 600k songs. The top twenty songs with the highest similarity are displayed.

To run this project locally download the dataset from kaggle and place the "tracks.csv" file in the main directory. Dataset is from https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks
 
Background image taken from pexels.com, link to original https://www.pexels.com/photo/people-enjoying-the-concert-1047442/

The project is hosted [here](https://stormy-crag-39179.herokuapp.com/)