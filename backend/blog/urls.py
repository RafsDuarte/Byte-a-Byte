from django.urls import path
from . import views

urlpatterns = [
    # HOME do site (lista geral de posts)
    path('', views.index, name='home'),

    # Categoria pai
    path(
        'categoria/<slug:slug>/',
        views.posts_by_category,
        name='category_posts'
    ),

    # Subcategoria
    path(
        'categoria/<slug:parent_slug>/<slug:slug>/',
        views.posts_by_subcategory,
        name='subcategory_posts'
    ),

    # Post individual
    path(
        'post/<slug:slug>/',
        views.post_detail,
        name='post_detail'
    ),
]
