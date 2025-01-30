# from django.db import IntegrityError
# from django.core.exceptions import ObjectDoesNotExist
# from djoser.serializers import UserCreateSerializer, UserSerializer
# from django.core.files.base import ContentFile
# from rest_framework import serializers
# from rest_framework.validators import UniqueTogetherValidator



# class UserSignUpSerializer(UserCreateSerializer):
#     """User registration."""

#     class Meta:
#         model = User
#         fields = (
#             'id',
#             'username',
#             'email',
#             'first_name',
#             'last_name',
#             'password'
#         )