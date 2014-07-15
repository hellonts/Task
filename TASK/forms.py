#coding=utf-8
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.models import *
from .models import *
from django.contrib.admin.widgets import FilteredSelectMultiple
class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"用户名:",
        error_messages={'required': '请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u"用户名",
                'class':'form-control',
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label=u"密   码:",
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"密码",
                'class':'form-control',
            }
        ),
    )
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"用户名和密码为必填项")
        else:
            cleaned_data = super(LoginForm, self).clean()

class AdduserForm(forms.Form):
    username = forms.CharField(required=True,max_length=20,label='用户名:',widget=forms.TextInput(attrs={'class':'form-control','text-align':'right'}),)
    first_name = forms.CharField(required=True,max_length=30,label='姓名:',widget=forms.TextInput(attrs={'class':'form-control'}),)
    last_name = forms.CharField(required=True,max_length=30,label='部门:',widget=forms.TextInput(attrs={'class':'form-control'}),)
    email = forms.EmailField(required=True,max_length=30,label='邮箱:',widget=forms.TextInput(attrs={'class':'form-control'}),)
    password = forms.CharField(required=False,max_length=20,min_length=6,label='密码:',widget=forms.PasswordInput(attrs={'class':'form-control'}),)
    is_staff = forms.BooleanField(required=False,label='该账号是否有效:',help_text='指明这个账号是否是活跃的')
    is_active = forms.BooleanField(required=False,label='该账号是否可以登录:',help_text='指明这个账号是否可以登录')
    is_superuser = forms.BooleanField(required=False,label='该账号是否管理员:',)
    user_permissions = forms.ModelMultipleChoiceField(label='该用户权限:',required=False,queryset=Permission.objects.all(),widget=forms.CheckboxSelectMultiple(attrs={}))
    last_login = forms.DateTimeField(label='上次登录时间:',required=False,widget=forms.DateTimeInput(attrs={'class':'form-control','id':'last_login'}))
    date_joined = forms.DateTimeField(label='创建时间:',required=False,widget=forms.DateTimeInput(attrs={'class':'form-control','id':'date_joined'}))
    class Meta:
	model = User
class TaskForm(forms.Form):
    demand_status = forms.IntegerField(required=False,label='紧急状态:',widget=forms.TextInput(attrs={'class':'form-control'}))
    completion_time = forms.DateTimeField(required=False,label='任务申请完成时间:',widget=forms.DateTimeInput(attrs={'class':'form-control','value':''}),)

    vmusage = forms.CharField(required=True,label='虚拟机用途:',widget=forms.TextInput(attrs={'class':'form-control'}))
    vmstarttime = forms.DateTimeField(required=True,label='虚拟机启动时间:',widget=forms.DateTimeInput(attrs={'class':'form-control'}),)
    vm_cpu_core = forms.IntegerField(required=True,label='虚拟机cpu核数:',widget=forms.TextInput(attrs={'class':'form-control','value':'0'}))
    vm_mem = forms.IntegerField(required=True,label='虚拟机内存大小(G):',widget=forms.TextInput(attrs={'class':'form-control','value':'0'}))
    vm_disk = forms.IntegerField(required=True,label='虚拟机磁盘大小(G):',widget=forms.TextInput(attrs={'class':'form-control','value':'0'}))
    vm_ip = forms.IPAddressField(required=False,label='虚拟机ip地址:',widget=forms.TextInput(attrs={'class':'form-control'}))
    vm_life_cycle = forms.IntegerField(required=True,label='资源使用周期(月):',widget=forms.TextInput(attrs={'class':'form-control','value':'0'}))

    messages = forms.CharField(required=False,max_length=80,label='备注:',widget=forms.Textarea(attrs={'class':'form-control','rows':'5','cols':'6','style':'resize:none'}))
    task_status = forms.IntegerField(required=False,label='任务状态:',widget=forms.TextInput(attrs={'class':'form-control'}))



