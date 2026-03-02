from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)  # nome da categoria
    slug = models.SlugField(unique=True)  # identificador único na URL

    parent = models.ForeignKey(
        'self',  # referência a si mesma para subcategorias
        on_delete=models.CASCADE,  # apaga filhos ao apagar o pai
        null=True,
        blank=True,
        related_name='children'  # acessa subcategorias via categoria.children
    )

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']  # ordena alfabeticamente

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"  # exibe hierarquia pai > filho
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)  # título do post
    slug = models.SlugField(unique=True)  # identificador único na URL
    content = models.TextField()  # conteúdo principal

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # mantém o post se a categoria for apagada
        null=True,
        related_name='posts'  # acessa posts via categoria.posts
    )

    created_at = models.DateTimeField(auto_now_add=True)  # data de criação automática
    updated_at = models.DateTimeField(auto_now=True)  # atualiza a cada save
    is_published = models.BooleanField(default=True)  # controla visibilidade do post

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']  # mais recentes primeiro

    def __str__(self):
        return self.title