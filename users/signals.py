from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from events.models import Event

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}"
        subject = "Activate your EventSync Account"
        if instance.first_name and instance.last_name:
            recipient_name = instance.get_full_name()
        elif instance.first_name:
            recipient_name = instance.first_name
        elif instance.last_name:
            recipient_name = instance.last_name
        else:
            recipient_name = instance.username
        message = f"Hi {recipient_name},\n\nThank you for signing up on EventSync. Activate your account by clicking the activation link below:\n{activation_url}\n\nYou can safely ignore this email if you don't want to Sign Up.\n\nBest Regards,\n\nEventSync Business & Dev Team\nSynchronize your Events with care."
        recipient_list = [instance.email]
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        except Exception as err:
            print(f"Failed to sent email to {instance.email} for: {str(err)}")


@receiver(post_save, sender=User)
def assign_role(sender, instance, created, **kwargs):
    if created:
        user_group, created = Group.objects.get_or_create(name='User')
        participant_group = Group.objects.get(name='Participant')
        instance.groups.add(user_group)
        instance.groups.add(participant_group)
        instance.save()
