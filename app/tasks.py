from celery.task import periodic_task, task
from datetime import timedelta
from project.app.models import File, CheckLog
from project.send_email import send_email

@task(name='check_file_task')
def check_file_task(file_id):
    checked_file = File.objects.get(id=file_id)
    # выполняем проверку файла
    result = 'File checked successfully'
    # сохраняем результат в базу данных
    CheckLog.objects.create(file=checked_file, result=result, updated_by=checked_file.uploaded_by)
    # отправляем уведомление на почту пользователю
    send_email(user_email=checked_file.uploaded_by.email, checked_file=checked_file)


@periodic_task(run_every=timedelta(hours=1))
def check_new_files():
    new_files = File.objects.filter(checklog__isnull=True)
    for file in new_files:
        # выполняем проверку файла
        result = 'File checked successfully'
        # сохраняем результат в базу данных
        CheckLog.objects.create(file=file, result=result, updated_by=file.uploaded_by)
        # отправляем уведомление на почту пользователю
        send_email(user_email=file.uploaded_by.email, checked_file=file)