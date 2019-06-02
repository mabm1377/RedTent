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
    if request.method == 'POST':
        try:
            data = jwt.decode(request.data["data"], SECRET_KEY)
            user = UserAccount.objects.get(username=data["username"])
            if user.password == request.data['password']:
                if user.kind == "designer":
                    response_data = {"token": jwt.encode({"user_id": user.pk, "designer_id": user.designer.pk},
                                                         SECRET_KEY)}
                else:
                    response_data = {"token": jwt.encode({"user_id": user.pk},
                                                         SECRET_KEY)}
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

            #data = jwt.decode(request.data["data"], SECRET_KEY)
            data = {"user_name":"ali12345455", "password":"1234556"}
            user = UserAccount.objects.create(username=data["user_name"],
                                              password=data["password"])
            user.token = jwt.encode({"id": user.pk}, SECRET_KEY)
            user.save()
            response_data = {"user_name": user.username, "token": user.token}
            sc = status.HTTP_200_OK
        except:
            response_data = {"error": "this user is exist"}
            sc = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(response_data, status=sc)


@api_view(['PUT', 'DELETE', 'GET'])
def user_operations(request,*args , **kwargs):
    pass


@api_view(['POST','GET'])
def rates_for_tag(request, *args , **kwargs):
    pass


@api_view(['GET'])
def rate_operations(request, *args, **kwargs):
    pass
