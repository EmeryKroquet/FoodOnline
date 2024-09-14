from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


def detectUser(user):
    """
    Detects the user's role and returns the appropriate redirection URL.
    """
    if user.role == 1:
        return 'vendorDashboard'
    elif user.role == 2:
        return 'custDashboard'
    elif user.role is None and user.is_superadmin:
        return '/admin'
    return None  # Default if no role matches


def send_verification_email(request, user, mail_subject, email_template):
    """
    Sends a verification email with a secure link to validate the user.
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = "html"  # Defines HTML content type
    mail.send()  # Send e-mail


def send_notification(mail_subject, mail_template, context):
    """
    Sends an e-mail notification based on a given template and context.
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)

    # Make sure to_email is a list even if it's a single string
    to_email = context['to_email'] if isinstance(context['to_email'], list) else [context['to_email']]

    mail = EmailMessage(mail_subject, message, from_email, to=to_email)
    mail.content_subtype = "html"  #Defines HTML content type
    mail.send()  # Send e-mail
