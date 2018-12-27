from django.db import models
import json
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager
)

class UserManage(BaseUserManager):
	def create_user(self, email, password=None, active=True, is_director=False, is_admin=False, lastname='', firstname='', secondname='', date=None, old_pass=True, company=0):
		if not email:
			raise ValueError("Users must have an email address")
		if not password:
			raise ValueError("Users must have a password")
		user_obj = self.model(
			email = self.normalize_email(email)
		)
		user_obj.set_password("natusvincere"+password)
		user_obj.active = active
		user_obj.director = is_director
		user_obj.admin = is_admin
		user_obj.lastname = lastname
		user_obj.firstname = firstname
		user_obj.secondname = secondname
		user_obj.date = date
		user_obj.old_pass = old_pass
		user_obj.company = company
		user_obj.save(using=self._db)
		return user_obj

	def create_director(self, email, password=None):
		user = self.create_user(email, password=password, is_director=True)
		return user

	def create_superuser(self, email, password=None):
		user = self.create_user(email, password=password, is_admin=True)
		return user

class User(AbstractBaseUser):
	email      = models.EmailField(max_length=255, unique=True, default='abc123@mail.ru')
	active     = models.BooleanField(default=True)
	director   = models.BooleanField(default=False)
	admin      = models.BooleanField(default=False)
	lastname   = models.CharField(max_length=255, verbose_name="Фамилия", default='')
	firstname  = models.CharField(max_length=255, verbose_name="Имя", default='')
	secondname = models.CharField(max_length=255, verbose_name="Отчество", default='', null=True, blank=True)
	date       = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
	company    = models.IntegerField(verbose_name="компания", default=0)
	old_pass   = models.BooleanField(default=True)
	image      = models.FileField(default='person.jpg')

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManage()

	def __str__(self):
		return self.email

	def get_full_name(self):
		out = self.lastname + ' ' + self.firstname + ' ' + self.secondname
		return out

	def short_name(self):
		out = self.lastname + ' ' + self.firstname[0:1] + '.'
		if self.secondname > '':
			out += self.secondname[0:1]
			out += '.'
		return out

	def get_company(self):
		with open('ocean/templates/ocean/json_data.json', mode='r', encoding='utf-8') as feedsjson:
			d = json.load(feedsjson)
		name = ""
		for i in range(0, len(d["companies"])):
			if d["companies"][i]["id"] == self.company:
				name = d["companies"][i]["name"]
		return name

	def get_old_pass(self):
		return self.old_pass

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_active(self):
		return self.active
	def is_director(self):
		return self.director
	def is_staff(self):
		return self.admin
	def is_admin(self):
		return self.admin
	def is_superuser(self):
		return self.admin