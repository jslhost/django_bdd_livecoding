# Livecoding Django 2 : BDD
Code de l'app Django produite durant le livecoding du 21/03/2024.

Vous trouverez ci-dessous mes notes utilisées durant le livecoding pour reproduire l'application :


### Prérequis :

```bash
python -m venv env_django

source env_django/Scripts/activate

pip install django 

pip freeze > requirements.txt

django-admin startproject MyProject

renommer MyProject en src

cd src
```

Création d’une vue très simple :

Je créé [views.py](http://views.py) dans MyProject

```python
from django.shortcuts import render

def blog_post(request):
    return render(request, "blog_post.html")
```

Puis dans [urls.py](http://urls.py/) :

- ajouter : from .views import blog_post
- et dans la variable urlpatterns : path("", blog_post, name="blog_post"),

Puis créer un nouveau dossier "templates" dans MyProject
Dans ce dossier, créer un fichier "blog_post.html" et coller le code suivant :

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mon site web</title>
</head>

<body>
  <h1>Formulaire</h1>
</body>

</html>
```

Puis ajouter le chemin vers ce template dans [settings.py](http://settings.py/) :

```python
import os 
# et dans la variable TEMPLATES :
DIRS : [os.path.join(BASE_DIR, r"MyProject\templates")]
```

### Début du Livecoding

**Objectif : Créer une BDD et réussir à ajouter du contenu à l’intérieur via notre application. Pour cela on va utiliser les modèles pour créer la BDD et les formulaires pour rajouter des données depuis l’app.**

```python
python [manage.py](http://manage.py) runserver # crée le fichier db.sqlite3
```

On peut visualiser la BDD facilement à l’intérieur de DBeaver.
Elle est vide pour l’instant, ce qui est normal.

Puis on peut retourner sur le projet pour effectuer la migration :

```bash
python manage.py migrate
```

Puis on retourne sur DBeaver, on fait clique droit “régénérer” sur la bdd et les tables apparaissent

On peut voir la table migrations pour voir les migrations effectuées. 

### Les modèles et les migrations

Beaucoup de champs possibles, ce sont des “type de données” : bool, str, text, filepath etc.

La clé primaire = ID

On va créer une application :

```bash
python manage.py startapp blog 
```

Puis on se rend dans MyProject/settings.py et on rajoute ‘blog’ dans la liste INSTALLED_APPS

On va maintenant aller dans blog/models.py pour venir créer notre modèle de bdd. Le fichier doit ressembler à quelque chose comme :

```python
from django.db import models

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField() # Permet d'afficher le titre dans l'url, transforme les espaces en tiret 
    published = models.BooleanField(default=False) # Les articles par défaut ne sont pas publiés
    date = models.DateField(blank=True, null=True) # Ce champ peut contenir des NaN
    content = models.TextField() # Pas de longueur max au contraire de CharField
```

On retourne dans le terminal :

```bash
python manage.py makemigrations blog
```

Dans blog/migrations apparait alors 0001_initial.py

On rentre dans le fichier et on observe que cela correspond au modèle que l’on a spécifié. On peut noter que id a été créé de lui même.

Les migrations permettent de recréer l’état de nos bdd. C’est un peu comme un historique de notre bdd. Parallèle avec git. On inclut d’ailleurs ces fichiers sur git.

On peut relancer makemigrations et voir qu’il ne se passe rien car il n’y a pas de changement sur la bdd.

Dans models.py on rajoute un nouveau champ : **description = models.TextField()** puis on réutilise makemigrations.

Puis : option 1 et “”

On peut aller dans le nouveau fichier de migration et observer la dépendance avec le premier fichier.

Puis on lance :

```bash
# Récupérer le code sql que la migration va lancer :
python manage.py sqlmigrate blog 0001_initial 

python manage.py migrate blog # Applique les migrations
```

Puis retourner sur DBeaver pour voir la nouvelle table 

### Faire des requêtes

```bash
python manage.py shell
```

```python
from blog.models import BlogPost # BlogPost représente notre table

# On créé une nouvelle ligne dans la BDD
blog_post = BlogPost(title="test", slug="test", content="test", description="description")

blog_post.save() # Puis retourner voir sur DBeaver

BlogPost.objects.all()

BlogPost.objects.get(title='test')

b = BlogPost.objects.get(title='test')
b.content = "Je modifie mon article"
b.save()

BlogPost.objects.filter(title='test') # A noter que filter est vraiment riche 
```

On va rajoute une méthode pour notre classe :

```python
quit()
```

On modifie [models.py](http://models.py) en rajoutant la méthode publish_string : 

```python
class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField() # Permet d'afficher le titre dans l'url, transforme les espaces en tiret 
    published = models.BooleanField(default=False) # Les articles par défaut ne sont pas publiés
    date = models.DateField(blank=True, null=True) # blank=True : Ce champ peut contenir des NaN
    content = models.TextField() # Pas de longueur max au contraire de CharField
    description = models.TextField()

    def publish_string(self):
        if self.published:
            return "L'article est publié"
        return "L'article est inaccessible"
```

Puis on retourne sur l’interpréteur python :

```python
python manage.py shell

from blog.models import BlogPost
b = BlogPost.objects.get(title='test')
b.publish_string()

quit()
```

### Créer un formulaire

Créer un fichier ‘forms.py’ dans MyProject. On le complète de cette manière :

```python
from django import forms 
from blog.models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'description']
```

On retourne sur le terminal

```python
python manage.py shell

from MyProject.forms import BlogPostForm
form = BlogPostForm()
print(form)
```

On se rend sur le fichier [views.py](http://views.py) et on le modifie ainsi :

```python
from django.shortcuts import render
from MyProject.forms import BlogPostForm

def blog_post(request):

    form = BlogPostForm()

    return render(request, "blog_post.html", {"form": form})
```

Puis on se rend dans templates/blog_post.html qu’on modifie ainsi :

```python
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mon site web</title>
</head>

<body>
  <h1>Formulaire</h1>
  
  <form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    
    <input type="submit" value="Publier">

  </form>

</body>

</html>
```

On regarde si le formulaire s’affiche dans notre application :

```python
python manage.py runserver
```

On va maintenant faire en sorte de pouvoir sauvegarder le formulaire dans la bdd.

Pour se faire on retourne sur [views.py](http://views.py) qu’on modifie ainsi :

```python
from django.shortcuts import render
from MyProject.forms import BlogPostForm

def blog_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            form = BlogPostForm()
    else:
        form = BlogPostForm()

    return render(request, "blog_post.html", {"form": form})
```
