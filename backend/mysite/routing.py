from django.urls import re_path
from nlp.consumers import ChineseToEnglish
from nlp.consumers import EnglishToChinese


websocket_urlpatterns = [
    re_path(r'ws/chinese/', ChineseToEnglish.as_asgi()),
    re_path(r'ws/english/', EnglishToChinese.as_asgi()),

] 