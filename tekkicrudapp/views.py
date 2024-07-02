from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Product
from .serializer import ProductSerializer
from django.db.models import Max
from datetime import timedelta, datetime


class ProductView(APIView):

    def get(self, request, pk=None):
        if pk:
            product = get_object_or_404(Product, pk=pk)
            serializer = ProductSerializer(product)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
    
class CreateProductView(APIView):

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditProductView(APIView):

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.retrieval_count += 1
        product.save(update_fields=['retrieval_count'])
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DetailProductView(APIView):

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.retrieval_count += 1
        product.save(update_fields=['retrieval_count'])
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteProductView(APIView):

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MaxRetrievedProductView(APIView):

    def get(self, request):
        time_period = self.request.GET.get('time_period')

        if time_period == "all":    #hard coded due to time constraint
            max_retrieval_count = Product.objects.aggregate(Max('retrieval_count'))['retrieval_count__max']
            product = Product.objects.filter(retrieval_count=max_retrieval_count).first()

        if time_period == "last_day":    #hard coded due to time constraint
            last_day = datetime.now() - timedelta(days=1)
            max_retrieval_count = Product.objects.aggregate(Max('retrieval_count'))['retrieval_count__max']
            product = Product.objects.filter(retrieval_count=max_retrieval_count, created_at__gte=last_day).first()
        
        if time_period == "last_week":    #hard coded due to time constraint
            last_week = datetime.now() - timedelta(days=7)
            max_retrieval_count = Product.objects.aggregate(Max('retrieval_count'))['retrieval_count__max']
            product = Product.objects.filter(retrieval_count=max_retrieval_count, created_at__gte=last_week).first()

        else:
            max_retrieval_count = Product.objects.aggregate(Max('retrieval_count'))['retrieval_count__max']
            product = Product.objects.filter(retrieval_count=max_retrieval_count).first()

        if not product:
            return Response({'error': 'No product found.'}, status=status.HTTP_404_NOT_FOUND)
        
        product.retrieval_count += 1
        product.save(update_fields=['retrieval_count'])
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
 