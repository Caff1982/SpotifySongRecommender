from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('show_recommendations/<track_id>', show_recommendations, name='show_recommendations')
]