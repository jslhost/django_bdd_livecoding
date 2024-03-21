from django.db import models

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField() # Permet d'afficher le titre dans l'url, transforme les espaces en tiret 
    published = models.BooleanField(default=False) # Les articles par défaut ne sont pas publiés
    date = models.DateField(blank=True, null=True) # Ce champ peut contenir des NaN
    content = models.TextField() # Pas de longueur max au contraire de CharField
    description = models.TextField()

    def publish_string(self):
        if self.published:
            return "L'article est publié"
        return "L'article est inaccessible"
