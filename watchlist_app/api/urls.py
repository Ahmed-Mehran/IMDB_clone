from django.urls import path

from watchlist_app.api import views


urlpatterns = [
    
    path('movie-list', views.WatchListAV.as_view(), name='movie-list'),
    
    path('movie-details/<int:pk>', views.WatchDetailAV.as_view(), name='movie-details'),
    
    path('stream-platform', views.StreamPlatformAV.as_view(), name='stream-platform'),
    
    path('stream-platform-detail/<int:pk>', views.StreamPlatformDetailsAV.as_view(), name='stream-platform-detail'),
    
    # path('all-reviews', views.ReviewListAV.as_view(), name='all-reviews'),  the modified review urls are below 2
    
    # path('review/<int:pk>', views.ReviewDetailsAV.as_view(), name='review'),
    
    path('movie-details/<int:pk>/all-reviews', views.ReviewListAV.as_view(), name='all-reviews'),
    
    path('movie-list/review/<int:pk>', views.ReviewDetailsAV.as_view(), name='review'),
     
    
]
