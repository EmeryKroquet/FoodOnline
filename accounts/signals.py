from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    # Vérifie si l'utilisateur vient d'être créé
    if created:
        UserProfile.objects.create(user=instance)
        print(f"UserProfile created for {instance.email}")
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()  # Enregistre le profil si trouvé
            print(f"UserProfile updated for {instance.email}")
        except UserProfile.DoesNotExist:
            # Crée le UserProfile si celui-ci n'existe pas encore
            UserProfile.objects.create(user=instance)
            print(f"UserProfile created for {instance.email} (after except)")
        except Exception as e:
            print(f"Error updating UserProfile for {instance.email}: {e}")

@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    # Logique à ajouter avant de sauvegarder un profil utilisateur
    print(f"Pre-save signal triggered for {instance.email}")
