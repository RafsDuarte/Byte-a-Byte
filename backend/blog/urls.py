from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # lista geral de posts

    path(
        'categoria/<slug:slug>/',
        views.posts_by_category,
        name='category_posts'  # posts filtrados por categoria pai
    ),

    path(
        'categoria/<slug:parent_slug>/<slug:slug>/',
        views.posts_by_subcategory,
        name='subcategory_posts'  # posts filtrados por subcategoria
    ),

    path(
        'post/<slug:slug>/',
        views.post_detail,
        name='post_detail'  # exibe um post individual
    ),
]