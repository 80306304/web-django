"""
URL configuration for DjangoProject1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() view: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from api.view.card_view import *
from api.view.crypto_view import get_crypto
from api.view.login_view import *
from api.view.regisiter_view import regisiterView
from api.view.test_view import test_f

from api.view.varifyVip_view import varifyVip
from api.views import trigger_task

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/login/', loginView.as_view(), name='user_login'),
    path('api/user/regisiter/', regisiterView.as_view(), name='user_regisiter'),
    path('api/user/varifyVip/', varifyVip.as_view(), name='user_varify'),
    path('api/user/getCrypto/', get_crypto.as_view(), name='get_crypto'),
    path('api/user/test/', test_f.as_view(), name='test'),
    path('api/user/createCard/', createCard.as_view(), name='varify'),
    path('api/user/useCard/', useCard.as_view(), name='varify'),
    path('api/user/getCards/', getCard.as_view(), name='varify'),
    path('api/user/delCard/', delCard.as_view(), name='varify'),
    path('api/user/getUsers/', getUsers.as_view(), name='varify'),
    path('api/user/updateUser/', updateUser.as_view(), name='varify'),
    path('api/user/addUser/', addUser.as_view(), name='varify'),
    path('api/trigger/', trigger_task, name='trigger-task'),

]
