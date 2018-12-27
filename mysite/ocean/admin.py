from functools import update_wrapper

from django.contrib import admin
from django.contrib.auth import get_user_model
from .forms import UserAdminCreationForm, UserAdminChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import Http404
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

User = get_user_model()

class UserAdmin(BaseUserAdmin):
	form = UserAdminChangeForm
	add_form = UserAdminCreationForm

	list_display = ('email', 'active')
	list_filter = ('admin', 'director')
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Персональная информация', {'fields': ('lastname', 'firstname', 'secondname', 'date', 'company')}),
		('Разрешения', {'fields': ('admin', 'director', 'active')}),
	)
	add_fieldsets = (
		(None, {
			'classes':('wide',),
			'fields': ('email', 'password1', 'password2')}
		),
	)
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()
# def admin_view(view, cacheable=False):
# 	def inner(request, *args, **kwargs):
# 		if not request.user.admin:
# 			raise Http404()
# 		return view(request, *args, **kwargs)

# 	if not cacheable:
# 		inner = never_cache(inner)
# 	if not getattr(view, 'csrf_exempt', False):
# 		inner = csrf_protect(inner)

# 	return update_wrapper(inner, view)

admin.site.register(User, UserAdmin)