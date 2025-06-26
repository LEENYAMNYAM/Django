from django.urls import path
from app02 import views


urlpatterns = [
    path('', views.home),
    path('write_form/', views.write_form, name="write"),
    path('insert/', views.insert),
    
    path('list/', views.list, name="list"),
    path('list_page/', views.list_page, name="list_page"),
    path('detail/<int:board_id>/', views.detail, name = "view"),
    path('delete/<int:board_id>/', views.delete),
    path('update/<int:board_id>/', views.update_form),
    path('update/', views.update),
  
    path('download_count/', views.download_count),
    path('download/', views.download),
    ###########
    path('comment_insert/', views.comment_insert),
    #####
    path('signup/', views.signup, name="signup"),
]