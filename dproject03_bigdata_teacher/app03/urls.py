from django.urls import path
from django.contrib.auth import views as auth_views
from app03 import views

urlpatterns = [
    path('',views.home),
    path('melon/',views.melon),
    path('movie/',views.movie),
    path('movie_db/',views.movie_db),
    path('movie_dbchart/',views.movie_dbchart),
    path('movie_chart/',views.movie_chart),


      #############
    path('login/',
         auth_views.LoginView.as_view(template_name='common/login.html'),
         name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),    
    path('signup/', views.signup),  

    
    

   
]