from django.urls import path

from .import views

app_name = 'core'

urlpatterns = [

    path('',views.MovieList.as_view(),name='movies'),
    path('movies/top',views.TopMovies.as_view(),name='top_movie'),
    path('movie/<int:pk>',views.MovieDetail.as_view(),name='MovieDetail'),
    path('movie/<int:movie_id>/vote',views.CreateVote.as_view(),name='CreateVote'),
    path('movie/<int:movie_id>/vote/<int:pk>',views.UpdateVote.as_view(),name='UpdateVote'),
    path('movie/<int:movie_id>/image/upload',views.MovieImageUpload.as_view(),name='MovieImageUpload'),
]