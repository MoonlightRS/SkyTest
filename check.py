import subprocess

from django.conf import settings
from project import File, CheckLog


def check_code(file_id, file_path):
    """Проверяет код на соответствие правилам с помощью утилиты flake8"""

    # формируем команду для проверки с помощью flake8
    cmd = f"{settings.FLAKE8_PATH} {file_path}"

    # выполняем проверку
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # сохраняем лог проверки
    log = CheckLog.objects.create(
        file_id=file_id,
        result=result.stdout + result.stderr
    )

    # обновляем статус файла в базе данных
    if result.returncode == 0:
        file = File.objects.get(id=file_id)
        file.status = "passed"
        file.save()