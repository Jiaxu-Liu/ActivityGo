#coding = utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from activity.models import User, Activities
from activity.form import UserForm, ChangePasswordForm, LogInUserForm, ChangeImgForm, ChangeEmailForm, ChangePhoneForm, ShowInfoForm, CreateActivityForm, SearchForm

from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import math

#注册账号
def Register(Req):
	if Req.method == 'POST':
		u = UserForm(Req.POST, Req.FILES)
		if u.is_valid():
			#访问表单数据，并转换为正确的格式
			un = u.cleaned_data['username']
			pw = u.cleaned_data['password']
			cpw = u.cleaned_data['checkpassword']
			email = u.cleaned_data['email']
			phone = u.cleaned_data['phone']
			headImg = u.cleaned_data['headImg']
			#表单数据与数据库进行比较
			user = User.objects.filter(username__exact = un)
			if user:
				#若已经被注册了
				return HttpResponse('该用户名已被注册')
			else:
				if (pw == cpw):
					#添加至数据库
					u1 = User()
					u1.username = un
					u1.password = pw
					u1.email = email
					u1.phone = phone
					u1.headImg = headImg
					u1.save()
					return HttpResponseRedirect('/registsuccess/')
				else:
					return HttpResponse('两次输入密码不一致')
	else:
		u = UserForm()
	return render_to_response('regist.html', {'uf':u}, context_instance=RequestContext(Req))

#修改头像
def ChangeHeadImg(Req):
	un = Req.COOKIES.get('username', '')
	if Req.method == 'POST':
		chif = ChangeImgForm(Req.POST, Req.FILES)
		if chif.is_valid():
			un = Req.COOKIES.get('username', '')
			nhi = chif.cleaned_data['newheadimg']
			user = User.objects.filter(username__exact = un)
			if user:
				u1 = User.objects.get(username = un)
				u1.headImg = nhi
				u1.save()
				return HttpResponseRedirect('/changesuccess/')
			else:
				#比较失败，还在changeheadimg界面
				return HttpResponseRedirect('/changeheadimg/') 
	else:
		chif = ChangeImgForm()
	return render_to_response('changeheadimg.html', {'chif':chif, 'username': un}, context_instance=RequestContext(Req))

#登录界面
def  LogIn(Req):
	if Req.method == 'POST':
		u = LogInUserForm(Req.POST)
		if u.is_valid():
			#获取表单数据，并转换为正确格式
			un = u.cleaned_data['username']
			pw = u.cleaned_data['password']
            
			#un = Req.POST['InputUsername']
			#pw = Req.POST['InputPassword']
            
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
				return HttpResponseRedirect('/index_nouser/')
	else:
		u = LogInUserForm()
	return render_to_response('login.html', {'uf':u}, context_instance=RequestContext(Req))

#登陆成功
def index(Req):
	all_activities = Activities.objects.all()
	un = Req.COOKIES.get('username', '')
    #分页
	ONE_PAGE_OF_DATA = 10  
    
	try:  
		curPage = int(Req.GET.get('curPage', '1'))  
		allPage = int(Req.GET.get('allPage','1'))  
		pageType = str(Req.GET.get('pageType', ''))  
	except ValueError:  
		curPage = 1  
		allPage = 1  
		pageType = ''  
    
    #判断点击了【下一页】还是【上一页】  
	if pageType == 'pageDown':  
		curPage += 1  
	elif pageType == 'pageUp':  
		curPage -= 1  
	startPos = (curPage - 1) * ONE_PAGE_OF_DATA  
	endPos = startPos + ONE_PAGE_OF_DATA  
	posts = Activities.objects.all()[startPos:endPos]  
    
	if curPage == 1 and allPage == 1: 
		allPostCounts = Activities.objects.filter(astatus__exact = 1).count()  
		allPage = math.ceil(allPostCounts / ONE_PAGE_OF_DATA)   
    #分页
	return render_to_response('index.html', {'username': un, 'all_activities': all_activities, 'posts':posts, 'allPage':allPage, 'curPage':curPage},context_instance=RequestContext(Req))

#未登录的主页
def indexNoUser(Req):
	all_activities = Activities.objects.all()
	un = Req.COOKIES.get('username', '')
	#分页
	ONE_PAGE_OF_DATA = 10  
    
	try:  
		curPage = int(Req.GET.get('curPage', '1'))  
		allPage = int(Req.GET.get('allPage','1'))  
		pageType = str(Req.GET.get('pageType', ''))  
	except ValueError:  
		curPage = 1  
		allPage = 1  
		pageType = ''  
    
    #判断点击了【下一页】还是【上一页】  
	if pageType == 'pageDown':  
		curPage += 1  
	elif pageType == 'pageUp':  
		curPage -= 1  
	startPos = (curPage - 1) * ONE_PAGE_OF_DATA  
	endPos = startPos + ONE_PAGE_OF_DATA  
	posts = Activities.objects.all()[startPos:endPos]  
    
	if curPage == 1 and allPage == 1: 
		allPostCounts = Activities.objects.filter(astatus__exact = 1).count() 
		allPage = math.ceil(allPostCounts / ONE_PAGE_OF_DATA)   
    #分页
	
	return render_to_response('index_nouser.html', {'username': un, 'all_activities': all_activities, 'posts':posts, 'allPage':allPage, 'curPage':curPage},context_instance=RequestContext(Req))

#注销登录
def LogOut(Req):
	response = HttpResponseRedirect('/index_nouser/')
	#清除cookie
	response.delete_cookie('username')
	return response

#修改密码
def ChangePassword(Req):
	un = Req.COOKIES.get('username', '')
	if Req.method == 'POST':
		cpf = ChangePasswordForm(Req.POST)
		if cpf.is_valid():
			un = Req.COOKIES.get('username', '')
			op = cpf.cleaned_data['oldpassword']
			np = cpf.cleaned_data['newpassword']
			cnp = cpf.cleaned_data['checknewpassword']
			user = User.objects.filter(username__exact = un, password__exact = op)
			if user:
				if (np == cnp):
					User.objects.filter(username = un).update(password = np)
					
					return HttpResponseRedirect('/changesuccess/')
				else:
					return HttpResponse('两次输入密码不一致')
			else:
				#比较失败，还在changepassword界面
				return HttpResponseRedirect('/changepassword/') 
	else:
		cpf = ChangePasswordForm()
	return render_to_response('changepassword.html', {'cpf':cpf, 'username': un}, context_instance=RequestContext(Req))

#修改邮箱
def ChangeEmail(Req):
	un = Req.COOKIES.get('username', '')
	if Req.method == 'POST':
		cef = ChangeEmailForm(Req.POST)
		if cef.is_valid():
			un = Req.COOKIES.get('username', '')
			ne = cef.cleaned_data['newemail']
			
			user = User.objects.filter(username__exact = un)
			if user:
				User.objects.filter(username = un).update(email = ne)
				
				return HttpResponseRedirect('/changesuccess/')
			else:
				#比较失败，还在changeemail界面
				return HttpResponseRedirect('/changeemail/') 
	else:
		cef = ChangeEmailForm()
	return render_to_response('changeemail.html', {'cef':cef, 'username': un}, context_instance=RequestContext(Req))

#修改电话
def ChangePhone(Req):
	un = Req.COOKIES.get('username', '')
	if Req.method == 'POST':
		cpf = ChangePhoneForm(Req.POST)
		if cpf.is_valid():
			un = Req.COOKIES.get('username', '')
			np = cpf.cleaned_data['newphone']
			
			user = User.objects.filter(username__exact = un)
			if user:
				User.objects.filter(username = un).update(phone = np)
				
				return HttpResponseRedirect('/changesuccess/')
			else:
				#比较失败，还在changephone界面
				return HttpResponseRedirect('/changephone/') 
	else:
		cpf = ChangePhoneForm()
	return render_to_response('changephone.html', {'cpf':cpf, 'username': un}, context_instance=RequestContext(Req))

#查看信息
def ShowInfo(Req):
    un = Req.COOKIES.get('username', '')
    sif = User.objects.get(username = un)
    return render_to_response('showinfo.html', {'sif':sif, 'username': un}, context_instance=RequestContext(Req))

#修改信息成功
def ChangeSuccess(Req):
	un = Req.COOKIES.get('username', '')
	return render_to_response('changesuccess.html',  {'username': un})

#注册成功
def RegistSuccess(Req):
	return render_to_response('registsuccess.html')

#创建活动成功
def OrganizeSuccess(Req):
	un = Req.COOKIES.get('username','')
	return render_to_response('organizesuccess.html',  {'username': un})

#我参与的活动
def MeJoinActivity(Req):
	un = Req.COOKIES.get('username', '')
	user = User.objects.get(username=un)
	#print(user.email)
	posts = user.activities_set.all()
	return render_to_response('me_joinactivity.html', {'username': un,'posts':posts})

#我组织的活动
def MeOrganizeActivity(Req):
	un = Req.COOKIES.get('username', '')
	acts = Activities.objects.filter(aorganiser = un)
	act_flag = ""
	if acts:
		act_flag = "1"
    #分页
	ONE_PAGE_OF_DATA = 10  
    
	try:  
		curPage = int(Req.GET.get('curPage', '1'))  
		allPage = int(Req.GET.get('allPage','1'))  
		pageType = str(Req.GET.get('pageType', ''))  
	except ValueError:  
		curPage = 1  
		allPage = 1  
		pageType = ''  
    
    #判断点击了【下一页】还是【上一页】  
	if pageType == 'pageDown':  
		curPage += 1  
	elif pageType == 'pageUp':  
		curPage -= 1  
	startPos = (curPage - 1) * ONE_PAGE_OF_DATA  
	endPos = startPos + ONE_PAGE_OF_DATA  
	posts = Activities.objects.filter(aorganiser = un)[startPos:endPos]  
    
	if curPage == 1 and allPage == 1: 
		allPostCounts = Activities.objects.filter(aorganiser = un).count()  
		allPage = math.ceil(allPostCounts / ONE_PAGE_OF_DATA)   
    #分页
	return render_to_response('me_organizeactivity.html', {'username': un, 'acts':acts, 'act_flag': act_flag, 'posts':posts, 'allPage':allPage, 'curPage':curPage})

#创建活动
def OrganizeActivity(Req):
	un = Req.COOKIES.get('username','')
	if Req.method == 'POST':
		crf = CreateActivityForm(Req.POST)
		if crf.is_valid():
			un = Req.COOKIES.get('username','')
			an = crf.cleaned_data['aname']
			ad = crf.cleaned_data['adate']
			ap = crf.cleaned_data['alocation']
			ade = crf.cleaned_data['adescription']
			Activities.objects.create(aname=an,adate=ad,alocation=ap,adescription=ade,aorganiser=un)
            
			return HttpResponseRedirect('/organizesuccess/')
	else:
		crf = CreateActivityForm()
	return render_to_response('organizeactivity.html',{'crf':crf, 'username': un},context_instance=RequestContext(Req))

#参与活动
def JoinActivity(Req):
	all_activities = Activities.objects.all()
	un = Req.COOKIES.get('username', '')
	join_flag = 0
    #分页
	ONE_PAGE_OF_DATA = 10  
    
	try:  
		curPage = int(Req.GET.get('curPage', '1'))  
		allPage = int(Req.GET.get('allPage','1'))  
		pageType = str(Req.GET.get('pageType', ''))  
	except ValueError:  
		curPage = 1  
		allPage = 1  
		pageType = ''  
    
    #判断点击了【下一页】还是【上一页】  
	if pageType == 'pageDown':  
		curPage += 1  
	elif pageType == 'pageUp':  
		curPage -= 1  
	startPos = (curPage - 1) * ONE_PAGE_OF_DATA  
	endPos = startPos + ONE_PAGE_OF_DATA  
	posts = Activities.objects.all()[startPos:endPos]  
    
	if curPage == 1 and allPage == 1: 
		allPostCounts = Activities.objects.filter(astatus__exact = 1).count()  
		allPage = math.ceil(allPostCounts / ONE_PAGE_OF_DATA)   
    #分页
	return render_to_response('joinactivity.html', {'username': un, 'all_activities': all_activities, 'posts':posts, 'allPage':allPage, 'curPage':curPage, 'join_flag': join_flag},context_instance=RequestContext(Req))
#检索
def Search(Req):
	sf = Req.GET.get('searchcontents', '')
	un = Req.COOKIES.get('username', '')
	start_flag = ""
	if sf:
		acts = Activities.objects.filter(Q(adescription__contains= sf)|Q(aname__contains = sf)|Q(aorganiser__contains = sf)|Q(alocation__contains = sf))
	else:
		acts = []
		start_flag = "1"
    #分页
	ONE_PAGE_OF_DATA = 10  
    
	try:  
		curPage = int(Req.GET.get('curPage', '1'))  
		allPage = int(Req.GET.get('allPage','1'))  
		pageType = str(Req.GET.get('pageType', ''))  
	except ValueError:  
		curPage = 1  
		allPage = 1  
		pageType = ''  
    
    #判断点击了【下一页】还是【上一页】  
	if pageType == 'pageDown':  
		curPage += 1
		acts = Activities.objects.filter(Q(adescription__contains= sf)|Q(aname__contains = sf)|Q(aorganiser__contains = sf)|Q(alocation__contains = sf))
	elif pageType == 'pageUp':  
		curPage -= 1
		acts = Activities.objects.filter(Q(adescription__contains= sf)|Q(aname__contains = sf)|Q(aorganiser__contains = sf)|Q(alocation__contains = sf)) 
	startPos = (curPage - 1) * ONE_PAGE_OF_DATA  
	endPos = startPos + ONE_PAGE_OF_DATA  
	posts = Activities.objects.filter(Q(adescription__contains= sf)|Q(aname__contains = sf)|Q(aorganiser__contains = sf)|Q(alocation__contains = sf))[startPos:endPos]  
    
	if curPage == 1 and allPage == 1: 
		allPostCounts = Activities.objects.filter(Q(adescription__contains= sf)|Q(aname__contains = sf)|Q(aorganiser__contains = sf)|Q(alocation__contains = sf)).filter(astatus__exact = 1).count()
		allPage = math.ceil(allPostCounts / ONE_PAGE_OF_DATA)   
    #分页
	return render_to_response('list.html', {'username': un, 'acts': acts, 'startflag': start_flag, 'posts':posts, 'allPage':allPage, 'curPage':curPage})

#加入活动
def join(Req, id):
	un = Req.COOKIES.get('username', '')
	post = Activities.objects.get(id = str(id))
	us = User.objects.get(username=un)
	post.aparticipants.add(us)
	post.aparticipantnum = post.aparticipantnum+1
	post.save()
	return render_to_response('joinsuccess.html',{'username': un})

#活动详情
def Detail(Req, id):
    organizer_flag = ""
    join_flag = ""
    un = Req.COOKIES.get('username', '')
    act = Activities.objects.get(id = str(id))
    organizer = User.objects.get(username = act.aorganiser)
    joinact = None
    if act.aparticipants.all():
        joinact = act.aparticipants.all().get(username = un)
    if joinact:
        join_flag = ""
    else:
        join_flag = "1"
    if un == act.aorganiser:
        organizer_flag = ""
    else:
        organizer_flag = "1"
    return render_to_response('detail.html',{'username': un, 'act': act, 'organizer_flag': organizer_flag, 'organizer': organizer, 'join_flag': join_flag})

#活动详情 未登录
def DetailNoUser(Req, id):
    un = Req.COOKIES.get('username', '')
    act = Activities.objects.get(id = str(id))
    return render_to_response('detail_nouser.html',{'username': un, 'act': act, })
    
#组织者信息
def OrganizerDetail(Req, id):
    un = Req.COOKIES.get('username', '')
    organizer = User.objects.get(id = str(id))
    return render_to_response('organizerdetail.html',{'username': un, 'organizer': organizer})