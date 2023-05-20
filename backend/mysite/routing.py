from django.urls import re_path
from nlp.consumers import SpeechConsumer

websocket_urlpatterns = [
    re_path(r'ws/result/',SpeechConsumer.as_asgi()),
] 