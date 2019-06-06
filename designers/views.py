from rest_framework.response import Response
from rest_framework.decorators import api_view
from designers.models import Designer, CommentForDesigner, RateForDesigner, DesignerRecord
from rest_framework import status
from user_account.models import UserAccount
import jwt
from redtent.settings import SECRET_KEY

@api_view(['POST', 'GET'])
def test(request,**kwargs):
    return Response({"asd":"hoora"})


@api_view(["GET", "POST"])
def list_of_all_designers(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            headers = request.headers
            token = headers["Authorization"]
            requestingـuser = UserAccount.objects.get(pk=jwt.decode(token, SECRET_KEY)["user_id"])
        except:
            return Response(data={"error": "invalid user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if not requestingـuser.kind == "admin" and requestingـuser.kind != "designer":
            return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
        designer = Designer.objects.create(user=requestingـuser, phoneNumber=request.data["phone_number"],
                                           city=request.data["city"], address=request.data["address"],
                                           description=request.data["description"])
        requestingـuser.kind = "designer"
        requestingـuser.save()
        new_token = jwt.encode({"user_id": requestingـuser.pk, "designer_id": designer.pk}, SECRET_KEY)
        return Response({"id": designer.pk, "description": designer.description, "token": new_token}, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        params = request.GET
        _from = 0
        _row = 10
        if "_from" in params.keys():
            _from = int(params["_from"])
        if "_row" in params.keys():
            _row = int(params["_row"])
        if "_order_by" in params.keys():
            designers = Designer.objects.all().order_by('-'+params["_order_by"])[_from:_row]
        else:
            designers = Designer.objects.all()[_from:_row]
        all_designers = []
        for designer in designers:
            all_designers.append({"id": designer.pk, "description":designer.description})
        return Response(all_designers, status=status.HTTP_200_OK)


@api_view(["GET", "PUT", "DELETE"])
def designer_operation(request, **kwargs):
    try:
        headers = request.headers
        token = headers["Authorization"]
        header_information = jwt.decode(token, SECRET_KEY)
        requestingـuser = UserAccount.objects.get(pk=header_information["user_id"])
        if requestingـuser.kind == "designer":
            designer = Designer.objects.get(pk= header_information["designer_id"])
    except:
        return Response(data={"error": "invalid user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if requestingـuser.kind != "admin" and requestingـuser.kind != "designer" and designer.pk != kwargs["designer_id"]:
        return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
    if request.method == "GET":
        return Response(data={"first_name": designer.user.firstName, "last_name": designer.user.lastName,
                              "phone_number": designer.phoneNumber, "city": designer.city,
                              "address": designer.address, "description": designer.description},
                        status=status.HTTP_200_OK)

    elif request.method == "PUT":
        designer.phoneNumber = request.data["phone_number"]
        designer.city = request.data["city"]
        designer.address = request.data["address"]
        designer.description = request.data["description"]
        designer.save()
        return Response(data={"msg": "successful updated"}, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        id = designer.pk
        designer.delete()
        return Response(data={"id": id}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def list_of_comment_designer(request, *args, **kwargs):
    try:
        headers = request.headers
        token = headers["Authorization"]
        header_information = jwt.decode(token, SECRET_KEY)
        requestingـuser = UserAccount.objects.get(pk=header_information["user_id"])
    except:
        return Response(data={"error": "invalid user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        designer = Designer.objects.get(pk=kwargs["designer_id"])
    except:
        return Response(data={"error": "this designers does not exist"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if request.method == "GET":
        _from = 0
        _row = 10
        params = request.GET
        if "_from" in params.keys():
            _from = int(params["_from"])
        if "_row" in params.keys():
            _row = int(params["_row"])
        if requestingـuser != "admin":
            comments = CommentForDesigner.objects.filter(designer=designer, isvalid=True)[_from:_row]
        else:
            comments = CommentForDesigner.objects.filter(designer=designer)[_from:_row]
        all_comments = []
        for comment in comments:
            all_comments.append({"user": comment.user.pk, "is_valid": comment.isvalid, "body": comment.body,
                                 "designer_id": comment.designer.pk, "id": comment.pk})
        return Response(data=all_comments, status=status.HTTP_200_OK)
    if request.method == "POST":
        comment_for_designer = CommentForDesigner.objects.create(user=requestingـuser, designer=designer, body=request.data["body"])
        return Response(data={"id": comment_for_designer.pk}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def list_of_rate_for_designer(request, *args, **kwargs):
    try:
        headers = request.headers
        token = headers["Authorization"]
        header_information = jwt.decode(token, SECRET_KEY)
        requestingـuser = UserAccount.objects.get(pk=header_information["user_id"])
    except:
        return Response(data={"error": "invalid user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        designer = Designer.objects.get(pk=kwargs["designer_id"])
    except:
        return Response(data={"error": "this designers does not exist"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if request.method == "GET":
        if requestingـuser.kind != "admin":
            return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
        _from = 0
        _row = 10
        params = request.GET
        if "_from" in params.keys():
            _from = int(params["_from"])
        if "_row" in params.keys():
            _row = int(params["_row"])
        rates = RateForDesigner.objects.filter(designer=designer)[_from:_row]
        all_rate = []
        for rate in rates:
            all_rate.append({"rate": rate.rate, "user_id": rate.user.pk, "designer_id": rate.designer.pk})
        return Response(data=all_rate, status=status.HTTP_200_OK)
    elif request.method == "POST":
        rate_for_designer = RateForDesigner.objects.create(user=requestingـuser, designer=designer,
                                                           rate=request.data["rate"])
        return Response(data={"id": rate_for_designer.pk}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def list_of_designer_records(request, *args , **kwargs):
    try:
        designer = Designer.objects.get(pk=kwargs['designer_id'])
    except:
        return Response(data={"error": "this designers does not exist"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if request.method == "GET":
        _from = 0
        _row = 10
        params = request.GET
        if "_from" in params.keys():
            _from = int(params["_from"])
        if "_row" in params.keys():
            _row = int(params["_row"])
        designer_records = designer.designer_records.all()[_from:_row]
        all_records = []
        for designer_record in designer_records:
            all_records.append({"id": designer_record.pk, "description": designer_record.description,
                                "picture": str(designer_record.image)})
        return Response(data=all_records, status=status.HTTP_200_OK)
    try:
        headers = request.headers
        token = headers["Authorization"]
        header_information = jwt.decode(token, SECRET_KEY)
        requestingـuser = UserAccount.objects.get(pk=header_information["user_id"])
    except:
        return Response(data={"error": "invalid user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if requestingـuser.kind != "admin" and requestingـuser.kind != "designer" and (requestingـuser.kind == "designer" or
                                                                                   requestingـuser.pk != designer.pk):
        return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "POST":
        designer_record = DesignerRecord(picture=request.data["image"],
                                         description=request.data["description"],
                                         Designer=designer)
        designer_record.save()
        return Response(data={"id": designer_record.pk}, status=status.HTTP_200_OK)


@api_view(["GET", "PUT", "DELETE"])
def designer_records_operations(request, *args , **kwargs):
    try:
        designer = Designer.objects.get(pk=kwargs["designer_id"])
    except:
        return Response(data={"error": "this designer does not exist"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        designer_record = DesignerRecord.objects.get(pk=kwargs["designer_record_id"])
    except:
        return Response(data={"error": "this record does not exist"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if designer.pk != designer_record.designer.pk:
        return Response(data={"error": "invalid pass"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == "GET":
        return Response(data={"id": designer_record.pk, "path": str(designer_record.picture)}, status=status.HTTP_200_OK)
    try:
        headers = request.headers
        token = headers["Authorization"]
        header_information = jwt.decode(token, SECRET_KEY)
        requestingـuser = UserAccount.objects.get(pk=header_information["user_id"])
    except:
        return Response(data={"error": "invalid user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if requestingـuser.kind != "admin" and requestingـuser.kind != "designer" and (requestingـuser.kind == "designer" or
                                                                                   requestingـuser.pk != designer.pk):
        return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "PUT":
        designer_record.description = request.data["description"]
        if not isinstance(request.data["image"], str):
            designer_record.picture.delete()
            designer_record.picture = request.data["image"]
        designer_record.save()
        return Response(data={"id": id}, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        id = designer_record.pk
        designer_record.picture.delete()
        designer_record.delete()
        return Response(data={"id": id}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_my_rate(request,*args,**kwargs):
    try:
        headers = request.headers
        token = headers["Authorization"]
        header_information = jwt.decode(token, SECRET_KEY)
        requestingـuser = UserAccount.objects.get(pk=header_information["user_id"])
    except:
        return Response(data={"error": "invalid user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        designer = Designer.objects.get(pk=kwargs["designer_id"])
    except:
        return Response(data={"error": "this designer does not exist"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        myrate = RateForDesigner.objects.filter(user=requestingـuser,designer=designer)[0].rate
        return Response(data={"rate": myrate}, status=status.HTTP_200_OK)
    except:
        return Response(data={"error": "you are not rating this designer"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


