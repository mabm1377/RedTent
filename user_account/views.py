from user_account.models import UserAccount, RateForTag
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from designers.models import Designer
import jwt
from redtent.settings import SECRET_KEY
from designs.models import RateForDesign
from collections_of_designs.models import CollectionOfDesign
from tag.models import Tag
#login
@api_view(['POST'])
def get_token_for_login(request):
    response_data = {}
    sc = status.HTTP_200_OK
    if request.method == 'POST':
        try:
            data = jwt.decode(request.data["data"], SECRET_KEY)
            print(data)
            user = UserAccount.objects.get(username=data["username"])
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAA")
            print(user.pk)
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
        params = request.GET
        _from = 0
        _row = 10
        if "_from" in params.keys():
            _from = int(params["_from"])
        if "_row" in params.keys() :
            _row = int(params["_row"])
        try:
            headers = request.headers
            token = headers["Authorization"]

            user = UserAccount.objects.get(pk=jwt.decode(token, SECRET_KEY)['user_id'])
            if user.kind != "admin":
                return Response({"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
            users = UserAccount.objects.all()[_from:_row]
            return_data = []
            for user in users:
                return_data.append({"id": user.pk, "username": user.username})
            return Response(data=return_data, status=status.HTTP_200_OK)
        except:
            return Response(data={"": ""}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )

    elif request.method == "POST":
        sc = status.HTTP_200_OK
        try:
            if "avatar" in request.data.keys():
                data = jwt.decode(request.data["data"], SECRET_KEY)
                print("BBBBBBBBBBBBBBBBBBBB")
                user = UserAccount(username=data["username"],
                                   password=data["password"],
                                   firstName=data["firstname"],
                                   lastName=data["lastname"],
                                   avatar=request.data["avatar"])
            else:
                data = jwt.decode(request.data["data"], SECRET_KEY)
                print(data)
                user = UserAccount(username=data["username"],
                                   password=data["password"],
                                   firstName=data["firstname"],
                                   lastName=data["lastname"])
            user.save()
            CollectionOfDesign.objects.create(title="default", user=user)
            token = jwt.encode({"user_id": user.pk}, SECRET_KEY)
            response_data = {"token": token}
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
            if data["kind"] == "designer":
                pk = Designer.objects.create(city="",address="",phoneNumber=123, description="").pk
                return Response(data={"data": jwt.encode({"username": user.username,
                                                          "password": user.password}, SECRET_KEY),
                                      "token": jwt.encode({"user_id":user.pk,"designer_id": str(pk)}, SECRET_KEY)})

            return Response(data={"data": jwt.encode({"username": user.username,
                                                      "password": user.password}, SECRET_KEY),
                                  "avatar": str(user.avatar)},
                            status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            user.avatar.delete()
            id = user.pk
            user.delete()
            return Response(data={"id": id}, status=status.HTTP_200_OK)
    except:
        return Response(data={"error": "user does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            params = request.GET
            if "_from" in params.keys():
                _from = int(params["_from"])
            if "_row" in params.keys():
                _row = int(params["_row"])
            rates = RateForTag.objects.filter(user=user).order_by('-rate')[_from:_row]
            tag_list = []
            for rate in rates:
                tag_list.append(rate.tag_id)
            return Response(data={"tags": tag_list}, status=status.HTTP_200_OK)
    except:
        return Response(data={"error": "user does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def rates_for_designs(request, *args, **kwargs):
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
            params = request.GET
            if "_from" in params.keys():
                _from = int(params["_from"])
            if "_row" in params.keys():
                _row = int(params["_row"])
            rates = RateForDesign.objects.filter(user=user).order_by('-rate')[_from:_row]
            design_list = []
            for rate in rates:
                design_list.append(rate.design_id)
            return Response(data={"designs": design_list}, status=status.HTTP_200_OK)
    except:
        return Response(data={"error": "user does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def favorites(request, *args, **kwargs):
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
            params = request.GET
            if "_from" in params.keys():
                _from = int(params["_from"])
            if "_row" in params.keys():
                _row = int(params["_row"])
            rate_for_tags = RateForTag.objects.all().order_by("-rate")[0:20]
            all_designs = []
            for rate in rate_for_tags:
                all_designs += list(rate.tag.designs.all()[0:10])
            favorites = []
            for design in all_designs:

                favorites.append({"id": design.pk, "picture": str(design.picture)})
            return Response(data=favorites[_from:_row], status=status.HTTP_200_OK)
    except:
        return Response(data={"error":""}, status=status.HTTP_400_BAD_REQUEST)
