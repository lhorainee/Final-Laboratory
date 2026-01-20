from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('create/', views.create_post, name='create_post'),
    path('react/<int:post_id>/<str:r_type>/', views.add_reaction, name='add_reaction'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
]

