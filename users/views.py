from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.shortcuts import render
from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.signals import user_logged_in
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework_jwt.utils import jwt_payload_handler
from django.contrib.auth.hashers import check_password
from rest_framework.request import Request
from django.conf import settings
from users.models import CustomUser
import jwt
from rest_framework.decorators import action

@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    try:
        email = request.data['email']
        password = request.data['password']
        user = CustomUser.objects.get(email=email)
        if check_password(password, user.password):
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['name'] = "%s %s" % (
                    user.first_name, user.last_name)
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res)


class UserViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser,)
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @action(methods=['GET'], detail=False)
    def current(self, request):
        print(self.request.user)
        serializer=CustomUserSerializer(self.request.user,context={'request': request})
        return Response(serializer.data)

# @api_view(['GET',])
# def current_user(request):
#     serializer_context = {
#         'request': Request(request),
#     }
#     serializer=CustomUserSerializer(instance=request.user,context=serializer_context)
#     return Response(serializer.data)
