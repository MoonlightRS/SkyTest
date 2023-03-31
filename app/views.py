from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from project.app.models import File, CheckLog
from project.app.serializers import FileSerializer, CheckLogSerializer

@login_required
def report(request):
    checked_files = CheckLog.objects.filter(updated_by=request.user)
    return render(request, 'report.html', {'checked_files': checked_files})

class FileListView(generics.ListAPIView):
    serializer_class = FileSerializer

    def get_queryset(self):
        return File.objects.filter(uploaded_by=self.request.user)

class FileInfoView(generics.RetrieveAPIView):
    serializer_class = CheckLogSerializer

    def get_queryset(self):
        return CheckLog.objects.filter(file__id=self.kwargs.get('file_id'), updated_by=self.request.user)

class FileRecheckView(APIView):
    def post(self, request, file_id):
        checked_file = get_object_or_404(CheckLog, file__id=file_id, updated_by=request.user)
        # выполняем проверку файлов заново
        # ...
        # сохраняем результат в базу данных
        checked_file.result = 'New result'
        checked_file.save()
        serializer = CheckLogSerializer(checked_file)
        return Response(serializer.data, status=status.HTTP_200_OK)