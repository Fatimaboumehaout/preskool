from django.db import models

class Holiday(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom du congé")
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(verbose_name="Date de fin")
    description = models.TextField(blank=True, verbose_name="Description")
    type_conge = models.CharField(
        max_length=20,
        choices=[
            ('vacances', 'Vacances'),
            ('fete', 'Fête'),
            ('autre', 'Autre'),
        ],
        default='vacances',
        verbose_name="Type de congé"
    )
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_debut']
        verbose_name = 'Congé/Holiday'
        verbose_name_plural = 'Congés/Holidays'

    def __str__(self):
        return f"{self.name} ({self.date_debut} - {self.date_fin})"
