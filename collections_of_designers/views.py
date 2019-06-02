from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_account.models import UserAccount
from designers.models import Designer
from collections_of_designers.models import CollectionOfDesigner
from rest_framework import status
import json


@api_view(['GET', 'POST'])
def user_collection_of_designers(request, *args, **kwargs):
    headers = request.header
    token = headers["Authorization"]
    user = UserAccount.objects.get(token=token)
    if request.method == "GET":
        try:
            _from = 0
            _row = 10
            if _from in kwargs.keys():
                    _from = kwargs["_from"]
            if _row in kwargs.keys():
                    _row = kwargs["_row"]
            collections = CollectionOfDesigner.objects.all(user=user.pk)[_from:_row]
            return_data = []
            for collection in collections:
                return_data.append({"title": collection.title, "path": collection.callPic.pk,
                                    "useraccount": collection.user.pk})
            return Response(return_data)
        except:
            return Response({"error": "this user is not exist"})
    elif request.method == "POST":
        data = json.loads(request.body)
        data["user"] = user.pk
        collection = CollectionOfDesigner.objects.create(**data)
        return Response({"id": collection.pk})


@api_view(['GET', 'DELETE'])
def collection_of_designer_operations(request, **kwargs):
    headers = request.header
    token = headers["Authorization"]
    user = UserAccount.objects.get(token=token)
    collection = None
    collection = CollectionOfDesigner.objects.get(pk=kwargs['collection_of_designer_id'])
    if collection:
        if request.method == "GET":
            try:
                if collection:
                    return Response(
                        {"title": collection.title, "collectionPicture": str(collection.callPic),
                         "user": collection.user})
            except:
                raise ("This collection is not exist")
        if request.method == "PUT":
            if user.pk == collection.user.pk:
                collection.title = request.data = ["title"]
                collection.collectionPicture = request.data = ["collectionPicture"]
            else:
                return Response({"access denied"}, status=status.HTTP_403_FORBIDDEN)
            
        if request.method == "DELETE":
            collection.delete()
            return Response({"Collection was deleted"}, status=status.HTTP_200_OK)
    else:
        return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST', 'DELETE'])
def designers_of_collection(request,*args,**kwargs):
    collection = None
    collection = CollectionOfDesigner.objects.get(pk=kwargs['collection_of_designer_id'])
    headers = request.header
    token = headers["Authorization"]
    user = UserAccount.objects.get(token=token)
    if collection:
        if request.method == "POST":
            if collection.user.pk == user.pk:
                designer_id = request.data["designer_id"]
                designer = Designer.objects.get(designer_id)
                collection.designers.add(designer)
                return Response({"designer was added"}, status=status.HTTP_200_OK)
            else:
                return Response({"access denied"}, status=status.HTTP_403_FORBIDDEN)

        if request.method == "DELETE":
            if collection.user.pk == user.pk:
                designer_id = request.data["design_id"]
                designer = Designer.objects.get(designer_id)
                collection.designs.remove(designer)
                return Response({"design was deleted"}, status=status.HTTP_200_OK)
            else:
                return Response({"access denied"}, status=status.HTTP_403_FORBIDDEN)



