from user_account.models import UserAccount
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
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
        user = UserAccount.objects.get(pk=jwt.decode(token, SECRET_KEY)['user_id'])
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
            user.token = jwt.encode({"user_id": user.pk}, SECRET_KEY)
            user.save()
            response_data = {"token": user.token}
            sc = status.HTTP_200_OK
        except:
            response_data = {"error": "this user is exist"}
            sc = status.HTTP_201_CREATED
    return Response(response_data, status=sc)


@api_view(['PUT', 'DELETE', 'GET'])
def user_operations(request, *args , **kwargs):
    return_data = {}
    sc = status.HTTP_200_OK
    headers = request.headers
    token = headers["Authorization"]
    try:
        print(jwt.decode(token, SECRET_KEY))
        requestingـuser = UserAccount.objects.get(pk=jwt.decode(token, SECRET_KEY)["user_id"])
        user = UserAccount.objects.get(pk=kwargs["user_id"])
        if not user.pk == requestingـuser.pk and not requestingـuser.kind == "admin":
            return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
        if request.method == "GET":
            return Response(data={"username": user.username, "first_name": user.firstName, "last_name": user.lastName,
                                  "kind": user.kind, "avatar": str(user.avatar)}, status=status.HTTP_200_OK)
        elif request.method == "PUT":
            if not user.kind == "admin" and requestingـuser["kind"] == "admin":
                return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
            user.username = request.data["username"]
            user.firstName = request.data["first_name"]
            user.lastName = request.data["last_name"]
            user.kind = request.data["kind"]
            if not type(request.data["avatar"] == "str"):
                user.avatar.delete()
                user.avatar = request.data["avatar"]
            user.save()
        elif request.method == 'DELETE':
            user.avatar.delete()
            user.delete()
    except:
        Response(data={"error": "user does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST', 'GET'])
def rates_for_tag(request, *args , **kwargs):
    pass


@api_view(['GET'])
def rate_operations(request, *args, **kwargs):
    pass
