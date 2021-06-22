from . import models

def StopTask(task , user):
    if task== True:
        models.Task.objects.filter(employee__user=user).update(active=False)
        models.TaskRecord.objects.filter(task__employee__user=user).update(is_doing=False)
    else:
        models.Task.objects.filter(pk=task , employee__user=user).update(active=False)
        models.TaskRecord.objects.filter(task__id=task ,task__employee__user=user , is_doing=False)
