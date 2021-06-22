from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.views import View
from cartable import models
from core import models as core_models
from django.db.models import Q
import datetime
from django.core.files import File


class Cartable(LoginRequiredMixin, View):

    def get(self, request):
        inbox = core_models.Employee.objects.get(user=request.user).received_letters.all().order_by("-date")
        return render(request, "cartable/cartable.html", {"letters": inbox})


class Write(LoginRequiredMixin, View):
    def get(self, request):
        possible_templates = models.Template.objects.all()
        return render(request, "cartable/write.html", {"templates": possible_templates})


class Detail(LoginRequiredMixin, View):

    def post(self, request):
        tracking = int(datetime.datetime.now().timestamp())
        detail = request.POST
        template = models.Template.objects.get(id=detail['template'])
        body = request.POST['body']
        return render(request, "cartable/write_detail.html",
                      {"template": template, 'body': body, "tracking": tracking,
                       "summary": request.POST['summary'], "title": request.POST['title']})


class SaveLetter(LoginRequiredMixin, View):
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
        return redirect('cartable_out_letter', pk=this.id)


class OnGoingLetter(LoginRequiredMixin, View):
    def get(self, request, pk):
        this = models.Letter.objects.get(pk=pk)
        # current_employee = core_models.Employee.objects.get(user=request.user)
        print(this.draft)
        if this.draft:
            possible_receivers = core_models.Employee.objects.filter(~Q(user=request.user))
            possible_related_letters = models.Letter.objects.filter(~Q(id=pk))
            return render(request, "cartable/set_contacts.html",
                          {"letter": this, "possible_receivers": possible_receivers,
                           "possible_related_letters": possible_related_letters})
        else:
            return redirect("cartable_simple_read", pk=pk)


class SendLetter(LoginRequiredMixin, View):

    def post(self, request):
        this = models.Letter.objects.get(id=request.POST['letter'])
        for letter in request.POST.getlist('related-letters'):
            related_letter = models.Letter.objects.get(id=letter)
            this.related_letters.add(related_letter)
        attachments = []
        for attachment in request.FILES.getlist('attachments'):
            attach = File(attachment)
            attachments.append(attach)
            this.attachments = attachments
        this.save()

        sender = core_models.Employee.objects.get(user=request.user)
        for receiver in request.POST.getlist("receivers"):
            to = core_models.Employee.objects.get(id=receiver)
            new_reference = models.Reference(letter=this, sender=sender, to=to, depth=0)
            new_reference.save()
        this.draft = False
        this.save()

        return redirect("cartable_simple_read", pk=this.id)


class ShowLetter(LoginRequiredMixin, View):
    def get(self, request, pk):
        reference = models.Reference.objects.filter(pk=pk)
        if reference.count():
            reference = reference[0]
        else:
            return redirect("cartable_inbox")
        this = reference.letter
        start_references = this.references.filter(depth=0)
        employee = core_models.Employee.objects.get(user=request.user)
        possible_letters = models.Letter.objects.filter(Q(references__to=employee) | Q(creator=employee))
        if this in possible_letters:
            print(this.references.filter(to=employee).update(read=True))
            return render(request, "cartable/simple_read.html",
                          {'letter': this, 'references': start_references, 'reference': reference})
        else:
            return redirect("cartable_inbox")


class NewReference(LoginRequiredMixin, View):
    def get(self, request, pk):
        reference = models.Reference.objects.get(pk=pk)
        letter = reference.letter
        possible_receivers = core_models.Employee.objects.filter(~Q(user=request.user))
        return render(request, "cartable/new_reference.html",
                      {"letter": letter, "possible_receivers": possible_receivers, "reference": reference})

    def post(self, request, pk):
        reference = models.Reference.objects.get(pk=pk)
        this = reference.letter
        sender = core_models.Employee.objects.get(user=request.user)
        for receiver in request.POST.getlist("receivers"):
            to = core_models.Employee.objects.get(id=receiver)
            new_reference = models.Reference(letter=this, sender=sender, to=to, message=request.POST['message'],
                                             parent=reference)
            new_reference.save()
        return redirect("cartable_simple_read", pk=pk)


class DeleteReference(LoginRequiredMixin, View):
    def get(self, request, pk):
        child = models.Reference.objects.get(pk=pk)
        child.delete()
        return redirect("cartable_simple_read", pk=pk)


class CartableOut(LoginRequiredMixin, View):
    def get(self, request):
        employee = core_models.Employee.objects.get(user=request.user)
        refrences = models.Reference.objects.filter(sender=employee).order_by("-date")
        return render(request , 'cartable/out_box.html' , {"letters" : refrences})

class CartableDrafts(LoginRequiredMixin, View):
    def get(self, request):
        employee = core_models.Employee.objects.get(user=request.user)
        letters = models.Letter.objects.filter(creator=employee , references=None).order_by("-created_date")
        return render(request , 'cartable/drafts.html' , {"letters" : letters})
