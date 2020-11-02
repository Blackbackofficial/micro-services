from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Items, Order_item
from .serializers import ItemSerializer, OrderItemSerializer
from django.http import JsonResponse
from rest_framework import status

# Create your views here.
def warranty_solution():