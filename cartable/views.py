from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from cartable import models
from core import models as core_models
from django.db.models import Q
import datetime


class Cartable(LoginRequiredMixin, View):

    def get(self, request):
        inbox = core_models.Employee.objects.get(user=request.user).received_letters.all().order_by("-date")
        return render(request, "cartable/cartable.html", {"letters": inbox})


class Write(LoginRequiredMixin, View):
    def get(self, request):
        possible_templates = models.Template.objects.all()
        return render(request, "cartable/write.html", {"templates": possible_templates})


class Detail(LoginRequiredMixin, View):
    tracking = int(datetime.datetime.now().timestamp())

    def post(self, request):
        detail = request.POST
        template = models.Template.objects.get(id=detail['template'])
        body = request.POST['body']
        return render(request, "cartable/write_detail.html",
                      {"template": template, 'body': body, "tracking": self.tracking,
                       "summary": request.POST['summary'], "title": request.POST['title']})


class Contact(LoginRequiredMixin, View):
    def post(self, request):
        body = request.POST['body']
        tracking = request.POST['tracking']
        title = request.POST['title']
        template = models.Template.objects.get(id=request.POST['template'])
        summary = request.POST['summary']
        employee = core_models.Employee.objects.get(user=request.user)
        this = models.Letter(title=title, summary=summary, tracking_id=tracking, body=body, template=template,
                             creator=employee)
        this.save()
        print(this)
        return None
