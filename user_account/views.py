from user_account.models import UserAccount,RateForTag
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import hashlib


#login
@api_view(['POST'])
def get_token_for_login(request):
    response_data = {}
    if request.method == 'POST':
        try:

            user = UserAccount.objects.get(username=request.data["user_name"])
            if user.password == request.data['password']:
                response_data = {"token": user.token}
            else:
                response_data = {"error": "this password is not Incorrect"}
        except:
            response_data = {"error": "this user does not exist"}

    return Response(response_data)


#signup
@api_view(['POST'])
def get_token_for_signup(request):
    response_data = {}
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = hashlib.md5(data["user_name"].encode()).hexdigest()
            user = UserAccount.objects.create(username=data["user_name"], password=data["password"], token=token)
            response_data = {"user_name": user.username, "token": token}
        except :
            response_data = {"error": "this user is exist"}
    return Response(response_data, content_type='application/json', status= status.HTTP_200_OK)


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
            token = hashlib.md5(request.data["user_name"].encode()).hexdigest()
            user = UserAccount.objects.create(username=request.data["user_name"],
                                              password=request.data["password"],
                                              avatar=request.data["avatar"],
                                              token=token)
            response_data = {"user_name": user.username, "token": token, "avatar": str(user.avatar)}
            sc = status.HTTP_200_OK
        except:
            response_data = {"error": "this user is exist"}
            sc = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(response_data, status=sc)


@api_view(['PUT', 'DELETE', 'GET'])
def user_operations(request,*args , **kwargs):
    headers = request.header
    token = headers["Authorization"]
    user = UserAccount.objects.get(token=token)
    if request.method == "GET":
        headers = request.header
        token = headers["Authorization"]
        user = UserAccount.objects.get(token=token)
        if user:
            return Response({"fistName": user.firstName, "lastName": user.lastName, "username": user.username,
                              "password": user.password, "avatar": str(user.avatar)})
        else:
            return Response({"Wrong user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if request.method == "PUT":
        if user:
            user.firstName = request.body["firstName"]
            user.lastName = request.body["lastName"]
            user.username = request.body["username"]
            user.password = request.body["password"]
            user.save()
        else:
            return Response({"Wrong user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if request.method == "DELETE":
        if user:
            user.remove()
            return Response({"user was deleted"}, status=status.HTTP_200_OK)
        else:
            return Response({"Wrong user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
def rates_for_tag(request, *args , **kwargs):
    headers = request.header
    token = headers["Authorization"]
    user = UserAccount.objects.get(token=token)
    if user:
        return_data = []
        a = RateForTag.objects.filter(user=user).order_by('rate')
        for b in a:
            return_data.append({"id": b.pk, "rate":b.rate})
        return Response(data=return_data, status=status.HTTP_200_OK)
    else:
        return Response({"Wrong user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






