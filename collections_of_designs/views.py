from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_account.models import UserAccount
from collections_of_designs.models import CollectionOfDesign
import json


@api_view(['GET', 'POST'])
def user_collection_of_designs(request, **kwargs):
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
            collections = CollectionOfDesign.objects.all(user=user.pk)[_from:_row]
            return_data = []
            for collection in collections:
                return_data.append({"title": collection.title, "pic": collection.callPic.pk, "user_account": collection.userAccount.pk})
            return Response(return_data)
        except:
            return Response({"error": "this user is not exist"})
    elif request.method == "POST":
        data = json.loads(request.body)
        data["user"] = user.pk
        collection = CollectionOfDesign.objects.create(**data)
        return Response({"id":collection.pk})


@api_view(['GET', 'PUT', 'DELETE'])
def collection_of_design_operations(requset, **kwargs):
    pass
'''
    collection =None
    collection = CollectionOfDesign.objects.get(pk=kwargs['collection_of_design_id'])
    if collection:
        if requset.method == "GET":
            try:
                if collection:
                    return Response({"title": collection.title, "collpic":collection.callPic, "useraccount": collection.user})
            except:
                raise ("This collection is not exist")
        if requset.method == "PUT":
            collection =CollectionOfDesign.objects.create(????)
        if requset.method == "DELETE":
            collection.delete()
            return Response({"Collection was deleted"})

'''


@api_view(['POST', 'DELETE'])
def designs_of_collection(request,*args,**kwargs):
    pass


@api_view(['POST', 'GET'])
def test(request,**kwargs):
    return Response({"asd":"hoora"})
