import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from . import routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
# application = get_asgi_application()
application = ProtocolTypeRouter({
   "http":get_asgi_application(),
   "websocket":AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns )))
})
