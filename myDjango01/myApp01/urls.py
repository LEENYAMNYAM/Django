from django.urls import path
from myApp01 import views

urlpatterns =[
    # Include the URLs from myApp01
    path("", views.write_form),
    path("insert/", views.insert),
]