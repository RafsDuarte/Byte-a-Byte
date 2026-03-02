# ✅ Boas Práticas — Byte A Byte

Guia de boas práticas de código, segurança e deploy para o projeto Django.

---

## 🏗️ Boas Práticas de Código

### Slugs Únicos
Todos os models têm `slug` com `unique=True`, gerado automaticamente pelo admin via `prepopulated_fields`.

- Melhora o SEO — `/post/como-escolher-gpu/` é indexado melhor que `/post/1/`
- Evita duplicatas — o banco rejeita slugs repetidos
- Nunca use IDs numéricos em URLs públicas

### Campo `is_published`
Controla a visibilidade sem deletar conteúdo.

- Permite salvar rascunhos sem publicar
- Facilita publicação manual futura
- Nunca delete um post — use `is_published = False`

### `get_object_or_404`
Todas as views usam `get_object_or_404` ao invés de `.get()`.

```python
# ✅ correto — retorna 404 para o usuário
post = get_object_or_404(Post, slug=slug, is_published=True)

# ❌ errado — gera erro 500 se não encontrar
post = Post.objects.get(slug=slug)
```

### Datas Automáticas
`auto_now_add` e `auto_now` garantem datas sempre precisas e não editáveis acidentalmente.

```python
created_at = models.DateTimeField(auto_now_add=True)  # define na criação
updated_at = models.DateTimeField(auto_now=True)       # atualiza a cada save
```

### `on_delete` Correto
- `Post.category` usa `SET_NULL` — mantém o post se a categoria for deletada
- `Category.parent` usa `CASCADE` — remove subcategorias ao deletar o pai

### `ordering` no `Meta`
Define ordenação padrão consistente para todas as queries.

```python
class Meta:
    ordering = ['-created_at']  # posts mais recentes primeiro
```

### Proteção Contra SQL Injection
Use sempre o ORM. Nunca construa queries com f-strings.

```python
# ✅ correto
Post.objects.filter(slug=slug, is_published=True)

# ❌ errado — vulnerável a SQL Injection
Post.objects.raw(f'SELECT * FROM blog_post WHERE slug = {slug}')
```

---

## 🔐 Segurança

### Variáveis de Ambiente
Nunca coloque dados sensíveis no `settings.py`. Use `.env` com `python-decouple`.

```bash
pip install python-decouple
```

**.env**
```env
SECRET_KEY=sua-chave-super-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=localhost,seudominio.com
DATABASE_URL=postgres://user:senha@localhost/pcdicas
```

**settings.py**
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
```

> ⚠️ **Adicione `.env` ao `.gitignore` imediatamente!**

### Configurações de Produção

```python
# settings.py — produção
DEBUG = False
ALLOWED_HOSTS = ['seudominio.com']

SECURE_SSL_REDIRECT = True             # redireciona HTTP para HTTPS
SESSION_COOKIE_SECURE = True           # cookie só via HTTPS
CSRF_COOKIE_SECURE = True              # proteção CSRF via HTTPS
SECURE_HSTS_SECONDS = 31536000        # força HTTPS por 1 ano
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

X_FRAME_OPTIONS = 'DENY'              # evita clickjacking
SECURE_CONTENT_TYPE_NOSNIFF = True    # evita sniffing de MIME
```

### URL do Admin
Mude `/admin/` para algo menos óbvio:

```python
# urls.py
path('painel-pcdicas/', admin.site.urls),
```

### Senhas e Acesso ao Admin
- Use senha longa e única para o superusuário
- Instale `django-two-factor-auth` para autenticação em dois fatores
- Use `django-axes` para bloquear tentativas de login repetidas

---

## 🧪 Testes

```bash
python manage.py test
```

O que testar no PCDicas:

```python
from django.test import TestCase
from .models import Category, Post

class PostModelTest(TestCase):
    def test_post_str_retorna_titulo(self):
        post = Post(title="Como escolher uma GPU")
        self.assertEqual(str(post), "Como escolher uma GPU")

    def test_post_nao_publicado_nao_aparece(self):
        Post.objects.create(title="Rascunho", slug="rascunho", is_published=False)
        posts = Post.objects.filter(is_published=True)
        self.assertEqual(posts.count(), 0)

    def test_slug_inexistente_retorna_404(self):
        response = self.client.get('/post/nao-existe/')
        self.assertEqual(response.status_code, 404)

    def test_categoria_hierarquia(self):
        pai = Category.objects.create(name="Hardware", slug="hardware")
        filho = Category.objects.create(name="CPU", slug="cpu", parent=pai)
        self.assertEqual(str(filho), "Hardware > CPU")
```

---

## 🚀 Deploy (Produção)

### Recomendações de Infraestrutura
- **Servidor**: Railway, Render ou VPS com Nginx + Gunicorn
- **Banco de dados**: PostgreSQL (mais robusto que SQLite)
- **Arquivos estáticos**: Whitenoise ou AWS S3
- **Variáveis de ambiente**: configuradas no painel do serviço de hospedagem

```bash
pip install gunicorn whitenoise psycopg2-binary
```

### Arquivos Estáticos com Whitenoise

```python
# settings.py
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

```bash
python manage.py collectstatic
```

---

## 📋 Checklist Antes de Colocar no Ar

- [ ] `DEBUG = False` no settings de produção
- [ ] `SECRET_KEY` forte e no `.env`
- [ ] `.env` no `.gitignore`
- [ ] HTTPS ativado e configurações de segurança aplicadas
- [ ] URL do admin alterada
- [ ] Banco de dados PostgreSQL configurado
- [ ] `collectstatic` executado
- [ ] Testes passando
- [ ] Superusuário com senha forte criado
