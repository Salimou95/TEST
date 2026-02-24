"""Models for the accounts app."""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extended profile for a user."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", verbose_name="Utilisateur"
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    address = models.CharField(max_length=250, blank=True, verbose_name="Adresse")
    city = models.CharField(max_length=100, blank=True, verbose_name="Ville")
    postal_code = models.CharField(max_length=20, blank=True, verbose_name="Code postal")
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="Avatar"
    )

    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"

    def __str__(self):
        return f"Profil de {self.user.username}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Automatically create or update the UserProfile when a User is saved."""
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()
