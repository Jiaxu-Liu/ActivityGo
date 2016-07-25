from django import forms

#表单
class UserForm(forms.Form):
	username = forms.CharField(label = 'username', max_length = 100)
	password = forms.CharField(label = 'password', max_length = 100, widget=forms.PasswordInput())
	email = forms.CharField(label='email',max_length = 100)
	phone = forms.CharField(label='phone',max_length=100)
	headImg = forms.FileField(label = 'headimg')

class ChangePasswordForm(forms.Form):
	oldpassword = forms.CharField(label = 'old password', max_length = 100, widget = forms.PasswordInput())
	newpassword = forms.CharField(label = 'new password', max_length = 100, widget = forms.PasswordInput())
	

class LogInUserForm(forms.Form):
	username = forms.CharField(label = 'username', max_length = 100)
	password = forms.CharField(label = 'password', max_length = 100, widget=forms.PasswordInput())

class ChangeEmailForm(forms.Form):
	newemail = forms.CharField(label = 'new email', max_length = 100)
    
class ChangePhoneForm(forms.Form):
	newphone = forms.CharField(label = 'new phone', max_length = 100)

class ChangeImgForm(forms.Form):
	newheadimg = forms.FileField(label = 'new headimg')
    
class ShowInfoForm(forms.Form):
    username = forms.CharField(label = 'username', max_length = 100)
    email = forms.CharField(label='email',max_length = 100)
    phone = forms.CharField(label='phone',max_length=100)
    headImg = forms.FileField(label = 'headimg')
