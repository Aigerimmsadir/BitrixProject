from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import CustomUserSerializer
from rest_framework.response import Response
from users.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class TokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        user_serializer = CustomUserSerializer(self.user, context=self.context)
        data['user'] = user_serializer.data
        return data


class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = (IsAuthenticated, )
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        email = request.data['email']
        password = request.data['password']
        user = CustomUser.objects.get(email=email)
        if check_password(password, user.password):
            try:
                token = get_tokens_for_user(user)
                return Response({'user': serializer.data, **token}, status=status.HTTP_201_CREATED, headers=headers)
            except:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
