from django.urls import path
from myApp01 import views

urlpatterns =[
    # Include the URLs from myApp01
    path("", views.list),
    path("write_form/", views.write_form, name='write'),
    path("insert/", views.insert),
    path("list/", views.list ),
    path("detail_idx/", views.detail_idx),
    path("detail/<int:board_idx>/", views.detail),

    path("delete/<int:board_idx>/", views.delete),
    
    path("update_form/<int:board_idx>/", views.update_form),
    path("update/", views.update),

    path("download_count/", views.download_count),
    path("download/", views.download),

    ##comment
    path("comment_insert/", views.comment_insert),

]