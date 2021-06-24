from django.db import models
from jalali_date import datetime2jalali, date2jalali

from core import models as core_models, enums

class Project(models.Model):
    creator = models.ForeignKey(core_models.Employee,models.CASCADE , related_name="created_projects")
    employees = models.ManyToManyField(core_models.Employee, related_name="involving_projects")
    moderators = models.ManyToManyField(core_models.Employee,related_name="moderating_projects")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} ( {self.creator.user.first_name} {self.creator.user.last_name} )'

class Task(models.Model):
    project = models.ForeignKey(Project , models.CASCADE , related_name="tasks")
    employee = models.ForeignKey(core_models.Employee, models.CASCADE, related_name="tasks")
    creator = models.ForeignKey(core_models.Employee, models.CASCADE, related_name="created_tasks")
    created_date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=65)
    expected_hour = models.FloatField()
    salary = models.PositiveIntegerField()
    salary_unit = models.CharField(choices=enums.TaskType.choices, default=enums.TaskType.PERHOUR, max_length=2)
    passed_hours = models.FloatField(default=0)
    tolerance = models.IntegerField(default=10)
    done = models.BooleanField(default=False)
    deadline = models.DateTimeField()
    failed = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    def __str__(self):
        percentage = (self.passed_hours / self.expected_hour) * 100
        return f'{self.employee.user.first_name} {self.employee.user.last_name} - {self.title} ( {percentage}% )'

    @property
    def get_percentage(self):
        percentage = (self.passed_hours / self.expected_hour) * 100
        return int(percentage)

    @property
    def get_salary(self):
        salary = f'{self.get_salary_unit_display()} {self.salary} تومان '
        return salary

    @property
    def persian_date(self):
        return {"created_date": date2jalali(self.created_date).strftime("%Y/%m/%d"),
                "deadline": datetime2jalali(self.deadline).strftime("%Y/%m/%d %H:%M")}
    @property
    def sum_hours(self):
        secs = 0
        for record in self.records.all():
            secs += record.record_length['full_time'].seconds
        return {"mins" : int(secs/60) , "secs" : int(secs%60) , "hours" : round(secs/3600 , 3)}

    @property
    def sum_income(self):
        income = self.sum_hours["hours"] * self.salary
        return int(income)

    @property
    def expected_minutes(self):
        income = int(self.expected_hour * 60)
        return int(income)

class TaskRecord(models.Model):
    task = models.ForeignKey(Task, models.CASCADE, related_name="records")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_doing = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_time']

    @property
    def persian_date(self):

        if not self.end_time:
            end_time = None
        else:
            end_time = datetime2jalali(self.end_time).strftime("%Y/%m/%d %H:%M")
        return {"start_time": datetime2jalali(self.start_time).strftime("%Y/%m/%d %H:%M"),
                "end_time": end_time}

    @property
    def record_length(self):
        full_time = self.end_time - self.start_time
        return {"mins" : int(full_time.seconds % 60) , "secs" : int(full_time.seconds / 60) , "full_time" : full_time}
