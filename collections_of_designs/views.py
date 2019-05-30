from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_account.models import UserAccount
from designs.models import Design
from collections_of_designs.models import CollectionOfDesign
from rest_framework import status
from rest_framework.response import Response
import json


@api_view(['GET', 'POST'])
def user_collection_of_designs(request, **kwargs):
    headers = request.header
    token = headers["Authorization"]
    user = UserAccount.objects.get(token=token)
    sc = status.HTTP_200_OK
    if request.method == "GET":
        try:
            _from = 0
            _row = 10
            if _from in kwargs.keys():
                    _from = kwargs["_from"]
            if _row in kwargs.keys():
                    _row = kwargs["_row"]
            collections = CollectionOfDesign.objects.all(user=user.pk)[_from:_row]
            return_data = []
            for collection in collections:
                return_data.append({"title": collection.title, "pic": str(collection.callPic), "user_account": collection.userAccount.pk})
            return Response(return_data, status=sc)
        except:
            return Response({"error": "this user is not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == "POST":
        collection = CollectionOfDesign.objects.create(collPic=request.data["collPic"], title=request.data["title"],
                                                                                                         user=user)

        return Response({"id": collection.pk}, status=sc)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_of_design_operations(request, collection_of_design_id,**kwargs):
    headers = request.header
    token = headers["Authorization"]
    user = UserAccount.objects.get(token=token)
    sc = status.HTTP_200_OK
    collection =None
    collection = CollectionOfDesign.objects.get(pk=kwargs['collection_of_design_id'])
    if collection:
        if request.method == "GET":
            try:
                if collection:
                    return Response({"title": collection.title, "collpic":str(collection.callPic), "useraccount": collection.user})
            except:
                raise ("This collection is not exist")
        if request.method == "PUT":
            if user.pk == collection.user.pk:
                collection.title = request.data = ["title"]
                collection.callPic = request.data = ["collPic"]
            else:
                return Response({"access denied"}, status=status.HTTP_403_FORBIDDEN)
        if request.method == "DELETE":
            collection.delete()
            return Response({"Collection was deleted"}, status=status.HTTP_200_OK)
    else:
        return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST', 'DELETE'])
def designs_of_collection(request,*args,**kwargs):
    collection =None
    collection = CollectionOfDesign.objects.get(pk=kwargs['collection_of_design_id'])
    headers = request.header
    token = headers["Authorization"]
    user = UserAccount.objects.get(token=token)
    if collection:
        if request.method == "POST":
            if collection.user.pk == user.pk:
                design_id = request.data["design_id"]
                design = Design.objects.get(design_id)
                collection.designs.add(design)
                return Response({"design was added"}, status=status.HTTP_200_OK)
            else:
                return Response({"access denied"}, status=status.HTTP_403_FORBIDDEN)

        if request.method == "DELETE":
            if collection.user.pk == user.pk:
                design_id = request.data["design_id"]
                design = Design.objects.get(design_id)
                collection.designs.remove(design)
                return Response({"design was deleted"}, status=status.HTTP_200_OK)
            else:
                return Response({"access denied"}, status=status.HTTP_403_FORBIDDEN)

