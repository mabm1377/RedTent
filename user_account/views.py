from user_account.models import UserAccount
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import hashlib
import jwt
from redtent.settings import SECRET_KEY


#login
@api_view(['POST'])
def get_token_for_login(request):
    response_data = {}
    sc = status.HTTP_200_OK
    if request.method == 'POST':
        try:
            data = jwt.decode(request.data["data"], SECRET_KEY)
            user = UserAccount.objects.get(username=data["username"])
            if user.password == data['password']:
                if user.kind == "designer":
                    response_data = {"token": jwt.encode({"user_id": user.pk, "designer_id": user.designer.pk},
                                                         SECRET_KEY)}
                else:
                    response_data = {"token": jwt.encode({"user_id": user.pk},
                                                         SECRET_KEY)}
            else:
                sc = status.HTTP_404_NOT_FOUND
                response_data = {"error": "invalid username or password"}
        except:
            sc = status.HTTP_404_NOT_FOUND
            response_data = {"error": "invalid username or password"}

    return Response(response_data, status=sc)


@api_view(['POST', 'GET'])
def list_of_users(request, *args, **kwargs):
    if request.method == 'GET':
        _from = 0
        _row = 10
        if _from in kwargs.keys():
            _from = kwargs["_from"]
        if _row in kwargs.keys():
            _row = kwargs["_row"]
        headers = request.headers
        token = headers["Authorization"]
        user = UserAccount.objects.get(token=token)
        if user.kind != "admin":
            return Response({"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
        users = UserAccount.objects.all()[_from:_row]
        return_data = []
        for user in users:
            return_data.append({"id": user.pk, "user_name": user.username})
        return Response(data=return_data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        sc = status.HTTP_200_OK
        try:

            data = jwt.decode(request.data["data"], SECRET_KEY)
            user = UserAccount.objects.create(username=data["username"],
                                              password=data["password"])
            user.token = jwt.encode({"id": user.pk}, SECRET_KEY)
            user.save()
            response_data = {"username": user.username, "token": user.token}
            sc = status.HTTP_200_OK
        except:
            response_data = {"error": "this user is exist"}
            sc = status.HTTP_201_CREATED
    return Response(response_data, status=sc)


@api_view(['PUT', 'DELETE', 'GET'])
def user_operations(request, *args , **kwargs):
    return_data = {}
    sc = status.HTTP_200_OK
    try:
        user = UserAccount.objects.get(kwargs["user_id"])
        if request.method == "GET":
            return_data = {"username": user.username, "first_name": user.firstName, "last_name": user.lastName,
                           "kind": user.kind, "avatar": str(user.avatar)}
    except:
        {}

    return Response(data=return_data, status=sc)


@api_view(['POST','GET'])
def rates_for_tag(request, *args , **kwargs):
    pass


@api_view(['GET'])
def rate_operations(request, *args, **kwargs):
    pass
