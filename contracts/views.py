import datetime

from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from core import models as core_models
from django.views.decorators.csrf import csrf_exempt
from jalali_date import datetime2jalali, date2jalali

from . import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import Employee
from . import functions

class Contract(View):

    def get(self , request):
        projects = models.Project.objects.filter(employees__user=request.user)
        return render(request,"contract/index.html", {"projects":projects})

class Task(View):
    def get(self, request , pk):
        tasks = models.Task.objects.filter(employee__user=request.user,project__pk=pk, done=False)
        return render(request, "contract/tasks.html", {"tasks": tasks})


class HeartBeat(View):
    def post(self, request):
        employee = core_models.Employee.objects.get(pk=request.POST["user"])
        try:
            task_record = models.TaskRecord.objects.get(task__employee=employee, is_doing=True)
        except models.TaskRecord.DoesNotExist:
            return JsonResponse({"status":0})
        task = task_record.task
        elapsed_time = (task_record.end_time - task_record.start_time).seconds
        mins = int(elapsed_time / 60)
        secs = int(elapsed_time % 60)
        toleranced = task.expected_hour * 3600 + ((task.tolerance * task.expected_hour / 100) * 3600)
        if task.expected_hour * 3600 > elapsed_time:
            status = 1
        elif toleranced > elapsed_time:
            status = 2
        elif elapsed_time > toleranced:
            status = 3
        task_record.end_time = task_record.end_time + datetime.timedelta(seconds=int(request.POST['time']))
        task_record.save()
        return JsonResponse({"mins": str(mins), "secs": str(secs), "status": status})


class StartTask(View):
    def get(self, request):
        functions.StopTask(True, request.user)
        task_id = request.GET['task']
        task = models.Task.objects.get(pk=task_id)
        if not task.records.filter(end_time=None):
            models.TaskRecord.objects.create(task=task, start_time=timezone.now(),end_time=timezone.now(), is_doing=True)
            task.active = True
            task.save()
            return redirect("project" , pk=task.project.pk)
        return 0


class StopRecord(View):
    def get(self, request):
        functions.StopTask(True , request.user)
        record = models.TaskRecord.objects.get(pk=request.GET['task_record_id'])
        full_time = record.end_time - record.start_time
        full_time = round(full_time.seconds/3600 , 2)
        record.task.passed_hours = record.task.passed_hours + full_time
        record.task.save()
        return redirect("project", pk=record.task.project.pk)


class Projector(View):
    def post(self,request):
        return redirect("project", pk=request.POST['project'])
