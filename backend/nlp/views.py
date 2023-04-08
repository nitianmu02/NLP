from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['POST'])
def speech(request):
    word = request.data.get('word')
    print(word)
    return Response(word)