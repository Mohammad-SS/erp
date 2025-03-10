from django.db import models
from django.contrib.auth.models import User

from core import enums


class Permision(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        parent_name = ""
        if not self.parent == None:
            parent_name = " > " + self.parent.name
        return f'{self.name} ( {self.parent} )'


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee")
    department = models.CharField(max_length=150)
    national_id = models.CharField(max_length=10)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=11)
    position = models.ForeignKey(Position, models.CASCADE, related_name="employees")
    permission = models.ManyToManyField(Permision, related_name="employees")
    read = models.BooleanField(default=False)
    read_time = models.DateTimeField(blank=True, null=True)
    signature = models.FileField(upload_to="signs", blank=True, null=True, default="signs/sign.png")
    type = models.CharField(max_length=1, choices=enums.ContractType.choices, default=enums.ContractType.CONTRACTUAL)
    wage = models.IntegerField(blank=True, null=True)
    contract_length = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} ( {self.department} ) '
