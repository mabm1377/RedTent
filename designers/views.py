from rest_framework.response import Response
from rest_framework.decorators import api_view
from designers.models import Designer


@api_view(['POST', 'GET'])
def test(request,**kwargs):
    return Response({"asd":"hoora"})


@api_view(["GET", "POST"])
def list_of_all_designers(request, **kwargs):
    if request.method == "GET":
        _from = 0
        _row = 10
        if _from in kwargs.keys():
            _from = kwargs["_from"]
        if _row in kwargs.keys():
            _row = kwargs["_row"]
        designers = Designer.objects.all()[_from:_row]
        return_data = []
        for designer in designers:
            return_data.append({"designer": designer.pk})
        return Response(return_data)
    '''
    if request.method == "POST":
        designer = Designer.objects.create(**data)
        design.designer.add(designer)
        return Response({"designer_id": designer.pk})
    '''


@api_view(["GET", "PUT", "DELETE"])
def designer_operation(request, **kwargs):
    if request.method == "GET":
        headers = request.header
        token = headers["Authorization"]
        designer = Designer.objects.get(pk=kwargs['designer_id'])
        if designer:
            return Response({"firstname": designer.firstname, "lastname": designer.lastname, "username": designer.username,
                             "password": designer.password, "tag": designer.tag, "token": token,
                             "phonenumber": designer.phoneNumber
                           , "city": designer.city, "address": designer.address, "comments": designer.comments,
                             "rates": designer.rates})


