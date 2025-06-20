from django.urls import path
from app02 import views

urlpatterns =[
    path('', views.home),
    path('write_form/', views.write_form),
    path('insert/', views.insert),
    path('list/', views.list),
    path('detail', views.detail),
    path('detail/<int:board_id>/', views.detail, name='view'),
    
    # path('update_form', views.update)

    path("download_count/", views.download_count),
    path("download/", views.download),

    
]