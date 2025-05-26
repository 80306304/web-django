from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from DjangoProject1.settings import RSA_PUBLIC_KEY, RSA_PRIVATE_KEY
from api.function.get_client_ip import get_client_ip

from api.selfUtils import rsa_decrypt, result

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class get_crypto(TokenObtainPairView):
    def get(self, request, *args, **kwargs):
        user = request.user

        power = user.user_level
        if power <=1:return result.success("无权限")
        ip = get_client_ip(request)
        data = {
            "type":"RSA",
            "RSA_PUBLIC_KEY":RSA_PUBLIC_KEY.replace('\n',''),
            "RSA_PRIVATE_KEY":RSA_PRIVATE_KEY.replace('\n',''),
            "ip":ip
        }

        return result.success(data)