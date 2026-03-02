from django.contrib import admin
from .models import Post, Category

@admin.register(Category)  # registra Category no admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')  # colunas exibidas na listagem
    list_filter = ('parent',)  # filtro lateral por categoria pai
    prepopulated_fields = {'slug': ('name',)}  # slug gerado automaticamente pelo nome

@admin.register(Post)  # registra Post no admin
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at')  # colunas: título, status e data
    prepopulated_fields = {'slug': ('title',)}  # slug gerado automaticamente pelo título