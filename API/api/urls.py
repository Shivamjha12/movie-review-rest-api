from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path, include
from API.api import views

urlpatterns = [
        path('', views.MovieListAV.as_view(), name='movies_list'),
        path('movies/<int:pk>/', views.MovieDetailAV.as_view(), name='movies_details'),
        path('platforms/', views.StreamingPlatformsAV.as_view(), name='platforms'),
        path('platforms/<int:pk>/', views.StreamingPlatformsDetailview.as_view(), name='streamingplatforms-detail'),
        path('movies/<int:pk>/reviews/', views.reviewstList.as_view(), name='review-list'),
        path('movies/', views.movies_se.as_view(), name='movie-list'),
        path('movies/review/<int:pk>/', views.reviewsAll.as_view(), name='review-all'),
        path('movies/<int:pk>/reviews-create/', views.reviewsDetailsCreate.as_view(), name='review-list_detail_create'),
        path('user/', views.UserReview_filter.as_view(),name='logout'),         
]