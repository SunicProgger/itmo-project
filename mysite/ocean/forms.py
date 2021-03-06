from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email',)

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Пароли не совпадают")
		return password2

	def save(self, commit=True):
		user = super(UserAdminCreationForm, self).save(commit=False)
		user.set_password("natusvincere"+self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class UserAdminChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ('email', 'password', 'active', 'admin')

	def clean_password(self):
		return self.initial["password"]
