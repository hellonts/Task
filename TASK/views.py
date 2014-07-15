# Create your views here.
#coding=utf-8
from django.shortcuts import render_to_response, render, get_object_or_404
from TASK.models import *
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms.formsets import formset_factory
from django.utils import simplejson


from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *
import json, os, time, sys
from datetime import datetime
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage




# admin_login
def login(request):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if request.method == 'GET':
        form = LoginForm()
	cform = AdduserForm()
	
        return render_to_response('login.html', RequestContext(request, locals()))
    else:
	if request.POST.has_key('login'):
            form = LoginForm(request.POST)
            if form.is_valid():
                user = request.POST.get('username', '')
                password = request.POST.get('password', '')
                user = auth.authenticate(username=user, password=password)
		if user is not None and user.is_active and user.is_staff:
		    request.session['username']=user		
		    auth.login(request, user)
		    return HttpResponseRedirect('/TASK/admin/index/')
                elif user is not None and user.is_active:
		
                    return render_to_response('login.html', RequestContext(request, {'form': form,'disabled':True}))
		else:
		    return render_to_response('login.html', RequestContext(request, {'form': form,'password_is_wrong':True}))
            elif not form.is_valid():
                return render_to_response('login.html', RequestContext(request, {'form': form,'user_is_none':True}))


	elif request.POST.has_key('useradd'):
     	    cform = AdduserForm(request.POST)
            form = LoginForm()
	    if cform.is_valid():
		cd = cform.cleaned_data
            	username = cd['username']
                check = User.objects.filter(username__exact = username)
            	if check:
                    result ="该用户已被注册，请选择另外一个"
                    return render_to_response('login.html', RequestContext(request,locals()))
                first_name = cd['first_name']
                last_name = cd['last_name']
                email = cd['email']
                password = cd['password']
                staff = 1
                active = 1
                user = User.objects.create_user(username = username, password = password, email = email)
		user_permissions=(22,23)
                for i in user_permissions:
                    user.user_permissions.add(i)
                    user.save()
		user.save
                ID = user.id
                User.objects.filter(id=ID).update(first_name = first_name, last_name = last_name, is_staff = staff, is_active = active)

	        user = auth.authenticate(username=username, password=password)
	        auth.login(request, user)
                return HttpResponseRedirect('/TASK/admin/index/') 

            else:
                return render_to_response('login.html', RequestContext(request, locals()))



@login_required
def logout(request):
    del request.session['username']
    auth.logout(request)
    return HttpResponseRedirect("login/")

@login_required
def bglist(request):
    username = request.user.username
    user = User.objects.get(username=username)
    ID = user.id
    name = user.first_name
    if ID == 1:
	if name =='':
	    data = '请更新姓名,职位等信息.'
    message = Messages.objects.filter(touser=name,status=0).count()
    return render_to_response('admin_bglist.html', RequestContext(request, locals()))



@login_required 
def user(request):
    username = request.user.username
    name = User.objects.get(username=username).first_name
    message = Messages.objects.filter(touser=name,status=0).count()
    users = User.objects.all()
    paginator = Paginator(users,6)
    page = request.GET.get('page')
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except (EmptyPage,InvalidPage):
        pages = paginator.page(paginator.num_pages)
    if request.method == 'POST':
	if request.POST.has_key('delete'):
	    idlist = request.POST.getlist('answer','')
	    for i in idlist:
		user = User.objects.get(id=i)
		user.delete()

	return HttpResponseRedirect('/TASK/admin/user/')
    else:
	return render_to_response('admin_user.html', RequestContext(request, locals()))

@login_required
def user_add(request):
    username = request.user.username
    name = User.objects.get(username=username).first_name
    message = Messages.objects.filter(touser=name,status=0).count()
    if request.method == 'POST':
        form = AdduserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
	    check = User.objects.filter(username__exact = username)
	    if check:	
		result ="该用户已被注册，请选择另外一个"
	        return render_to_response('admin_useradd.html', RequestContext(request, locals()))
# 	    else:
	        #result ="""{"result":false}"""
#		pass
            first_name = cd['first_name']
            last_name = cd['last_name']
            email = cd['email']
            password = cd['password']
	    is_staff = request.POST.get('is_staff')
            if is_staff == 'on':
                staff = 1
            else:
                staff = 0
            is_active = request.POST.get('is_active')
            if is_active == 'on':
                active = 1
            else:
                active = 0
	    user_permissions = request.POST.getlist('user_permissions')
            user = User.objects.create_user(username = username, password = password, email = email)
            user.save
	    ID = user.id
            User.objects.filter(id=ID).update(first_name = first_name, last_name = last_name, is_staff = staff, is_active = active)
	    user = User.objects.get(id=ID)
	    if user_permissions != '':
	        for i in user_permissions:
                    user.user_permissions.add(i)
                    user.save()
            return HttpResponseRedirect('/TASK/admin/user/')

        else:
            return render_to_response('admin_useradd.html', RequestContext(request, locals()))    
    else:
	form = AdduserForm()
    return render_to_response('admin_useradd.html', RequestContext(request, locals()))

@login_required
def user_update(request,id=''):
    username = request.user.username
    name = User.objects.get(username=username).first_name
    message = Messages.objects.filter(touser=name,status=0).count()
    if request.method == 'POST':
        if request.POST.has_key('setnewpass'):
	    newpass = request.POST.get('newpass')
	    user = User.objects.get(id=id)
	    user.set_password(newpass)
	    user.save()
	    return HttpResponseRedirect("/TASK/admin/user/%s" % id) 
	else:	
	    form = AdduserForm(request.POST)
	    if form.is_valid():
	        cd = form.cleaned_data
	        username = cd['username']
	        first_name = cd['first_name']
	        last_name = cd['last_name'] 
	        email = cd['email']
	        is_staff = request.POST.get('is_staff')
	        if is_staff == 'on':
	            staff = 1
	        else:
		    staff = 0
	        is_active = request.POST.get('is_active')
	        if is_active == 'on':
		    active = 1
	        else:
		    active = 0
	        is_superuser = request.POST.get('is_superuser')
		if is_superuser == 'on':
		    superuser = 1
		else:
		    superuser = 0
	        user_permissions = request.POST.getlist('user_permissions')
	        last_login = cd['last_login']
	        date_joined = cd['date_joined']
	        User.objects.filter(id=id).update(username = username, first_name = first_name, last_name = last_name, 
		email = email, is_staff = staff, is_active = active, is_superuser = superuser)
	        user = User.objects.get(id=id)
	        user.user_permissions.clear()
	        for i in user_permissions:
		    user.user_permissions.add(i)
		    user.save()
		



     
	
	       # return HttpResponseRedirect("/TASK/admin/user/")
	        return render_to_response('admin_userupdate.html', RequestContext(request, locals()))
	    else:
	        return render_to_response('admin_userupdate.html', RequestContext(request, locals()))
    else:
    	user = User.objects.get(id=id)
	form = AdduserForm(initial={'username': user.username,
	'first_name': user.first_name,'last_name': user.last_name,'email': user.email, 'is_staff': user.is_staff,
	'is_active': user.is_active, 'is_superuser': user.is_superuser,'user_permissions': user.user_permissions.all(),'last_login':user.last_login,
	'date_joined': user.date_joined}) 
	return render_to_response('admin_userupdate.html', RequestContext(request, locals()))



@login_required
def task_add(request):
    username = request.user.username
    name = User.objects.get(username=username).first_name
    message = Messages.objects.filter(touser=name,status=0).count()
    super = User.objects.filter(is_superuser = 1)
    items = []
    superid = []
    supername = []
    for i in super:
        first_name = User.objects.get(username=i).first_name
        id = User.objects.get(username=i).id
	supername.append(first_name)
	superid.append(id)
    for i,value in enumerate(supername):
	list = {}
	list['name']=supername[i]
        list['id']=superid[i]
	items.append(list)
    if request.method == 'POST':
	reload(sys)
        sys.setdefaultencoding('utf-8')
        from subprocess import Popen, PIPE
        form = TaskForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
	    name = User.objects.get(username = username).first_name
	    frommail = User.objects.get(username = username).email
	    Touser = request.POST.get('touser')
	    if Touser == '':
		touser = '管理员'
	    else:
		touser = Touser
	    tomail = User.objects.get(first_name = first_name).email
	    demand_status = request.POST.get('demand_status')
	    if demand_status == '':
		demand_status = 1
	    else:
		demand_status = demand_status
	    completion_time = request.POST.get('completion_time') 
	    vmusage = cd['vmusage']
	    vmstarttime = cd['vmstarttime']
	    vm_cpu_core = cd['vm_cpu_core']
	    vm_mem = cd['vm_mem']
	    vm_disk = cd['vm_disk']
	    vm_ip = cd['vm_ip']
	    vm_life_cycle = cd['vm_life_cycle']
	    vm_status = 1
	    messages = cd['messages']
	    task_status = 1
	    task = Task(fromuser = name, touser = touser, completion_time = completion_time, vmstarttime = vmstarttime, demand_status = demand_status, vmusage = vmusage,  vm_cpu_core = vm_cpu_core,vm_mem = vm_mem, vm_disk = vm_disk, vm_ip = vm_ip, vm_life_cycle = vm_life_cycle, vm_status = vm_status, messages = messages, task_status = task_status)
	    task.save()
	    taskid = Task.objects.order_by('-id')[0].id
	    fromuser = name
	    touser = touser
	    
	    message =  Messages(taskid = taskid, fromuser = fromuser, touser = touser, title = vmusage, content = messages)
	    message.save() 
	    if messages == '':
		mess = '虚拟机资源申请'
	    else:
		mess = messages
	    cmd = "%s %s %s %s |%s -s 'VM资源申请' %s"% ('echo',mess,name,frommail,'mail',tomail)
	    p = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)

	   
	    return HttpResponseRedirect("/TASK/admin/tasklist/")

	else:
	    return render_to_response('admin_taskadd.html', RequestContext(request, locals()))
    else:
	form = TaskForm()

	return render_to_response('admin_taskadd.html', RequestContext(request, locals()))

@login_required
def task_list(request):
    username = request.user.username
#    username=request.session.get('username','')
    name = User.objects.get(username=username).first_name
    message = Messages.objects.filter(touser=name,status=0).count()
    task = Task.objects.all().order_by('-id')
    paginator = Paginator(task,6)
    page = request.GET.get('page')
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except (EmptyPage,InvalidPage):
        pages = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        if request.POST.has_key('delete'):
	    idlist = request.POST.getlist('answer','')
            for i in idlist:
                task = Task.objects.get(id=i)
                task.delete()	    
    

    return render_to_response('admin_tasklist.html', RequestContext(request, locals()))


@login_required
def task_get(request):
    username = request.user.username
    name = User.objects.get(username=username).first_name
    message = Messages.objects.filter(touser=name,status=0).count()
    first_name = User.objects.get(username=username).first_name
    task = Task.objects.filter(touser=first_name).order_by('-id')
    paginator = Paginator(task,6)
    page = request.GET.get('page')
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except (EmptyPage,InvalidPage):
        pages = paginator.page(paginator.num_pages)

    return render_to_response('admin_taskget.html', RequestContext(request, locals()))


@login_required
def task_post(request):
    username = request.user.username
    name = User.objects.get(username=username).first_name
    message = Messages.objects.filter(touser=name,status=0).count()
    first_name = User.objects.get(username=username).first_name
    task = Task.objects.filter(fromuser=first_name).order_by('-id')
    paginator = Paginator(task,6)
    page = request.GET.get('page')
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except (EmptyPage,InvalidPage):
        pages = paginator.page(paginator.num_pages)

    return render_to_response('admin_taskpost.html', RequestContext(request, locals()))

@login_required
def task_processing(request,id=''):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    username = request.user.username
    name = User.objects.get(username=username).first_name
    message = Messages.objects.filter(touser=name,status=0).count()
    task = Task.objects.get(id=id)
    taskfromuser = task.fromuser
    tasktouser = task.touser
    if name == taskfromuser or name == tasktouser :
	check = 'check'
    task_reply = Task_reply.objects.filter(taskid=id).order_by('-id')
    


    paginator = Paginator(task_reply,6)
    page = request.GET.get('page')
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except (EmptyPage,InvalidPage):
        pages = paginator.page(paginator.num_pages)
    if request.method == 'POST':
	if request.POST.has_key('accept'):
	    taskstatus = request.POST.get('task_status')
	    if taskstatus == '2':
		Mess = '%s接受了任务.'% name
	    elif taskstatus == '3':
		Mess = '%s完成了任务.'% name
		vmstatus =  request.POST.get('vm_status')
		Vmstatus = int(vmstatus)
		Task.objects.filter(id=id).update(vm_status='%d'% Vmstatus)
	    status = int(taskstatus)
	    Task.objects.filter(id=id).update(task_status='%d'% status)
	    reply = Task_reply(taskid = id, fromuser = username, touser = taskfromuser, content = Mess)
	    reply.save()
	elif request.POST.has_key('content'):
	    fromuser = username
	    contents = request.POST.get('messages')
	    touser = taskfromuser
	    reply = Task_reply(taskid = id, fromuser = fromuser, touser = touser, content = contents)
	    reply.save()
	    task_reply = Task_reply.objects.filter(taskid=id).order_by('-id')
	    paginator = Paginator(task_reply,6)
    	    page = request.GET.get('page')
    	    try:
        	pages = paginator.page(page)
    	    except PageNotAnInteger:
        	pages = paginator.page(1)
    	    except (EmptyPage,InvalidPage):
        	pages = paginator.page(paginator.num_pages)

	return HttpResponseRedirect("/TASK/admin/task/%s" % id)
    else:

        return render_to_response('admin_taskprocess.html', RequestContext(request, locals()))



@login_required
def messages(request):
    username = request.user.username
    name = User.objects.get(username=username).first_name
    update = Messages.objects.filter(touser=name).update(status=1)
    message = Messages.objects.filter(touser=name,status=0).count()
    messages = Messages.objects.filter(touser=name).order_by('-id')
    paginator = Paginator(messages,6)
    page = request.GET.get('page')
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except (EmptyPage,InvalidPage):
        pages = paginator.page(paginator.num_pages)


    return render_to_response('admin_messages.html', RequestContext(request, locals()))
#@login_required
#def jiankong(request):
#    from subprocess import Popen, PIPE
#    cmd = "uptime |cut -c '45-61'"
#    p = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
#    out, err = p.communicate()
#    out = simplejson.dumps(out).split()
#    return HttpResponse(out, mimetype='application/javascript')




