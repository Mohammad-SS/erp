from django.db import models


class ContractType(models.TextChoices):
    CONTRACTUAL = 'C' , "قراردادی"
    HOURLY = 'H' , "ساعتی"


class TaskType(models.TextChoices):
    PERHOUR = 'PH' , "به ازای هر ساعت"
    PERTASK = "PT" , "برای کل وظیفه"