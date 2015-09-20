from django.db import models
from django.conf import settings
from django.template import loader
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser

from .managers import AccountManager
from ..utils.models import BaseModel


class User(BaseModel, AbstractBaseUser):
    username = models.CharField(max_length=45, unique=True)
    email = models.EmailField(max_length=40, unique=True)

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)

    phone = models.CharField(max_length=12, unique=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email', 'first_name', 'last_name', 'phone')

    def __unicode__(self):
        return self.email

    @property
    def full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name or self.email

    def has_perm(self, perm, obj=None):
        """
        Returns True if user is an active admin.
        """
        if self.is_active and self.is_admin:
            return True

    def has_module_perms(self, app_label):
        """
        Returns True if user is an active admin.
        """
        if self.is_active and self.is_admin:
            return True

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        "Is the user a member of the staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def set_password(self, raw_password):
        """
        Sets the user's password and changes token_version.
        """
        super(User, self).set_password(raw_password)

    def change_password(self, raw_password):
        """
        Sets the user's password, changes token_version.
        """
        self.set_password(raw_password)
        self.save()

    def get_email_context(self):
        return {
            "domain": settings.DOMAIN,
            "site_name": settings.SITE_NAME,
            "protocol": settings.PROTOCOL
        }

    def send_password_reset_email(self):
        context = self.get_email_context()
        context["token"] = self.password_reset_token
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL
        self.email_user(
            subject="Reset Password",
            message=loader.render_to_string(
                "email/password_reset_email_body.txt",
                context)
        )

    def send_account_activation_email(self):
        if self.is_active is False:
            context = self.get_email_context()
            context["token"] = self.account_activation_token
            context["url"] = settings.ACTIVATION_URL
            self.email_user(
                subject="Account Activation",
                message=loader.render_to_string(
                    "email/activation_email_body.txt",
                    context)
            )