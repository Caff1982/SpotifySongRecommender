from django import forms


class SearchForm(forms.Form):
    song_title = forms.CharField(label='Song search', max_length=100, required=False,
                                 empty_value='Search by song title',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))