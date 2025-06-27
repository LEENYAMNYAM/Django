from django.urls import path
from app03 import views

urlpatterns = [
    path('',views.home),
    path('melon/',views.melon),
    path('movie/',views.movie),
    path('movie_chart/',views.movie_chart),

    
    

   
]