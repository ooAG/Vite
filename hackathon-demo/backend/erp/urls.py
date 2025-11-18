# backend/erp/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views

urlpatterns = [
    # auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # summary & sales
    path('api/summary/', views.summary, name='summary'),
    path('api/sales/', views.sales_list, name='sales_list'),
    path('api/sales/<int:pk>/', views.sales_detail, name='sales_detail'),
    # csv export (staff-only)
    path('api/sales/export/', views.export_sales_csv, name='export_sales_csv'),
    # whoami
    path('api/me/', views.whoami, name='whoami'),
]
