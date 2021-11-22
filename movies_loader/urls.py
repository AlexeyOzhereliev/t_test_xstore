from django.urls import path

from . import views

urlpatterns = [
    path('GETapi/movies/', views.GetGenreInfoView.as_view()),
    path('GETapi/actors/', views.GetActorsInfoView.as_view()),
    path('GETapi/directors/', views.GetDirectorsInfoView.as_view()),
]