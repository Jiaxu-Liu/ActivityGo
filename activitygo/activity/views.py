#coding = utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from activity.models import User
from activity.form import UserForm, ChangePasswordForm


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

#修改密码
def ChangePassword(Req):
	if Req.method == 'POST':
		cpf = ChangePasswordForm(Req.POST)
		if cpf.is_valid():
			un = Req.user.username
			op = cpf.cleaned_data['oldpassword']
			np = cpf.cleaned_data['newpassword']
			user = User.objects.filter(username__exact = un, password__exact = op)
			if user:
				user.set_password(newpassword)
				user.save()
				return HttpResponse('修改成功')
			else:
				#比较失败，还在changepassword界面
				return HttpResponseRedirect('/changepassword/') 
	else:
		cpf = ChangePasswordForm()
	return render_to_response('changepassword.html', {'cpf':cpf}, context_instance=RequestContext(Req))
