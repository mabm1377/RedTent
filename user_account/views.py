from user_account.models import UserAccount
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
        data = json.loads(request.body)
        try:
            user = UserAccount.objects.get(username=data["user_name"])
            if user.password == data['password']:
                response_data = {"token": user.token}
            else:
                response_data = {"error": "this password is not Incorrect"}
        except:
            response_data = {"error": "this user does not exist"}

    return Response(response_data)


#signup
@api_view(['POST', 'GET'])
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
    return Response(response_data, content_type='application/json')


@api_view(['POST', 'GET'])
def get_list_of_users(request, *args, **kwargs):
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
            return_data.append({""})


@api_view(['POST', 'DELETE', 'GET'])
def user_operations(request,*args , **kwargs):
    pass


@api_view(['POST','GET'])
def rates_for_tag(request, *args , **kwargs):
    pass


@api_view(['PUT','GET'])
def rate_operations(request, *args, **kwargs):
    pass
