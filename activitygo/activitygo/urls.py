"""activitygo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'activity.views.indexNoUser'),
    url(r'^login/','activity.views.LogIn'),
    url(r'^regist/','activity.views.Register'),
    url(r'^index/','activity.views.index'),
    url(r'^index_nouser/','activity.views.indexNoUser'),
    url(r'^logout/','activity.views.LogOut'),
    url(r'^changepassword/','activity.views.ChangePassword'),
    url(r'^changeemail/','activity.views.ChangeEmail'),
    url(r'^changephone/','activity.views.ChangePhone'),
    url(r'^changeheadimg/','activity.views.ChangeHeadImg'),
    url(r'^showinfo/','activity.views.ShowInfo'),
    url(r'^changesuccess/','activity.views.ChangeSuccess'),
    url(r'^registsuccess/','activity.views.RegistSuccess'),
    url(r'^organizesuccess/','activity.views.OrganizeSuccess'),
    url(r'^me_joinactivity/','activity.views.MeJoinActivity'),
    url(r'^me_organizeactivity/','activity.views.MeOrganizeActivity'),
    url(r'^organizeactivity/','activity.views.OrganizeActivity'),
    url(r'^joinactivity/','activity.views.JoinActivity'),
    url(r'^list/', 'activity.views.Search'),
    url(r'^activity/static/(?P<path>.*)', 'django.views.static.serve', {'document_root': 'activity/static/'})
]

