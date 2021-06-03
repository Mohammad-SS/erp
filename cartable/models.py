from django.db import models
from django.contrib.postgres.fields import ArrayField
from jalali_date import datetime2jalali
from core import models as core_models


class Template(models.Model):
    name = models.CharField(max_length=150)
    picture = models.FileField(blank=True , null=True , upload_to='letter_templates' )
    body_margins = ArrayField(models.CharField(max_length=6 , default="0px") , size=4 , blank=True )
    body_width = models.CharField(max_length=6)
    date_margins = ArrayField(models.CharField(max_length=6 ,default="0px") , size=4 , blank=True )
    tracking_margins = ArrayField(models.CharField(max_length=6 ,default="0px") , size=4 , blank=True)
    sign_margins = ArrayField(models.CharField(max_length=6 ,default="0px") , size=4 , blank=True )

    default = models.BooleanField(default=False)

class Letter(models.Model):
    title = models.CharField(max_length=400)
    creator = models.ForeignKey(core_models.Employee, models.CASCADE, related_name="created_letters")
    summary = models.TextField()
    tracking_id = models.PositiveIntegerField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    related_letters = models.ForeignKey("self", on_delete=models.SET_NULL, related_name="linked_letters", null=True,
                                        blank=True)
    attachments = ArrayField(models.FileField() , blank=True , null=True)
    body = models.TextField(blank=True , default="")
    template = models.ForeignKey(Template , on_delete=models.SET_NULL , null=True)
    def __str__(self):
        return f'{self.title} - {self.creator} ( {self.tracking_id} )'


class Reference(models.Model):
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE, related_name='references')
    sender = models.ForeignKey(core_models.Employee, models.CASCADE, related_name="sent_letters")
    to = models.ManyToManyField(core_models.Employee, related_name="received_letters")
    message = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    @property
    def persian_date(self):
        return datetime2jalali(self.date).strftime("%Y/%m/%d %H:%M")


    def __str__(self):
        return f'{self.letter} --- {self.sender} ----> {self.to}'


