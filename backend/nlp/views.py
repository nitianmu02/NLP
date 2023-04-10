from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['POST'])
def speech(request):
    word = request.data.get('word')
    print(word)
    return Response("后端接收到文本之后翻译的内容放这里")