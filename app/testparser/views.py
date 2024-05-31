"""
Views for the recipe APIs.
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404

from core.models import Product
from testparser import serializers
from .telegram_bot import telegram_notifications
from .functions import (
    selenium_get,
    data_save_db,
)
from .tasks import task_parser


class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Product.objects.all()
        serializer = serializers.ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Product.objects.all()
        model = get_object_or_404(queryset, pk=pk)
        serializer = serializers.ProductSerializer(model)
        return Response(serializer.data)


    @swagger_auto_schema(method='post',
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             properties={
                                 'products_count': openapi.Schema(
                                     type=openapi.TYPE_INTEGER,
                                     description='integer'
                                     ),
                                 }
                             )
                         )
    @action(detail=False, methods=['post'])
    def custom_create(self, request, next_page=False):
        serializer = serializers.ProductPostSerializer(data=request.data)
        if serializer.is_valid():
            if not serializer.data['products_count']:
                num = 10
            else:
                num = serializer.data['products_count']

            url = 'https://www.ozon.ru/seller/1/products/'

            if num > 36:
                next_page = True

            html_content = selenium_get(url, next_page)
            data_parsered = task_parser.delay(html_content, num).get()
            objects = data_save_db(data_parsered)
            telegram_notifications(len(objects))

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

