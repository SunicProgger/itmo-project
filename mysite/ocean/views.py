# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, redirect 
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import hashers
from django.template.context_processors import csrf
from pathlib import Path
from .models import User
from django.utils.encoding import smart_str
import operator, time, json

def index(request):
	companies = []
	oldpass = "no"
	d = json.load(open('ocean/templates/ocean/json_data.json', encoding="utf8"))
	for i in range(0, len(d["companies"])):
		companies.append(d["companies"][i]["name"])
	companies.sort()
	return render(request, 'ocean/homepage.html', {"args_co":companies})
def login(request):
	args = {}
	args.update(csrf(request))
	if request.POST:
		username = request.POST.get('loginusername', '')
		password = request.POST.get('loginpassword', '')
		user = auth.authenticate(email=username, password="natusvincere"+password)
		if user is not None:
			if user.is_active == True:
				auth.login(request, user)
				if user.old_pass:
					return redirect('profileer', typeer="me")
				return redirect('/')
			else:
				return render_to_response('ocean/companies.html')
		else:
			args['login_error'] = "no user"
			args['noemail'] = username
			args['nopass'] = password
			return render_to_response('ocean/homepage.html', args)
	else:
		return render_to_response('ocean/homepage.html', args)
def logout(request):
	auth.logout(request)
	return redirect('/')
def openadminpage(request):
	with open('ocean/templates/ocean/json_data.json', mode='r', encoding='utf-8') as feedsjson:
		d = json.load(feedsjson)
	cs = []
	users = User.objects.all()
	for i in range(0, len(d["companies"])):
		dt = {}
		dt["codata"] = d["companies"][i]
		ud = User.objects.get(email=dt["codata"]["director"])
		if ud is not None:
			dt["codata"]["director"] = ud.lastname + " " + ud.firstname + " " + ud.secondname + ", дата рождения: " + ud.date.strftime('%d.%m.%Y') + ", Email: " + ud.email;
		ships = []
		for j in range(0, len(d["ships"])):
			if d["ships"][j]["owner"] == dt["codata"]["id"]:
				ships.append(d["ships"][j])
		ships.sort(key=operator.itemgetter('name'))
		dt["ships"] = ships
		people = []
		deadpeople = []
		for k in users:
			if k.company == dt["codata"]["id"]:
				if k.active:
					people.append(k)
				else:
					deadpeople.append(k)
		people.sort(key=operator.attrgetter('firstname'))
		people.sort(key=operator.attrgetter('lastname'))
		deadpeople.sort(key=operator.attrgetter('firstname'))
		deadpeople.sort(key=operator.attrgetter('lastname'))
		dt["people"] = people
		dt["deadpeople"] = deadpeople
		cs.append(dt)
	for i in range(0, len(cs)):
		for j in range(0, len(cs)-1):
			if cs[j]["codata"]["name"].lower() > cs[j+1]["codata"]["name"].lower():
				t = cs[j]
				cs[j]=cs[j+1]
				cs[j+1]=t
	return render(request, 'ocean/adminpage.html', {"list": cs})
def getcompany(request, name=""):
	ships = []
	d = json.load(open('ocean/templates/ocean/json_data.json', encoding="utf8"))
	if name == "":
		if request.method == "GET":
			if 'choosecompany' in request.GET:
				namec = request.GET['choosecompany']
				ddict = {}
				for i in range(0, len(d["companies"])):
					if d["companies"][i]["name"] == namec:
						ddict = d["companies"][i]
				if len(ddict) > 0:
					for i in range(0, len(d["ships"])):
						if d["ships"][i]["owner"] == ddict["id"]:
							ships.append(d["ships"][i])
					ships.sort(key=operator.itemgetter('name'))
					ddict["photo"] = ""
					try:
						u = User.objects.get(email=ddict["director"])
						ddict["photo"] = u.image.url
						ddict["birthday"] = u.date
						ddict["fullname"] = u.lastname + " " + u.firstname + " " + u.secondname 
					except User.DoesNotExist:
						ddict["photo"] = ""
					finally:
						return render(request, 'ocean/companies.html', {"dict_co":ddict, "ships":ships})
				else:
					return render(request, 'ocean/homepage.html', {'args_co':companies,'er_co': namec})
			else:
				cid = request.user.company
				ddict = {}
				for i in range(0, len(d["companies"])):
					if d["companies"][i]["id"] == cid:
						ddict = d["companies"][i]
				if len(ddict) > 0:
					ud = User.objects.get(email=ddict["director"])
					for i in range(0, len(d["ships"])):
						if d["ships"][i]["owner"] == cid:
							ships.append(d["ships"][i])
					ships.sort(key=operator.itemgetter('name'))
					ddict["photo"] = ""
					try:
						u = User.objects.get(email=ddict["director"])
						ddict["photo"] = u.image.url
						ddict["birthday"] = u.date
						ddict["fullname"] = u.lastname + " " + u.firstname + " " + u.secondname 
					except User.DoesNotExist:
						ddict["photo"] = ""
					finally:
						return render(request, 'ocean/companies.html', {"dict_co":ddict, "ships":ships})
				else:
					return render(request, 'ocean/companies.html', {"dict_co":ddict, "ships":ships})	
		else:
			return render(request, 'ocean/homepage.html', {"args_co":companies})			
	else:
		ddict = {}
		for i in range(0, len(d["companies"])):
			if d["companies"][i]["id"] == (int)(name):
				ddict = d["companies"][i]
		for i in range(0, len(d["ships"])):
			if d["ships"][i]["owner"] == (int)(name):
				ships.append(d["ships"][i])
		ships.sort(key=operator.itemgetter('name'))
		ddict["photo"] = ""
		try:
			u = User.objects.get(email=ddict["director"])
			ddict["photo"] = u.image.url
			ddict["birthday"] = u.date
			ddict["fullname"] = u.lastname + " " + u.firstname + " " + u.secondname 
		except User.DoesNotExist:
			ddict["photo"] = ""
		finally:
			return render(request, 'ocean/companies.html', {"dict_co":ddict, "ships":ships})
def ship(request):
	if request.method == "POST":
		dnew = {}
		with open('ocean/templates/ocean/json_data.json', mode='r', encoding='utf-8') as feedsjson:
			d = json.load(feedsjson)
		d["id_sh"] = d["id_sh"] + 1
		dnew["id"] = d["id_sh"]
		dnew["name"] = request.POST.get('addshipname', '')
		dnew["model"] = request.POST.get('addshipmodel', '')
		dnew["date"] = request.POST.get('addshipdata', '')
		dnew["owner"] = request.user.company
		dnew["title"] = request.POST.get('addshiptitle', '')
		d["ships"].append(dnew)
		with open('ocean/templates/ocean/json_data.json', mode='w', encoding='utf-8') as feedsjson:
			json.dump(d, feedsjson)
		file_name = 'ocean/logger/ocean/' + (str)(dnew["owner"]) + '.txt';
		f1 = open(file_name, 'a');
		string = request.user.email + " [" + time.strftime("%H:%M %d/%m/%Y", time.localtime()) + "] " + " добавил во флот новый корабль " + dnew["name"] + ".\n" 
		f1.write(string)
		f1.close();
		return HttpResponseRedirect('/companies/')
	else:
		return render(request, 'ocean/homepage.html')
def editship(request):
	if request.method == "POST":
		with open('ocean/templates/ocean/json_data.json', mode='r', encoding='utf-8') as feedsjson:
			d = json.load(feedsjson)
		k = 0
		name = request.POST.get('editshipid')
		for i in range(0, len(d["ships"])):
			if d["ships"][i]["id"] == (int)(name):
				k = i
				break
		nameb = d["ships"][k]["name"]
		modelb = d["ships"][k]["model"]
		dateb = d["ships"][k]["date"]
		d["ships"][k]["name"] = request.POST.get('editshipname')
		d["ships"][k]["model"] = request.POST.get('editshipmodel')
		d["ships"][k]["date"] = request.POST.get('editshipdate')
		d["ships"][k]["title"] = request.POST.get('editshiptitle')
		with open('ocean/templates/ocean/json_data.json', mode='w', encoding='utf-8') as feedsjson:
			json.dump(d, feedsjson)
		file_name = 'ocean/logger/ocean/' + (str)(d["ships"][k]["owner"]) + '.txt';
		f1 = open(file_name, 'a');
		string = request.user.email + " [" + time.strftime("%H:%M %d/%m/%Y", time.localtime()) + "] " + " изменил данные о корабле " + nameb + " ( {} | {} | {} ) --> ( {} | {} | {} ).\n".format(nameb, modelb, dateb, d["ships"][k]["name"], d["ships"][k]["model"], d["ships"][k]["date"])		
		f1.write(string)
		f1.close();
		return HttpResponseRedirect('/companies/')
	else:
		return render(request, 'ocean/companies.html')
def delship(request, name=""):
	if name == "":
		return HttpResponseRedirect('/')
	else:
		with open('ocean/templates/ocean/json_data.json', mode='r', encoding='utf-8') as feedsjson:
			d = json.load(feedsjson)
		for i in range(0, len(d["ships"])):
			if d["ships"][i]["id"] == (int)(name):
				nameb = d["ships"][i]["name"]
				file_name = 'ocean/logger/ocean/' + (str)(d["ships"][i]["owner"]) + '.txt';
				del d["ships"][i]
				break
		with open('ocean/templates/ocean/json_data.json', mode='w', encoding='utf-8') as feedsjson:
			json.dump(d, feedsjson)
		f1 = open(file_name, 'a');
		string = request.user.email + " [" + time.strftime("%H:%M %d/%m/%Y", time.localtime()) + "] " + " удалил из флота корабль " + nameb + "\n."		
		f1.write(string)
		f1.close();
		return HttpResponseRedirect('/companies/')
def editco(request):
	if request.method == "POST":
		error = "ok"
		try:
			u = User.objects.get(email=request.POST.get('editcodirector'))
			if not u.director:
				error = "notdir"
		except User.DoesNotExist:
			error = "noemail"
		if not error == "ok":
			d = json.load(open('ocean/templates/ocean/json_data.json', encoding="utf8"))
			cid = request.user.company
			lastchange = {}
			lastchange["name"] = request.POST.get('editconame')
			lastchange["date"] = request.POST.get('editcodate')
			lastchange["loc"] = request.POST.get('editcolocation')
			lastchange["link"] = request.POST.get('editcolink')
			lastchange["title"] = request.POST.get('editcotitle')
			lastchange["mail"] = request.POST.get('editcodirector')
			ddict = {}
			ships = []
			for i in range(0, len(d["companies"])):
				if d["companies"][i]["id"] == cid:
					ddict = d["companies"][i]
			ud = User.objects.get(email=ddict["director"])
			for i in range(0, len(d["ships"])):
				if d["ships"][i]["owner"] == cid:
					ships.append(d["ships"][i])
			ships.sort(key=operator.itemgetter('name'))
			ddict["photo"] = ""
			try:
				u = User.objects.get(email=ddict["director"])
				ddict["photo"] = u.image.url
				ddict["birthday"] = u.date
				ddict["fullname"] = u.lastname + " " + u.firstname + " " + u.secondname 
			except User.DoesNotExist:
				ddict["photo"] = ""
			finally:
				return render(request, 'ocean/companies.html', {"dict_co":ddict, "ships":ships, "error":error, "lastinfo":lastchange})
		with open('ocean/templates/ocean/json_data.json', mode='r', encoding='utf-8') as feedsjson:
			d = json.load(feedsjson)
		k = 0
		name = request.POST.get('editcoid')
		for i in range(0, len(d["companies"])):
			if d["companies"][i]["id"] == (int)(name):
				k = i			
		if not ((d["companies"][k]["name"] == request.POST.get('editconame')) and (d["companies"][k]["date"] == request.POST.get('editcodate', '')) and (d["companies"][k]["location"] == request.POST.get('editcolocation', '')) and (d["companies"][k]["link"] == request.POST.get('editcolink', '')) and (d["companies"][k]["title"] == request.POST.get('editcotitle', '')) and (d["companies"][k]["director"] == request.POST.get('editcodirector'))):
			f1 = open('ocean/logger/ocean/' + (str)(request.user.company) + '.txt', 'a')
			string = request.user.email + " [" + time.strftime("%H:%M %d/%m/%Y", time.localtime()) + "] " + " изменил персональные данные ( {}; {}; {}; {}; {} ) --> ( {}; {}; {}; {}; {} ).\n".format(d["companies"][k]["name"], d["companies"][k]["date"], d["companies"][k]["location"], d["companies"][k]["link"], d["companies"][k]["director"], request.POST.get('editconame'), request.POST.get('editcodate'), request.POST.get('editcolocation'), request.POST.get('editcolink'), request.POST.get('editcodirector'))
			f1.write(string)
			f1.close()
		d["companies"][k]["name"] = request.POST.get('editconame')
		d["companies"][k]["date"] = request.POST.get('editcodate', '')
		d["companies"][k]["location"] = request.POST.get('editcolocation', '')
		d["companies"][k]["director"] = request.POST.get('editcodirector')
		d["companies"][k]["link"] = request.POST.get('editcolink', '')
		d["companies"][k]["title"] = request.POST.get('editcotitle', '')
		with open('ocean/templates/ocean/json_data.json', mode='w', encoding='utf-8') as feedsjson:
			json.dump(d, feedsjson)
		return HttpResponseRedirect('/companies/')
	else:
		return render(request, 'ocean/companies.html')
def profilepage(request, typeer=''):
	if request.user.date is not None:
		birthday = request.user.date.strftime('%Y-%m-%d')
		return render(request, 'ocean/profile.html', {"error":typeer, "birth":birthday})
	else:
		return render(request, 'ocean/profile.html', {"error":typeer})
def showperson(request, mail=""):
	if mail == "":
		return HttpResponseRedirect('/')
	else:
		up = User.objects.all()
		u = User()
		for i in up:
			if i.email == mail:
				u = i
				break
		if u is None:
			return HttpResponseRedirect('/')	
		if u.email == request.user.email:
			return redirect('profileer', typeer="me")
		else:
			return render(request, 'ocean/profile.html', {"mail":u})
def profilesave(request, mail=""):
	if request.method == "POST":
		lastinfo = {}
		lastinfo["ln"] = request.POST.get('editpln')
		lastinfo["fn"] = request.POST.get('editpfn')
		lastinfo["sn"] = request.POST.get('editpsn')
		lastinfo["date"] = request.POST.get('editpdate')
		if hashers.check_password("natusvincere"+request.POST.get('oldpass', ''), request.user.password):
			pass1 = request.POST.get('newpass1', '')
			pass2 = request.POST.get('newpass2', '')
			if len(pass1) < 8 and len(pass1) > 0:
				return redirect('profileer', typeer="newpass1")
			if pass1 != pass2:
				return redirect('profileer', typeer="newpass")
			else:
				person = User.objects.get(email=mail)
				f1 = open('ocean/logger/ocean/' + (str)(person.company) + '.txt', 'a')
				string = person.email + " [" + time.strftime("%H:%M %d/%m/%Y", time.localtime()) + "] " + " изменил персональные данные ( {} {} {}, {} ) --> ( {} {} {}, {} ).\n".format(person.lastname, person.firstname, person.secondname, person.date.strftime("%d.%m.%Y"), lastinfo["ln"], lastinfo["fn"], lastinfo["sn"], lastinfo["date"][8:10]+'.'+lastinfo["date"][5:7]+'.'+lastinfo["date"][0:4])
				f1.write(string)
				f1.close()
				person.lastname = lastinfo["ln"]
				person.firstname = lastinfo["fn"]
				person.secondname = lastinfo["sn"]
				person.date = lastinfo["date"]
				if len(pass1) != 0:
					person.set_password("natusvincere"+pass1)
					person.old_pass = False
				if request.FILES:
					person.image = request.FILES['editpfile']					
				person.save()
			return HttpResponseRedirect('/')
		else:
			return render(request, 'ocean/profile.html', {"error":"oldpasser","lastinfo":lastinfo})
	else:
		return render(request, 'ocean/companies.html')
def people(request, name=""):
	if name == "":
		return HttpResponseRedirect('/')
	else:
		if request.user.company == (int)(name):
			users = User.objects.all()
			people = []
			deadpeople = []
			for i in users:
				if i.company == (int)(name):
					if i.is_active == True:
						people.append(i)
					else:
						deadpeople.append(i)
			people.sort(key=operator.attrgetter('firstname'))
			people.sort(key=operator.attrgetter('lastname'))
			deadpeople.sort(key=operator.attrgetter('firstname'))
			deadpeople.sort(key=operator.attrgetter('lastname'))
			return render(request, 'ocean/people.html', {"people":people, "deadpeople":deadpeople})
		else:
			return render(request, 'ocean/people.html')
def delprofile(request, mail=""):
	if mail == "":
		return HttpResponseRedirect('/')
	else:
		if request.user.admin or request.user.director:
			try:
				u = User.objects.get(email=mail)
				u.active = False
				u.save()
				file_name = 'ocean/logger/ocean/' + (str)(u.company) + '.txt';
				f1 = open(file_name, 'a');
				string = u.email + " [" + time.strftime("%H:%M %d/%m/%Y", time.localtime()) + "] " + " был заморожен пользователем " + request.user.email + ".\n"
				string += request.user.email + " [" + time.strftime("%H:%M %d/%m/%Y", time.localtime()) + "] " + " заморозил пользоателя " + u.email + ".\n"
				f1.write(string)
				f1.close()
				if u.email == request.user.email:
					return HttpResponseRedirect('/')
				return redirect('people', name=request.user.company)
			except User.DoesNotExist:
				return render(request, 'ocean/people.html')
			except Exception as e:
				return render(request, 'ocean/people.html')
		else:
			return HttpResponseRedirect('/')
def activateprofile(request, mail=""):
	if mail == "":
		return HttpResponseRedirect('/')
	else:
		if request.user.admin or request.user.director:
			try:
				u = User.objects.get(email=mail)
				u.active = True
				u.save()
				file_name = 'ocean/logger/ocean/' + (str)(u.company) + '.txt';
				f1 = open(file_name, 'a');
				string = u.email + " [" + time.strftime("%H:%M %d/%m/%Y", time.localtime()) + "] " + " был восстановлен пользователем " + request.user.email + ".\n"
				string += request.user.email + " [" + time.strftime("%H:%M %d/%m/%Y", time.localtime()) + "] " + " восстановил пользователя " + u.email + ".\n"
				f1.write(string)
				f1.close()
				return redirect('people', name=request.user.company)
			except User.DoesNotExist:
				return render(request, 'ocean/people.html')
			except Exception as e:
				return render(request, 'ocean/people.html')
		else:
			return HttpResponseRedirect('/')
def delcompany(request, name=""):
	if name == "":
		return HttpResponseRedirect('/')
	else:
		if request.user.admin:
			with open('ocean/templates/ocean/json_data.json', mode='r', encoding='utf-8') as feedsjson:
				d = json.load(feedsjson)
			for i in range(0, len(d["companies"])):
				if d["companies"][i]["id"] == (int)(name):
					file_name = 'ocean/logger/ocean/' + (str)(d["companies"][i]["id"]) + '.txt';
					del d["companies"][i]
					break
			j = 0
			while j != len(d["ships"]):
				if d["ships"][j]["owner"] == (int)(name):
					del d["ships"][j]
					j = j-1
				j = j+1
			users = User.objects.all()
			with open('ocean/templates/ocean/json_data.json', mode='w', encoding='utf-8') as feedsjson:
				json.dump(d, feedsjson)
			f1 = open(file_name, 'a');
			for u in users:
				if u.company == (int)(name):
					u.active = False
					u.save()
					string = u.email + " [" + time.strftime("%H:%M %d/%m/%Y", time.localtime()) + "] " + " был заморожен Администратором.\n"
					f1.write(string)					
			f1.close()
			return redirect('adminpage')
		else:
			return HttpResponseRedirect('/')
def newperson(request):
	if request.method == "POST":
		mail = request.POST.get('addpmail')
		up = User.objects.all()
		k = 0;
		for i in up:
			if i.email == mail:
				k += 1
		if k == 0:
			u = User()
			u.email = mail
			u.lastname = request.POST.get('addpln')
			u.firstname = request.POST.get('addpfn')
			u.secondname = request.POST.get('addpsn', '')
			u.date = request.POST.get('addpdate')				
			if request.POST.get('addpdir') == "D":
				u.director = True
			u.company = request.user.company
			u.set_password("natusvincere"+request.POST.get('addppass'))
			if request.FILES:
				u.image = request.FILES['addpfile']
			u.save()
			file_name = 'ocean/logger/ocean/' + (str)(u.company) + '.txt';
			f1 = open(file_name, 'a');
			string = u.email + " [" + time.strftime("%H:%M %d/%m/%Y", time.localtime()) + "] " + " был зарегистрирован пользователем " + request.user.email + ".\n"
			string += request.user.email + " [" + time.strftime("%H:%M %d/%m/%Y", time.localtime()) + "] " + " зарегистрировал нового сотрудника " + u.email + ".\n"
			f1.write(string)
			f1.close()
			return redirect('people', name=u.company)
		else:
			name = request.user.company;
			users = User.objects.all()
			people = []
			deadpeople = []
			for i in users:
				if i.company == (int)(name):
					if i.is_active == True:
						people.append(i)
					else:
						deadpeople.append(i)
			people.sort(key=operator.attrgetter('firstname'))
			people.sort(key=operator.attrgetter('lastname'))
			deadpeople.sort(key=operator.attrgetter('firstname'))
			deadpeople.sort(key=operator.attrgetter('lastname'))
			lastmail = request.POST.get('addpmail')
			lastpass = request.POST.get('addppass')
			lastdate = request.POST.get('addpdate')
			lastln = request.POST.get('addpln')
			lastfn = request.POST.get('addpfn')
			lastsn = request.POST.get('addpsn', '')
			error = 'usedmail'
			return render(request, 'ocean/people.html', {"people":people, "deadpeople":deadpeople, "error":error, "lastmail":lastmail, "lastpass":lastpass, "lastdate":lastdate, "lastln":lastln, "lastfn":lastfn, "lastsn":lastsn})
	else:
		return HttpResponseRedirect('/')
def newcompany(request):
	if request.method == "POST":
		dnew = {}
		mail = request.POST.get('addcomail')
		up = User.objects.all()
		k = 0;
		for i in up:
			if i.email == mail:
				k += 1
		if k == 0:
			with open('ocean/templates/ocean/json_data.json', mode='r', encoding='utf-8') as feedsjson:
				d = json.load(feedsjson)
			d["id_co"] = d["id_co"] + 1
			dnew["id"] = d["id_co"]
			dnew["name"] = request.POST.get('addconame')
			dnew["date"] = request.POST.get('addcodate', '')
			dnew["location"] = request.POST.get('addcoloc', '')
			dnew["title"] = request.POST.get('addcotitle', '')
			dnew["director"] = request.POST.get('addcomail', '')
			dnew["link"] = request.POST.get('addcolink', '')
			d["companies"].append(dnew)
			with open('ocean/templates/ocean/json_data.json', mode='w', encoding='utf-8') as feedsjson:
				json.dump(d, feedsjson)
			file_name = 'ocean/logger/ocean/' + (str)(dnew["id"]) + '.txt';
			f1 = open(file_name, 'w');
			string = dnew["director"] + " [" + time.strftime("%H:%M %d/%m/%Y", time.localtime()) + "] " + " был зарегистрирован администратором.\n"
			f1.write(string)
			f1.close();
			u = User()
			u.email      = mail
			u.lastname   = request.POST.get('addcoln')
			u.firstname  = request.POST.get('addcofn')
			u.secondname = request.POST.get('addcosn')
			u.company    = dnew["id"]
			u.director   = True
			if request.POST.get('addcodateb'):
				u.date = request.POST.get('addcodateb')
			u.set_password("natusvincere"+request.POST.get('addcopass'))
			u.save()
			return redirect('adminpage')
		else:
			with open('ocean/templates/ocean/json_data.json', mode='r', encoding='utf-8') as feedsjson:
				d = json.load(feedsjson)
			cs = []
			users = User.objects.all()
			for i in range(0, len(d["companies"])):
				dt = {}
				dt["codata"] = d["companies"][i]
				ud = User.objects.get(email=dt["codata"]["director"])
				if ud is not None:
					dt["codata"]["director"] = ud.lastname + " " + ud.firstname + " " + ud.secondname + ", дата рождения: " + ud.date.strftime('%d.%m.%Y') + ", Email: " + ud.email;
				ships = []
				for j in range(0, len(d["ships"])):
					if d["ships"][j]["owner"] == dt["codata"]["id"]:
						ships.append(d["ships"][j])
				ships.sort(key=operator.itemgetter('name'))
				dt["ships"] = ships
				people = []
				deadpeople = []
				for k in users:
					if k.company == dt["codata"]["id"]:
						if k.active:
							people.append(k)
						else:
							deadpeople.append(k)
				people.sort(key=operator.attrgetter('firstname'))
				people.sort(key=operator.attrgetter('lastname'))
				deadpeople.sort(key=operator.attrgetter('firstname'))
				deadpeople.sort(key=operator.attrgetter('lastname'))
				dt["people"] = people
				dt["deadpeople"] = deadpeople
				cs.append(dt)
			for i in range(0, len(cs)):
				for j in range(0, len(cs)-1):
					if cs[j]["codata"]["name"].lower() > cs[j+1]["codata"]["name"].lower():
						t = cs[j]
						cs[j]=cs[j+1]
						cs[j+1]=t
			lastinfo = {}
			lastinfo["name"] = request.POST.get('addconame')
			lastinfo["date"] = request.POST.get('addcodate')
			lastinfo["loc"] = request.POST.get('addcoloc')
			lastinfo["link"] = request.POST.get('addcolink')
			lastinfo["title"] = request.POST.get('addcotitle')
			lastinfo["mail"] = request.POST.get('addcomail')
			lastinfo["pass"] = request.POST.get('addcopass')
			lastinfo["ln"] = request.POST.get('addcoln')
			lastinfo["fn"] = request.POST.get('addcofn')
			lastinfo["sn"] = request.POST.get('addcosn')
			lastinfo["dateb"] = request.POST.get('addcodateb')
			return render(request, 'ocean/adminpage.html', {"list": cs, "lastinfo":lastinfo})
	else:
		return HttpResponseRedirect('/')
def getinfo(request, mail):
	if request.user.director or request.user.admin:
		u = User.objects.get(email=mail)
		s1 = mail
		s2 = "Персональная информация: " + u.get_full_name() + "; " + (str)(u.date.strftime('%d.%m.%Y')) + "; "
		if u.director:
			s2 += "директор компании " + u.get_company() + "."
		else:
			s2 += "сотрудник компании " + u.get_company() + "."
		s3 = "Журнал действий:"
		file_name = 'ocean/logger/ocean/' + (str)(u.company) + '.txt'
		f1 = open(file_name, 'r')
		lines = []
		line = f1.readline()
		while line:
			i = line.find(" ")
			if line[0:i] == mail:
				lines.append(line[i+1:len(line)-1])
			line = f1.readline()
		f1.close()
		f2 = open('ocean/logger/ocean/temp.txt', 'w')
		f2.write(s1+"\n")
		f2.write(s2+"\n")
		f2.write(s3+"\n")
		for l in lines:
			f2.write(l+"\n")
		f2.close()
		stream = open('ocean/logger/ocean/temp.txt', 'rb')
		i = mail.find('@')
		file_name = "UFAS_" + mail 
		response = FileResponse(stream, content_type='application/txt')
		response['Content-Disposition'] = 'inline; filename={}.txt'.format(file_name)
		return response
	else:
		return HttpResponseRedirect('/')