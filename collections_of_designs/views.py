from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_account.models import UserAccount
from designs.models import Design
from collections_of_designs.models import CollectionOfDesign
from rest_framework import status
import jwt
from redtent.settings import SECRET_KEY


@api_view(['GET', 'POST'])
def user_collection_of_designs(request, *args, **kwargs):
    try:
        headers = request.headers
        token = headers["Authorization"]
        requestingـuser = UserAccount.objects.get(pk=jwt.decode(token, SECRET_KEY)["user_id"])
    except:
        return Response(data={"error": "invalid user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if request.method == "POST":
        collection = CollectionOfDesign.objects.create(user=requestingـuser,
                                                         picture=request.data["image"],
                                                         title=request.data["title"])
        return Response({"id": collection.pk}, status=status.HTTP_200_OK)

    elif request.method == "GET":
        try:
            params = request.GET
            _from = 0
            _row = 10
            if "_from" in params.keys():
                _from = params["_from"]
            if "_row" in params.keys():
                _row = params["_row"]
            collections = CollectionOfDesign.objects.filter(user=requestingـuser.pk)[_from:_row]
            all_collections = []
            for collection in collections:
                all_collections.append({"title": collection.title, "picture": collection.picture,
                                        "user_id": collection.user.pk})
            return Response(all_collections, status=status.HTTP_200_OK)
        except:
            return Response({"error": "this user is not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_of_design_operations(request, **kwargs):
    try:
        headers = request.headers
        token = headers["Authorization"]
        requestingـuser = UserAccount.objects.get(pk=jwt.decode(token, SECRET_KEY)["user_id"])
    except:
        return Response(data={"error": "invalid user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        collection = CollectionOfDesign.objects.get(pk=kwargs['collection_of_design_id'])
        if collection.user.pk != requestingـuser.pk and requestingـuser.kind != "admin":
            return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response(data={"error": "this collection does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == "GET":
        try:
            if collection:
                return Response(
                    {"title": collection.title, "collectionPicture": str(collection.picture),
                     "user": collection.user})
        except:
            return Response(data={"error": "this collection is not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == "PUT":
        collection.title = request.data = ["title"]
        if not isinstance(request.data["picture"], str):
            collection.picture.delete()
            collection.picture = request.data["picture"]
        collection.save()
        return Response(data={"id": collection.pk}, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        collection.picture.delete()
        collection.delete()
        return Response(data={"msg":"Collection was deleted"}, status=status.HTTP_200_OK)


@api_view(['POST', 'GET', 'DELETE'])
def designs_of_collection(request,*args,**kwargs):
    try:
        headers = request.headers
        token = headers["Authorization"]
        requestingـuser = UserAccount.objects.get(pk=jwt.decode(token, SECRET_KEY)["user_id"])
    except:
        return Response(data={"error": "invalid user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        collection = CollectionOfDesign.objects.get(pk=kwargs['collection_of_design_id'])
    except:
        return Response(data={"error": "this collection does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if collection.user.pk != requestingـuser.pk and requestingـuser.kind != "admin":
        return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        try:
            params = request.GET
            _from = 0
            _row = 10
            if "_from" in params.keys():
                _from = params["_from"]
            if "_row" in params.keys():
                _row = params["_row"]
            designs = collection.designs.all()[_from:_row]
            all_designs = []
            for design in designs:
                all_designs.append({"id": design.pk})
            return Response(data=all_designs, status=status.HTTP_200_OK)
        except:
            return Response({"error": ""}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        design = Design.objects.get(pk=request.data["design_id"])
    except:
        return Response(data={"error": "this design does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if request.method == "POST":
        collection.designs.add(design)
        return Response({"id": collection.pk}, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        collection.designs.remove(design)





