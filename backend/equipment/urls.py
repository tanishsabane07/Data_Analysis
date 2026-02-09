"""
URL configuration for equipment API.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Data endpoints
    path('upload/', views.CSVUploadView.as_view(), name='csv-upload'),
    path('summary/<int:pk>/', views.DatasetSummaryView.as_view(), name='dataset-summary'),
    path('data/<int:pk>/', views.DatasetDataView.as_view(), name='dataset-data'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('dataset/<int:pk>/', views.DatasetDeleteView.as_view(), name='dataset-delete'),
    path('report/<int:pk>/', views.PDFReportView.as_view(), name='pdf-report'),
    
    # Authentication endpoints
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
]
