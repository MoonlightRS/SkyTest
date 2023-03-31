from django.http import JsonResponse
import subprocess

def check_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        result = subprocess.run(['flake8', '--ignore=E501', code], stdout=subprocess.PIPE)
        error = result.stdout.decode('utf-8')
        if error:
            return JsonResponse({'status': 'error', 'message': error})
        else:
            return JsonResponse({'status': 'success'})

# Реализация эндпоинтов для управления проверками и перезапуска
# Требуемые пакеты: djangorestframework и drf-yasg

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import File
from .serializers import FileSerializer

# Endpoint для получения списка файлов пользователя
@swagger_auto_schema(
    method="get",
    responses={
        200: FileSerializer(many=True),
        401: "Unauthorized"
    },
    operation_description="Get all files of a user"
)
@api_view(['GET'])
def get_user_files(request):
    user = request.user
    files = File.objects.filter(user=user)
    serializer = FileSerializer(files, many=True)
    return Response(serializer.data)

# Endpoint для получения информации по одному файлу
@swagger_auto_schema(
    method="get",
    responses={
        200: FileSerializer(),
        401: "Unauthorized",
        404: "File not found"
    },
    operation_description="Get details of a file",
)
@api_view(['GET'])
def get_file_details(request, file_id):
    user = request.user
    try:
        file = File.objects.get(id=file_id, user=user)
    except File.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = FileSerializer(file)
    return Response(serializer.data)

# Endpoint для запроса на повторную проверку файлов
@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'file_id': openapi.Schema(type=openapi.TYPE_INTEGER),
        }
    ),
    responses={
        200: "Success",
        401: "Unauthorized",
        404: "File not found"
    },
    operation_description="Retry a file check",
)
@api_view(['POST'])
def retry_file_check(request):
    user = request.user
    file_id = request.data.get('file_id')
    try:
        file = File.objects.get(id=file_id, user=user)
    except File.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # TODO: код запроса на повторную проверку файла

    return Response(status=status.HTTP_200_OK)