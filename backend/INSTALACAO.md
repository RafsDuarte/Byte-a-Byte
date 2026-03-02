## ⚙️ Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/Byte A Byte.git
cd Byte A Byte

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env

# Execute as migrações
python manage.py migrate

# Crie o superusuário
python manage.py createsuperuser

# Inicie o servidor
python manage.py runserver
```

---

## 📦 Dependências

```
Django>=4.2
python-decouple>=3.8
Pillow>=10.0
django-extensions>=3.2
```
