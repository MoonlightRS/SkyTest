from django.core.mail import send_mail
from project import User, File, CheckLog


def send_notification(file_id, user_id):
    """Отправляет уведомление пользователю о результате проверки файла"""

    # получаем пользователя и файл из базы данных
    user = User.objects.get(id=user_id)
    file = File.objects.get(id=file_id)

    # получаем результаты всех проверок файла из лога
    logs = CheckLog.objects.filter(file_id=file_id).order_by("-created_at")

    # формируем тело письма
    message = f"Файл {file.name} успешно проверен на соответствие правилам Python!"
    if len(logs) > 0:
        message += "\n\nПоследние результаты проверки файлов:"
        for log in logs:
            message += f"\n{log.created_at}: {log.result}"

    # отправляем письмо
    send_mail(
        "Результат проверки файла",
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

    # отмечаем в логах, что письмо было отправлено
    if len(logs) > 0:
        logs[0].sent_notification = True
        logs[0].save()