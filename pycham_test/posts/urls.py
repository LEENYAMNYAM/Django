from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('create/', views.create_post, name='create'),
    path('<int:post_id>/', views.get_post, name='read'),
    path('<int:post_id>/update/', views.update_post, name='create'),
    path('<int:post_id>/delete', views.delete_post, name='delete'),
    path('<int:post_id>/download/', views.download_post, name='download'),
    path('', views.get_posts, name='list'),

]