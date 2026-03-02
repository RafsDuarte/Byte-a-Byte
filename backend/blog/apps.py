from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # define BigAutoField como tipo padrão para IDs
    name = 'blog'  # nome do app registrado no Django