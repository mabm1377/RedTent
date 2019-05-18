import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from designs.models import Design,RateForDesign
from tag.models import Tag
from user_account.models import UserAccount


@api_view(['POST', 'GET'])
def list_of_design(request,*args, **kwargs):
    if request.method == 'POST':
        data = json.loads(request.body)
        design = Design.objects.create(**data)
        return Response({"id": design.pk, "pic": design.pic})

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
            return_data.append({"id": design.pk, "path": design.pic, "view": design.view})
        return Response(return_data)
    return Response({})


@api_view(['GET', 'PUT ', 'DELETE'])
def get_design(request, design_id):
    response_data = {}
    try:
        design = Design.objects.get(id=design_id)
        if request.method == 'GET':
            design.view += 1
            design.save()
            response_data = {"design_id": design.pk, "design_picture": design.pic,
                             "total_rate": design.total_rate, "view": design.view}

        elif request.method == 'DELETE':
            id = design.pk
            design.delete()
            response_data = {"id": id}
        elif request.method == 'PUT':
            Design.objects.update_or_create(pk=design.pk)
    except Design.DoesNotExist:
        response_data = {"error": "this design is not exist"}
    return Response(response_data)


@api_view(['GET', 'POST'])
def list_of_design_tags(request, **kwargs):
    if request.method == 'GET':
        design = Design.objects.get(pk=kwargs["design_id"])
        tags = design.tag.all()
        return_data = []
        for tag in tags:
            return_data.append({"tag_id": tag.pk, "tag_body": tag.body})

        return Response(return_data)

    elif request.method == 'POST':
        data = json.loads(request.body)
        design = Design.objects.get(pk=kwargs['design_id'])
        tag = Tag.objects.get_or_create(body=data["body"])[0]
        design.tag.add(tag)
        return Response({"tag_id": tag.pk, "body": data["body"]})


@api_view(['DELETE'])
def delete_design_tag(request,*args,**kwargs):
    if request.method == 'DELETE':
        design = Design.objects.get(pk=kwargs["design_id"])
        tag = Tag.objects.get(pk=kwargs['tag_id'])
        tag_id = tag.pk
        design.tag.remove(tag)
        return Response({"tag was deleted": tag_id})


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


@api_view(['GET'])
def test(request):
    return Response({})
