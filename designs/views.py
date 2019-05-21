import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from designs.models import Design, RateForDesign, CommentForDesign
from tag.models import Tag
from user_account.models import UserAccount
from designers.models import Designer
import os


@api_view(['POST', 'GET'])
def list_of_design(request,*args, **kwargs):
    if request.method == 'POST':
        design = Design(picture=request.data["image"])
        design.save()
        return Response({"id": design.pk, "path": str(design.picture)})

    elif request.method == 'GET':
        designs = []
        _from = 0
        _row = 10
        if "_from" in kwargs.keys() and kwargs["_from"]:
            _from = int(kwargs["_from"])
        if "_row" in kwargs.keys() and kwargs["_row"]:
            _row = int(kwargs["_row"])
        if "_order_by" in kwargs.keys() and kwargs["_order_by"]:
            designs = Design.objects.filter().order_by('-'+kwargs["_order_by"])[_from:_row]
        else:
            designs = Design.objects.all()[_from:_row]
        return_data = []
        for design in designs:
            return_data.append({"id": design.pk, "path": str(design.picture), "view": design.view})
        return Response(return_data)
    return Response({})


@api_view(['GET', 'DELETE'])
def get_design(request, design_id):
    sc = status.HTTP_200_OK
    response_data = {}
    try:
        design = Design.objects.get(id=design_id)
        if request.method == 'GET':
            design.view += 1
            design.save()
            response_data = {"design_id": design.pk, "design_picture": str(design.picture),
                             "rate": design.total_rate, "view": design.view}

        elif request.method == 'DELETE':
            id = design.pk
            design.delete()
            response_data = {"id": id}
    except Design.DoesNotExist:
        response_data = {"error": "this design is not exist"}
        sc = status.HTTP_404_NOT_FOUND
    return Response(response_data, status=sc)


@api_view(['GET', 'POST', 'PUT'])
def list_of_design_tags(request, **kwargs):
    if request.method == 'GET':
        design = Design.objects.get(pk=kwargs["design_id"])
        tags = design.tag.all()
        return_data = []
        for tag in tags:
            return_data.append({"id": tag.pk, "tag_body": tag.name})

        return Response(return_data)

    elif request.method == 'POST':
        status_code = status.HTTP_200_OK
        return_data = {}
        try:
            data = dict(request.data)
            design = Design.objects.get(pk=kwargs['design_id'])
            for tag in data["tags"]:
                new_tag = Tag.objects.get_or_create(name=tag)[0]
                design.tag.add(new_tag)
            return_data = Response({"id": design.pk, "tags": data["tags"]})
        except:
            return_data = {"error": "invalid tags or design"}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(return_data, status=status_code)

    elif request.method == 'PUT':
        status_code = status.HTTP_200_OK
        return_data = {}
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

            return_data = {"tags": list(design.tag.all().values())}
        except:
            return_data = {"error": "this design does not exist"}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(return_data, status = status_code)



#not_tested
@api_view(['GET'])
def get_myrate(request, design_id, **kwargs):
    token = request.headers["Authorization"]
    user = UserAccount.objects.get(token=token)
    rate = RateForDesign.objects.filter(design=design_id).filter(user=user.pk)[0]
    return Response({"rate": rate.rate})


#not_tested
@api_view(['GET', 'POST'])
def list_of_rates_for_design(request, **kwargs):
    if request.method == 'GET':
        _from = 0
        _row = 10
        if "_from" in kwargs.keys():
            _from = kwargs["_from"]
        if "_row" in kwargs.keys():
            _row = kwargs["_row"]
        rates = RateForDesign.objects.all(design=kwargs["design_id"])[_from:_row]
        return_data = []
        for rate in rates:
            return_data.append({"rate": rate.rate, "design": rate.design, "user": rate.user})
            return Response(return_data)
    elif request.method == 'POST':
        try:
            new_rate = json.loads(request.body)["rate"]
            headers = request.headers
            token = headers["Authorization"]
            user = UserAccount.objects.get(token=token)
            design = Design.objects.get(pk=kwargs["design_id"])
            last_number_of_rates = len(RateForDesign.objects.filter(design=design))
            design.total_rate = (design.total_rate + new_rate)/(last_number_of_rates+1)
            design.save()
            RateForDesign.object.create(rate=new_rate, design=design, user=user)
            return Response({"rate": new_rate, "user_account": user.pk, "design": design.pk})
        except:
            return {"This Rate Does Not Exist"}


#not_tested
@api_view(["GET", "PUT", "DELETE"])
def rate_for_design_operations(request, rate_for_design_id, *args, **kwargs):
    if request.method == "GET":
        rate = RateForDesign.objects.get(id=rate_for_design_id)
        user = rate.user
        design = rate.design
        return Response({"rate": rate.rate, "user": user.pk, "design": design.pk})
    if request.method == "PUT":
        newrate = json.loads(request.body)["rate"]
        rate = RateForDesign.objects.get(id=rate_for_design_id)
        rate.rate = newrate
        rate.save()
        return Response({"rate_id": rate_for_design_id, "rate": rate.rate})
    if request.method == "DELETE":
        rate = RateForDesign.objects.get(id=rate_for_design_id)
        rate_id = rate.pk
        rate.delete()
        return Response({"deleted_rate": rate_id})


#not_tested
@api_view(['POST', 'GET'])
def list_of_comments_for_design(request, **kwargs):
    if request.method == 'GET':
        _from = 0
        _row = 10
        if "_from" in kwargs.keys():
            _from = kwargs["_from"]
        if "_row" in kwargs.keys():
            _row = kwargs["_row"]
        comments = CommentForDesign.objects.all(design=kwargs["design_id"])[_from:_row]
        return_data = []
        for comment in comments:
            if comment.isValid:
                return_data.append({"body": comment.body, "design": comment.design, "user": comment.user})
                return Response(return_data)

    elif request.method == 'POST':
        data = json.loads(request.body)["body"]
        try:
            design = Design.objects.get(pk=kwargs['design_id'])
            headers = request.headers
            token = headers["Authorization"]
            user = UserAccount.objects.get(token=token)
            comment = CommentForDesign.objects.create(body=data, isValid=False, user=user, design=design)
            return Response({"body": comment.body, "isValid": comment.isValid, "design": design.pk, "user": user.pk})
        except:
            return Response({"error": "design is not exist"})


#not_tested
@api_view(['GET', 'DELETE'])
def comment_for_design_operations(request, **kwargs):
    if request.method == "GET":
        try:
            comment = CommentForDesign.objects.get(pk=kwargs['comment_Id'])
            if comment:
                return Response({"body": comment.body, "isValid": comment.isValid, "design": comment.design, "user": comment.user})
        except:
            return Response({"this comment is not exist"})
    if request.method == "DELETE":
        try:
            headers = request.headers
            token = headers["Authorization"]
            user = UserAccount.objects.get(token=token)
            comment = CommentForDesign.objects.get(pk=kwargs['comment_Id'])
            if comment:
                if comment.user.pk == user.pk:
                    comment.delete()
                    return Response({"Comment was deleted"})
                else:
                    return Response({"This user cannot delete this comment"})
        except:
            raise ("this comment is not exist")


#not_tested (delete mikhad)
@api_view(['GET', 'POST'])
def list_of_a_post_designers(request, design_id, **kwargs):
    if request.method == "GET":
        try:
            design = Design.objects.get(pk=design_id)
            if design:
                designers = Design.designer.objects.all()
                return_data = []
                for designer in designers:
                    return_data.append({"designer": os.path.join("designers", str(designer.pk))})
                return Response(return_data)
        except:
            raise ("this design is not exist")
    if request.method == "POST":
        data = json.loads(request.body)
        design = None
        try:
            design = Design.objects.get(pk=design_id)
        except:
            if design:
                headers = request.header
                token = headers["Authorization"]
                user = UserAccount.objects.get(token=token)
                if user.isDesigner:
                    designer = Designer.objects.get_or_create(**data)
                    design.designer.add(designer)
                    return Response({"designer_id": designer.pk})
                else:
                    return Response({"Access Denied"})
