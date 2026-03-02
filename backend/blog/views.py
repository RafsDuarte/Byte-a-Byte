from django.shortcuts import render, get_object_or_404
from .models import Category, Post

def index(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')  # busca posts publicados, mais recentes primeiro

    return render(request, 'blog/index.html', {
        'posts': posts
    })

def post_list(request):
    posts = Post.objects.filter(is_published=True)  # busca apenas posts publicados
    return render(request, 'blog/posts_list.html', {'posts': posts})

def posts_by_category(request, parent_slug, slug):
    parent = get_object_or_404(Category, slug=parent_slug, parent__isnull=True)  # garante que é categoria raiz
    category = get_object_or_404(Category, slug=slug, parent=parent)  # busca subcategoria vinculada ao pai

    posts = Post.objects.filter(
        category=category,
        is_published=True  # filtra apenas publicados
    )

    return render(
        request,
        'blog/posts_list.html',
        {
            'posts': posts,
            'category': category,
            'parent': parent,
        }
    )

def posts_by_subcategory(request, slug):
    category = get_object_or_404(Category, slug=slug)  # busca categoria pelo slug

    posts = Post.objects.filter(category=category, is_published=True)  # filtra posts da categoria

    return render(request, 'blog/category.html', {
        'category': category,
        'posts': posts
    })

def post_detail(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        is_published=True  # impede acesso a posts não publicados
    )

    return render(request, 'blog/post_detail.html', {
        'post': post
    })