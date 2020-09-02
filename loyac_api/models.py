from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import date
from django.db.models import Sum
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
import logging
from django.core.mail import EmailMessage
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):

	def _create_user(self, email, password, birth_date, first_name, last_name, is_staff, is_superuser, **extra_fields):
		if not email:
			raise ValueError('Users must have an email address')
		email = self.normalize_email(email)
		user = self.model(
			first_name=first_name,
			last_name=last_name,
			email=email,
			birth_date=birth_date,
			is_staff=is_staff,
			is_active=True,
			is_superuser=is_superuser,
			**extra_fields
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, first_name, last_name, email, password, birth_date, **extra_fields):
		user = self._create_user(
			first_name=first_name,
			last_name=last_name,
			email=email,
			password=password,
			birth_date=birth_date,
			is_superuser=True,
			is_staff=True,
			**extra_fields)
		user.save(using=self._db)
		return user


class User(AbstractBaseUser, PermissionsMixin):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(max_length=254, unique=True)
	birth_date = models.DateField(blank=True, null=True)
	is_staff = models.BooleanField(default=True)
	is_superuser = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	USERNAME_FIELD = 'email'
	EMAIL_FIELD = 'email'
	REQUIRED_FIELDS = ['birth_date', 'first_name', 'last_name']

	objects = UserManager()

	def get_absolute_url(self):
		return "/users/%i/" % (self.pk)

	def get_email(self):
		return self.email

	def __str__(self):
		return self.email

class AgeGroup(models.Model):
	name=models.CharField(max_length=100)
	from_age=models.IntegerField()
	to_age=models.IntegerField()
	def __str__(self):
		return self.name

class Program(models.Model):
	name = models.CharField(max_length=100)
	image = models.ImageField()
	description = models.CharField(max_length=255)
	age_group = models.ForeignKey(AgeGroup, on_delete=models.CASCADE)
	points = models.IntegerField(default=0)

	def __str__(self):
		return self.name


class Applicant(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='applicant')
	program = models.ManyToManyField(Program, blank=True)
	age = models.IntegerField(null=True, blank=True)

	def __str__(self):
		return self.user.first_name + " " + self.user.last_name
	
	def total_points(self):
		return self.program.aggregate(total=models.Sum('points'))['total']

	def save(self, *args, **kwargs):
		if not self.age:
			today = date.today()
			self.age = today.year - self.user.birth_date.year - \
				((today.month, today.day) <
				 (self.user.birth_date.month, self.user.birth_date.day))
			self.user.is_staff = False
			self.user.save()
			super(Applicant, self).save(*args, **kwargs)
			

@receiver(m2m_changed, sender=Applicant.program.through)
def applicant_program_changed(sender, instance, action, **kwargs):
	if action == "post_add":
		send_mail('Loyac Verification', 'Are you sure you want to register to this program?', 'hanineiroukh@gmail.com', [instance.user.email], fail_silently=False)
