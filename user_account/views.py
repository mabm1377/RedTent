from user_account.models import UserAccount, RateForTag
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
        if "_from" in kwargs.keys() and kwargs["_from"]:
            _from = kwargs["_from"]
        if "_row" in kwargs.keys() and kwargs["_row"]:
            _row = kwargs["_row"]
        try:
            headers = request.headers
            token = headers["Authorization"]

            user = UserAccount.objects.get(pk=jwt.decode(token, SECRET_KEY)['user_id'])
            if user.kind != "admin":
                return Response({"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
            users = UserAccount.objects.all()[int(_from):int(_row)]
            return_data = []
            for user in users:
                return_data.append({"id": user.pk, "username": user.username})
            return Response(data=return_data, status=status.HTTP_200_OK)
        except:
            return Response(data={"": ""},status=status.HTTP_500_INTERNAL_SERVER_ERROR )

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
    try:
        headers = request.headers
        token = headers["Authorization"]
        requestingـuser = UserAccount.objects.get(pk=jwt.decode(token, SECRET_KEY)["user_id"])
        user = UserAccount.objects.get(pk=kwargs["user_id"])
        if not user.pk == requestingـuser.pk and not requestingـuser.kind == "admin":
            return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
        if request.method == "GET":
            return Response(data={"data": jwt.encode({"username": user.username,
                                                      "password": user.password,
                                                      "first_name": user.firstName,
                                                      "last_name": user.lastName,
                                  "kind": user.kind}, SECRET_KEY), "avatar": str(user.avatar)}, status=status.HTTP_200_OK)
        elif request.method == "PUT":
            data = jwt.decode(request.data["data"], SECRET_KEY)
            if data["kind"] == "admin" and not requestingـuser.kind == "admin":
                return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
            user.username = data["username"]
            user.firstName = data["first_name"]
            user.lastName = data["last_name"]
            user.kind = data["kind"]
            if not isinstance(request.data["avatar"], str):
                user.avatar.delete()
                user.avatar = request.data["avatar"]
            user.save()
            return Response(data={"data": jwt.encode({"username": user.username,
                                                      "password": user.password}, SECRET_KEY),
                                  "avatar": str(user.avatar)},
                            status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            user.avatar.delete()
            id = user.pk
            user.delete()
            return Response(data={"id": id},status=status.HTTP_200_OK)
    except:
        Response(data={"error": "user does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def rates_for_tag(request, *args , **kwargs):
    try:
        headers = request.headers
        token = headers["Authorization"]
        requestingـuser = UserAccount.objects.get(pk=jwt.decode(token, SECRET_KEY)["user_id"])
        user = UserAccount.objects.get(pk=kwargs["user_id"])
        if not user.pk == requestingـuser.pk and not requestingـuser.kind == "admin":
            return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
        if request.method == "GET":
            _from = 0
            _row = 10
            if "_from" in kwargs.keys() and kwargs["_from"]:
                _from = kwargs["_from"]
            if "_row" in kwargs.keys() and kwargs["_row"]:
                _row = kwargs["_row"]
            rates = RateForTag.objects.filter(user=user).order_by('-rate')[int(_from):int(_row)]
            tag_list = []
            for rate in rates:
                tag_list.append(rate.tag_id)
            return Response(data={"tags": tag_list}, status=status.HTTP_200_OK)
    except:
        return Response(data={"error": "user does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
