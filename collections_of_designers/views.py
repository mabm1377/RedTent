from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_account.models import UserAccount
from collections_of_designers.models import CollectionOfDesigner
import json


@api_view(['GET', 'POST'])
def user_collection_of_designers(request,*args,**kwargs):
    pass
    '''
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
                return_data.append({"title": collection.title, "pic": collection.callPic.pk,
                                    "useraccount": collection.user.pk})
            return Response(return_data)
        except:
            return Response({"error": "this user is not exist"})
    elif request.method == "POST":
        data = json.loads(request.body)
        data["user"] = user.pk
        collection = CollectionOfDesigner.objects.create(**data)
        return Response({"id": collection.pk})
        '''


@api_view(['GET', 'PUT', 'DELETE'])
def collection_of_designer_operations(request, UserID, CollectionOfDesignsID):
    pass


@api_view(['POST', 'DELETE'])
def designers_of_collection(request,*args,**kwargs):
    pass

