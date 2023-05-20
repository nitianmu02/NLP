from django.urls import re_path
from nlp.consumers import SpeechConsumer
from nlp.consumers import SpeechConsumer2


websocket_urlpatterns = [
    re_path(r'ws/result/', SpeechConsumer.as_asgi()),
    re_path(r'ws/result2/', SpeechConsumer2.as_asgi()),

] 