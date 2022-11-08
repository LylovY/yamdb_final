from django.urls import include, path

from .routers import router_v1
from .views import create_user_send_code, get_token

app_name = 'api'

urlpatterns = [
    path('v1/auth/signup/', create_user_send_code, name='create_user'),
    path('v1/auth/token/', get_token, name='create_token'),
    path('v1/', include(router_v1.urls)),
]
