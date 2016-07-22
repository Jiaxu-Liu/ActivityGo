#coding = utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django import forms
from activity.models import User

#表单
class UserForm(forms.Form):
	username = forms.CharField(label = 'username', max_length = 100)
	password = forms.CharField(label = 'password', max_length = 100, widget=forms.PasswordInput())
	email = forms.CharField(label='email',max_length = 100)
	phone = forms.CharField(label='phone',max_length=100)


#注册账号
def Register(Req):
	if Req.method == 'POST':
		u = UserForm(Req.POST)
		if u.is_valid():
			#访问表单数据，并转换为正确的格式
			un = u.cleaned_data['username']
			pw = u.cleaned_data['password']
			email = u.cleaned_data['email']
			phone = u.cleaned_data['phone']
			#表单数据与数据库进行比较
			user = User.objects.filter(username__exact = un)
			if user:
				#若已经被注册了
				return HttpResponse('该用户名已被注册')
			else:
				#添加至数据库
				User.objects.create(username = un, password =  pw,email=email,phone=phone)
				return HttpResponse('Regist Success')
	else:
		u = UserForm()
	return render_to_response('regist.html', {'uf':u}, context_instance=RequestContext(Req))

#登录界面
def  LogIn(Req):
	if Req.method == 'POST':
		u = UserForm(Req.POST)
		if u.is_valid():
			#获取表单数据，并转换为正确格式
			un = u.cleaned_data['username']
			pw = u.cleaned_data['password']
			#与数据库进行比较
			user = User.objects.filter(username__exact = un, password__exact = pw)
			if user:
				#比较成功，跳转登录成功界面
				response = HttpResponseRedirect('/index/')
				#将用户名写入cookie
				response.set_cookie('username', un, 1800)
				return response
			else:
				#比较失败，还在login界面，显示失败信息
				return HttpResponseRedirect('/login/')
	else:
		u = UserForm()
	return render_to_response('login.html', {'uf':u}, context_instance=RequestContext(Req))

#登陆成功
def index(Req):
	un = Req.COOKIES.get('username', '')
	return render_to_response('index.html', {'username': un})

#注销登录
def LogOut(Req):
	response = HttpResponseRedirect('/login/')
	#清除cookie
	response.delete_cookie('username')
	return response