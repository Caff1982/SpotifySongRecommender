## Spotifynder Song Recommender

I made this project to help me find new music. As much as I enjoy using Spotify I find that the music it recommends to me is mainly from arists that I've already heard. For this project I used Spotify's "hidden" features ('energy', 'danceability', 'speechiness', 'acousticness', 'instrumentalness', 'liveness' and 'valence') and found the cosine-theta simlarity between the features for a target track and a dataset of around 600k songs.
The top twenty songs with the highest similarity are displayed.

I created a basic website using django which is hosted [here](https://stormy-crag-39179.herokuapp.com/). 

To run this project locally download the dataset from kaggle and place the "tracks.csv" file in the main directory. Dataset is from https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks. Then run "python manage.py populate_db tracks.csv". This will populate the database with rows from the csv file. 

Background image taken from pexels.com, link to original https://www.pexels.com/photo/people-enjoying-the-concert-1047442/
