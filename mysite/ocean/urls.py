# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'login/', views.login, name="login"),
	url(r'logout/', views.logout, name="logout"),
	url(r'adminpage/$', views.openadminpage, name="adminpage"),	
	url(r'companies/$', views.getcompany, name="getcompany"),
	url(r'company_(?P<name>[0-9]+)/$', views.getcompany),
	url(r'delship_(?P<name>[0-9]+)/$', views.delship),
	url(r'newship/', views.ship, name="ship"),
	url(r'editship/', views.editship, name="editship"),
	url(r'editco/$', views.editco, name="editco"),
	url(r'profile(?P<typeer>[\w-]+)/$', views.profilepage, name="profileer"),
	url(r'delp_(?P<mail>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)/$', views.delprofile),
	url(r'actp_(?P<mail>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)/$', views.activateprofile),
	url(r'delco_(?P<name>[0-9]+)/$', views.delcompany, name="delcompany"),	
	url(r'profilesave_(?P<mail>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)/$', views.profilesave),
	url(r'people_(?P<name>[0-9]+)/$', views.people, name="people"),
	url(r'newperson/$', views.newperson),
	# url(r'show_(?P<mail>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)/$', views.showperson),
	url(r'newcompany/$', views.newcompany, name="company"),
	url(r'getinfo_(?P<mail>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)/$', views.getinfo),
]