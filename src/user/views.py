from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from phonenumber_field.phonenumber import PhoneNumber
from phonenumbers import NumberParseException

from .models import User
from .serializers import UserSerializer

@api_view(['GET'])
def user_list (request, format = None):
  users = User.objects.all()
  serializer = UserSerializer(users, many = True)
  return Response({'status': 'success', 'users': serializer.data}, status = status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def user_get (request, id, format = None):
  try:
    user = User.objects.get(pk = id)
  except User.DoesNotExist:
    return Response({'status': 'failure'}, status = status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    return Response({'status': 'success', 'user': UserSerializer(user).data})
  if request.method == 'PUT':
    serializer = UserSerializer(user, data = request.data)
    if serializer.is_valid():
      serializer.save()
      return Response({'status': 'success', 'user': serializer.data})
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
  if request.method == 'DELETE':
    user.delete()
    return Response({'status': 'success'}, status = status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def user_set (request, format = None):
  serializer = UserSerializer(data = request.data)
  if serializer.is_valid():
    serializer.save()
    return Response({'status': 'success', 'user': serializer.data}, status = status.HTTP_201_CREATED)
  return Response({'status': 'failure', 'error': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_search (request, query, format = None):
  # check if the search query is a phone number
  try:
    phone_number = PhoneNumber.from_string(query)
    if not phone_number.is_valid():
      raise ValueError
  except (NumberParseException, ValueError):
    # no, it is not a phone number
    # try performing other searches
    users = User.objects.filter(
      Q(name__istartswith = query) | Q(name__icontains = query) |
      Q(email__icontains = query) | Q(phone_number__icontains = query)
    ).distinct()
    serializer = UserSerializer(users, many = True)
  else:
    # yes, it is a phone number
    # in this case, try to find perfect match
    user = User.objects.filter(Q(phone_number__icontains = phone_number))[0]
    serializer = UserSerializer(user)
  finally:
    return Response({'status': 'success', 'user': serializer.data}, status = status.HTTP_200_OK)
