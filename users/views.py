from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.models import User
from users.serializers import UserSerializer, EmailTokenObtainPairSerializer
from utils.permissions import IsAdmin
from rest_framework_simplejwt.views import TokenObtainPairView


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]
