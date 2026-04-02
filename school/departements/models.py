from django.db import models

class Departement(models.Model):
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom du département")
    code = models.CharField(max_length=10, unique=True, verbose_name="Code")
    description = models.TextField(blank=True, verbose_name="Description")
    responsable = models.CharField(max_length=100, blank=True, verbose_name="Responsable")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    email = models.EmailField(blank=True, verbose_name="Email")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nom']
        verbose_name = 'Département'
        verbose_name_plural = 'Départements'

    def __str__(self):
        return f"{self.nom} ({self.code})"
