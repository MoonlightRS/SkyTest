from django.urls import path
from project import FileListView, FileInfoView, FileRecheckView, report

urlpatterns = [
    path('report/', report, name='report'),
]

app_name = 'file_check'

urlpatterns = [
    path('api/files/', FileListView.as_view(), name='file_list'),
    path('api/files/<int:file_id>/', FileInfoView.as_view(), name='file_info'),
    path('api/files/<int:file_id>/recheck/', FileRecheckView.as_view(), name='file_recheck'),
]