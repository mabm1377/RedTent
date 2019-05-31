from rest_framework.response import Response
from rest_framework.decorators import api_view
from designers.models import Designer, CommentForDesigner, RateForDesigner , DesignerRecord
from rest_framework import status
from user_account.models import UserAccount
import os
import json

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

        headers = request.headers
        token = headers["Authorization"]
        user = UserAccount.objects.get(token=token)
        if not user.kind == "admin":
            return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
        designers = Designer.objects.all()[_from:_row]
        return_data = []
        for designer in designers:
            return_data.append({"id": designer.pk, "description": designer.description})
        return Response(return_data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        headers = request.headers
        token = headers["Authorization"]
        user = UserAccount.objects.get(token=token)
        designer = Designer.objects.create(user=user, phoneNumber=request.data["phone_number"],
                                           city=request.data["city"], address=request.data["address"],
                                           description=request.data["description"])
        user.isDesigner = True
        user.save()
        return Response({"id": designer.pk})


#############create sales history in get###################
@api_view(["GET", "PUT", "DELETE"])
def designer_operation(request, **kwargs):
    try:
        designer = Designer.objects.get(pk=kwargs['designer_id'])
    except:
        return Response(data={"error": "this designers does not exist"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if request.method == "GET":
        #headers = request.header
        #token = headers["Authorization"]
        return Response({"first_name": designer.user.firstName, "last_name": designer.user.lastName,
                         "phone_number": designer.phoneNumber, "city": designer.city,
                         "address": designer.address})
    #for admin
    elif request.method == "PUT":
        new_data = {"first_name": designer.user.firstName, "last_name": designer.user.lastName,
                    "phone_number": designer.phoneNumber, "city": designer.city,
                    "address": designer.address}
        designer.user.objects.update(**new_data)
    #for admin
    elif request.method == "DELETE":
        designer.delete()


@api_view(["GET", "POST"])
def list_of_comment_designer(request, *args, **kwargs):
    try:
        designer = Designer.objects.get(pk=kwargs['designer_id'])
    except:
        return Response(data={"error": "this designers does not exist"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if request.method == "GET":
        _from = 0
        _row = 10
        if "_from" in kwargs.keys() and kwargs["_from"]:
            _from = int(kwargs["_from"])
        if "_row" in kwargs.keys() and kwargs["_row"]:
            _row = int(kwargs["_row"])
        comments = designer.comments.all()[_from:_row]
        return_data = []

        for comment in comments:
            return_data.append({"body": CommentForDesigner.objects.filter(user=comment, isvalid=True,
                                                                        designer=designer)[0].body})
        return Response(data=return_data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        headers = request.headers
        token = headers["Authorization"]
        user = UserAccount.objects.get(token=token)
        comment_for_designer = CommentForDesigner.objects.create(user=user, designer=designer, body=request.data["body"])
        return Response(data={"id": comment_for_designer.pk}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def list_of_rate_for_designer(request, *args, **kwargs):
    try:
        designer = Designer.objects.get(pk=kwargs['designer_id'])
    except:
        return Response(data={"error": "this designers does not exist"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if request.method == "GET":
        _from = 0
        _row = 10
        if "_from" in kwargs.keys() and kwargs["_from"]:
            _from = int(kwargs["_from"])
        if "_row" in kwargs.keys() and kwargs["_row"]:
            _row = int(kwargs["_row"])
        rates = designer.rates.all()[_from:_row]
        return_data = []

        for rate in rates:
            return_data.append({"rate": RateForDesigner.objects.filter(user=rate, designer=designer)[0].rate})
        return Response(data=return_data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        headers = request.headers
        token = headers["Authorization"]
        user = UserAccount.objects.get(token=token)
        rate_for_designer = RateForDesigner.objects.create(user=user, designer=designer, rate=request.data["rate"])
        return Response(data={"id": rate_for_designer.pk}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def list_of_designer_records(request, *args , **kwargs):
    try:
        designer = Designer.objects.get(pk=kwargs['designer_id'])
    except:
        return Response(data={"error": "this designers does not exist"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == "GET":
        designer_records = designer.designer_records()
        return_data = []
        for designer_record in designer_records:
            return_data.append({"id": designer_record.pk})

    elif request.method == "POST":
        designer_record = DesignerRecord(pic=request.data["image"],description=request.data["description"],Designer=designer)
        designer_record.save()
        return  Response(data={"id": designer_record.pk}, status=status.HTTP_200_OK)


@api_view(["GET", "PUT", "DELETE"])
def designer_records_operations(request, *args , **kwargs):
    try:
        designer_records = DesignerRecord.objects.get(pk=args[1])
    except:
        return Response(data={"error": "this record does not exist"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if request.method == "GET":
        return Response(data={"id":designer_records.pk, "path": str(designer_records.pic)}, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass


@api_view(["GET"])
def get_my_rate(request,*args,**kwargs):
    pass


@api_view(["GET", "POST", "DELETE"])
def edit_profile():
    pass
