import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from designs.models import Design, RateForDesign, CommentForDesign
from tag.models import Tag
from user_account.models import UserAccount, RateForTag
from designers.models import Designer
import jwt
from redtent.settings import SECRET_KEY


#"GET": "getting list of designs" _for all users
#"POST": "add new design"_ for admin
@api_view(['POST', 'GET'])
def list_of_design(request, *args, **kwargs):
    if request.method == 'POST':
        headers = request.headers
        token = headers["Authorization"]
        requestingـuser = UserAccount.objects.get(pk=jwt.decode(token, SECRET_KEY)["user_id"])
        if not requestingـuser.kind == "admin":
            return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
        design = Design(picture=request.data["image"])
        design.save()
        return Response({"id": design.pk, "picture": str(design.picture)}, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        params = request.GET
        _from = 0
        _row = 10
        if "_from" in params.keys() and params["_from"]:
            _from = int(params["_from"])
        if "_row" in params.keys() and params["_row"]:
            _row = int(params["_row"])
        if "_order_by" in params.keys() and params["_order_by"]:
            if "_tag" in params.keys() and params["_tag"]:
                designs = Tag.objects.get(pk=params["_tag"]).designs.all().order_by('-'+params["_order_by"])[_from:_row]
            else:
                designs =Design.objects.all().order_by('-'+params["_order_by"])[_from:_row]
        else:
            if "_tag" in params.keys() and params["_tag"]:
                designs = Tag.objects.get(pk=params["_tag"]).designs.all()[_from:_row]
            else:
                designs =Design.objects.all()[_from:_row]

        return_data = []
        for design in designs:
            return_data.append({"id": design.pk, "picture": str(design.picture)})
        return Response(return_data, status= status.HTTP_200_OK)


@api_view(['GET', 'DELETE'])
def design_operation(request, *args, **kwargs):
    try:
        design = Design.objects.get(pk=kwargs["design_id"])
        if request.method == 'GET':
            design.view += 1
            design.save()
            return Response(data={"design_id": design.pk, "design_picture": str(design.picture),
                                  "rate": design.total_rate, "view": design.view},
                            status=status.HTTP_200_OK)
        headers = request.headers
        token = headers["Authorization"]
        requestingـuser = UserAccount.objects.get(pk=jwt.decode(token, SECRET_KEY)["user_id"])
        if not requestingـuser.kind == "admin":
            return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
        elif request.method == 'DELETE':
            id = design.pk
            design.picture.delete()
            design.delete()
            return Response(data={"id": id}, status=status.HTTP_200_OK)
    except :
        return Response(data={"error": "this design is not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST', 'PUT'])
def list_of_design_tags(request, **kwargs):
    if request.method == 'GET':
        design = Design.objects.get(pk=kwargs["design_id"])
        tags = design.tag.all()
        all_tags = []
        for tag in tags:
            all_tags.append({"id": tag.pk, "name": tag.name})

        return Response({"tags": all_tags}, status=status.HTTP_200_OK)
    try:
        headers = request.headers
        token = headers["Authorization"]
        requestingـuser = UserAccount.objects.get(pk=jwt.decode(token, SECRET_KEY)["user_id"])
        if not requestingـuser.kind == "admin":
            return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
        elif request.method == 'POST':
            try:
                design = Design.objects.get(pk=kwargs['design_id'])
                for tag in request.data["tags"]:
                    new_tag = Tag.objects.get_or_create(name=tag)[0]
                    design.tag.add(new_tag)
                tags = design.tag.all()
                all_tags = []
                for tag in tags:
                    all_tags.append({"id": tag.pk, "name": tag.name})

                return Response(data={"id": design.pk, "tags": all_tags}, status=status.HTTP_200_OK)
            except:
                return Response(data={"error": "invalid tags or design"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif request.method == 'PUT':
            try:
                data = dict(request.data)
                design = Design.objects.get(pk=kwargs['design_id'])
                all_tags = []

                for tag in design.tag.all():
                    all_tags.append(tag.name)

                for add_item in [item for item in data["tags"] if item not in all_tags]:
                    new_tag = Tag.objects.get_or_create(name=add_item)[0]
                    design.tag.add(new_tag)

                for delete_item in [item for item in design.tag.all() if item.name not in data["tags"]]:
                    design.tag.remove(delete_item)
                tags = design.tag.all()
                all_tags = []
                for tag in tags:
                    all_tags.append({"id": tag.pk, "name": tag.name})

                return Response(data={"tags": all_tags}, status=status.HTTP_200_OK)
            except:
                return Response(data={"error": "this design does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except:
        return Response(data={"error": "invalid user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#for getting my rate
@api_view(['GET'])
def get_myrate(request, *args, **kwargs):
    try:
        headers = request.headers
        token = headers["Authorization"]
        requestingـuser = UserAccount.objects.get(pk=jwt.decode(token, SECRET_KEY)["user_id"])
        design = Design.objects.get(pk=kwargs["design_id"])
        rate = RateForDesign.objects.filter(design=design).filter(user=requestingـuser)
        if rate.__len__() > 0:
            return Response(data={"rate": rate[0].rate}, status=status.HTTP_200_OK)
    except:
        return Response(data={"": ""}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def list_of_rates_for_design(request, *args, **kwargs):
    if request.method == 'GET':
        try:
            headers = request.headers
            token = headers["Authorization"]
            requestingـuser = UserAccount.objects.get(pk=jwt.decode(token, SECRET_KEY)["user_id"])
            if requestingـuser.kind != "admin":
                return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
            params = request.GET
            _from = 0
            _row = 10
            if "_from" in params.keys():
                _from = params["_from"]
            if "_row" in params.keys():
                _row = params["_row"]
            rates = RateForDesign.objects.filter(design=kwargs["design_id"])[_from:_row]
            return_data = []
            for rate in rates:
                return_data.append({"rate": rate.rate, "design_id": rate.design.pk, "user_id": rate.user.pk})
            return Response(data=return_data, status=status.HTTP_200_OK)
        except:
            return Response(data={"error": "invalid user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'POST':
        try:
            headers = request.headers
            token = headers["Authorization"]
            requestingـuser = UserAccount.objects.get(pk=jwt.decode(token, SECRET_KEY)["user_id"])
            new_rate = int(request.data["rate"])
            design = Design.objects.get(pk=kwargs["design_id"])
            last_number_of_rates = len(RateForDesign.objects.filter(design=kwargs["design_id"]))
            design.total_rate = (design.total_rate + new_rate)/(last_number_of_rates+1)
            design.save()
            tags = design.tag.all()
            for tag in tags:
                rate_for_tag = RateForTag.objects.filter(tag=tag, user=requestingـuser)
                if len(rate_for_tag) > 0:
                    rate_for_tag[0].number_of_rating += 1
                    rate_for_tag[0].rate = (rate_for_tag[0].rate * rate_for_tag[0].number_of_rating+new_rate)/rate_for_tag[0].number_of_rating
                    rate_for_tag[0].save()
                else:
                    RateForTag.objects.create(user=requestingـuser, tag=tag, rate=new_rate,number_of_rating=1)

            RateForDesign.objects.create(rate=new_rate, design=design, user=requestingـuser)
            return Response({"rate": new_rate, "user_account": requestingـuser.pk, "design": design.pk})

        except:
            return Response(data={"This Rate Does Not Exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#not_tested
@api_view(['POST', 'GET'])
def list_of_comments_for_design(request, *args, **kwargs):
    try:
        headers = request.headers
        token = headers["Authorization"]
        requestingـuser = UserAccount.objects.get(pk=jwt.decode(token, SECRET_KEY)["user_id"])
    except:
        return Response(data={"error": "this user does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'GET':
        params = request.GET
        _from = 0
        _row = 10
        if "_from" in params.keys():
            _from = int(params["_from"])
        if "_row" in params.keys():
            _row = int(params["_row"])
        comments = CommentForDesign.objects.all(design=kwargs["design_id"])[_from:_row]
        return_data = []
        if requestingـuser.kind != "admin":
            for comment in comments:
                if comment.isValid:
                    return_data.append({"body": comment.body, "design_id": comment.design, "user_id": comment.user})
        else:
            for comment in comments:
                return_data.append({"body": comment.body, "design_id": comment.design,
                                    "user_id": comment.user, "is_valid": comment.isValid})
        return Response(data=return_data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        try:
            design = Design.objects.get(pk=kwargs['design_id'])
            comment = CommentForDesign.objects.create(body=request.data["body"], isValid=False,
                                                      user=requestingـuser, design=design)
            return Response(data={"body": comment.body, "isValid": comment.isValid,
                                  "design": design.pk, "user": requestingـuser.pk}, status=status.HTTP_200_OK)
        except:
            return Response(data={"error": "design is not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#not_tested
@api_view(['GET', 'PUT', 'DELETE'])
def comment_for_design_operations(request, **kwargs):
    try:
        headers = request.headers
        token = headers["Authorization"]
        requestingـuser = UserAccount.objects.get(pk=jwt.decode(token, SECRET_KEY)["user_id"])
        comment = CommentForDesign.objects.get(pk=kwargs['comment_id'])
    except:
        return Response(data={"error": "this user does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if request.method == "GET":
        try:
            if requestingـuser.kind == "admin":
                return Response(data={"body": comment.body, "isValid": comment.isValid,
                                      "design": comment.design, "user": comment.user},
                                status=status.HTTP_200_OK)
            elif comment.isValid:
                return Response(data={"body": comment.body, "design": comment.design,
                                      "user": comment.user}, status=status.HTTP_200_OK)
        except:
            return Response(data={"this comment is not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == "DELETE":
        try:
            if requestingـuser.kind != "admin" and requestingـuser.pk != comment.user.pk:
                return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
            comment_id = comment.pk
            comment.delete()
            return Response(data={"id": comment_id}, status=status.HTTP_200_OK)
        except:
           return Response(data={""}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == "PUT":
        try:
            if requestingـuser.kind != "admin":
                return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
            comment.isValid = request.data["is_valid"]
            comment.save()
            return Response(data={"id": comment.pk}, status=status.HTTP_200_OK)
        except:
            return Response(data={""}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#not_tested
@api_view(['GET', 'POST', 'DELETE'])
def list_of_a_post_designers(request, *args, **kwargs):
    if request.method == "GET":
        try:
            params = request.GET
            _from = 0
            _row = 10
            if "_from" in params.keys():
                _from = int(params["_from"])
            if "_row" in params.keys():
                _row = int(params["_row"])
            design = Design.objects.get(kwargs["design_id"])

            designers = design.designer.objects.all()[_from: _row]
            all_designers = []
            for designer in designers:
                all_designers.append({"id": designer.pk, "description": designer.description})
            return Response(data=all_designers, status=status.HTTP_200_OK)
        except:
            return Response(data={"error": "this design does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        headers = request.headers
        token = headers["Authorization"]
        decoded_header = jwt.decode(token, SECRET_KEY)
        requestingـuser = UserAccount.objects.get(pk=decoded_header["user_id"])
    except:
        return Response(data={"error": "invalid user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if requestingـuser.kind != "designer" or "designer_id" not in decoded_header.keys():
        return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
    try:
        design = Design.objects.get(pk=kwargs["design_id"])
    except:
        return Response(data={"error": "design does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        designer = Designer.objects.get(pk=decoded_header["designer_id"])
    except:
        return Response(data={"error": "designer does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == "POST":
        design.designer.add(designer)
        return Response(data={"msg": "successful added"}, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        design.designer.delete(designer)
        return Response(data={"msg": "successful deleted"}, status=status.HTTP_200_OK)
