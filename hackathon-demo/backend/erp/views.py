# backend/erp/views.py
from django.http import HttpResponse
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .models import Sale
from .serializers import SaleSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

import csv

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def summary(request):
    """
    Returns aggregated totals and monthly series for charting.
    """
    qs = Sale.objects.all()
    category = request.query_params.get('category')
    if category:
        qs = qs.filter(category=category)

    total_sales = qs.aggregate(total=Sum('amount'))['total'] or 0
    total_orders = qs.count()
    inventory_count = 100  # placeholder

    monthly_qs = (
        qs.annotate(month=TruncMonth('date'))
          .values('month')
          .annotate(total=Sum('amount'))
          .order_by('month')
    )
    monthly_data = [
        {"month": m['month'].strftime("%Y-%m"), "total": float(m['total'])}
        for m in monthly_qs
    ]
    return Response({
        "total_sales": float(total_sales),
        "total_orders": total_orders,
        "inventory_count": inventory_count,
        "monthly": monthly_data
    })


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def sales_list(request):
    """
    GET: paginated list of sales (supports ?category= and ?page=)
    POST: create a new Sale (ONLY staff users allowed)
    """
    # Create -> only staff allowed
    if request.method == 'POST':
        if not request.user.is_staff:
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        ser = SaleSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=201)
        return Response(ser.errors, status=400)

    # GET (list) - allowed for any authenticated user
    qs = Sale.objects.all().order_by('-date')
    category = request.query_params.get('category')
    if category:
        qs = qs.filter(category=category)

    paginator = PageNumberPagination()
    paginator.page_size = 10
    page = paginator.paginate_queryset(qs, request)
    ser = SaleSerializer(page, many=True)
    return paginator.get_paginated_response(ser.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def sales_detail(request, pk):
    """
    GET: retrieve one sale (allowed for all authenticated)
    PUT, DELETE: only staff users allowed
    """
    try:
        s = Sale.objects.get(pk=pk)
    except Sale.DoesNotExist:
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(SaleSerializer(s).data)

    # For write operations ensure staff
    if not request.user.is_staff:
        return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        ser = SaleSerializer(s, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=400)

    if request.method == 'DELETE':
        s.delete()
        return Response(status=204)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def whoami(request):
    """Return username and is_staff for frontend role checks"""
    user = request.user
    return Response({"username": user.username, "is_staff": user.is_staff})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_sales_csv(request):
    """
    Export sales as CSV. Only staff users allowed.
    """
    if not request.user.is_staff:
        return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    qs = Sale.objects.all().order_by('-date')
    category = request.query_params.get('category')
    if category:
        qs = qs.filter(category=category)

    # build CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['date', 'product', 'category', 'amount'])
    for s in qs:
        writer.writerow([s.date.isoformat(), s.product, s.category, str(s.amount)])
    return response
