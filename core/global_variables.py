import datetime

from django.contrib.auth.decorators import login_required
from jalali_date import datetime2jalali, date2jalali
from .models import Employee


def dateandtime(request):
    date_and_time = datetime.datetime.now()
    date = datetime2jalali(date_and_time).strftime('%Y/%m/%d %A')
    time = datetime2jalali(date_and_time).strftime('%-M : %-H %p')
    return {"date": date, "time": time}

def employees(request):
    if request.user.is_authenticated:
        employee = Employee.objects.filter(user=request.user)
        if employee:
            return {"employee": employee[0]}
    return {}