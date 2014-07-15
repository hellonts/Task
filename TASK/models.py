from django.db import models
from django.contrib.auth.models import User
#coding=utf-8
# Create your models here.




   
class Task(models.Model):
    fromuser = models.CharField(max_length=20,blank=True)
    touser = models.CharField(max_length=20,blank=False)
    demand_status = models.IntegerField(default=1,blank=False,null=True)
    completion_time = models.DateTimeField(blank=True,null=True)

    vmusage = models.CharField(max_length=20,blank=False)
    vmstarttime = models.DateTimeField(blank=False,null=True)
    vm_cpu_core = models.IntegerField(default=0,blank=False,null=True)
    vm_mem = models.IntegerField(default=0,blank=False,null=True)
    vm_disk = models.IntegerField(default=0,blank=False,null=True)
    vm_ip = models.IPAddressField(blank=True,null=True)

    vm_life_cycle = models.IntegerField(default=0,blank=False,null=True)
    vm_status = models.IntegerField(default=1,blank=False,null=True)

    messages = models.TextField(max_length=20,blank=True,null=True)
    current_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    task_status = models.IntegerField(default=1,blank=True,null=True)
    def __unicode__(self):
        return self.fromuser

class Task_reply(models.Model):
    taskid = models.IntegerField(blank=False)
    fromuser = models.CharField(max_length=20,blank=True)
    touser = models.CharField(max_length=20,blank=False)
    content = models.TextField(max_length=20,blank=False)
    reply_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
	return self.fromuser

class Messages(models.Model):
    taskid = models.IntegerField(blank=False)
    fromuser = models.CharField(max_length=20,blank=True)
    touser = models.CharField(max_length=20,blank=False)
    title = models.CharField(max_length=20)
    content = models.TextField(max_length=20)
    status = models.BooleanField(default=False)
    message_time =  models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.taskid

