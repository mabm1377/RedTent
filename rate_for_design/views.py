from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from designs.models import RateForDesign, Design
from user_account.models import UserAccount
from user_account.models import RateForTag


@api_view(['POST'])
def post_rate(request, *args, **kwargs):
    return_data = {}
    if request.method == "POST":
        sc = status.HTTP_200_OK
        headers = request.headers
        token = headers["Authorization"]
        user = UserAccount.objects.get(token=token)
        if user:
            design = Design.objects.get(pk=request.data["design_id"])
            if design:
                rate_for_design = RateForDesign.objects.create(user=user, rate=request.data["rate"], design=design)
                design.total_rate = design.total_rate + rate_for_design.rate
                tags = design.tag.all()
                for tag in tags:
                    rate_for_tag = RateForTag.objects.get_or_create(user=user, tag=tag)
                    rate_for_tag.number_of_rating += 1
                    rate_for_tag.rate = (rate_for_tag.rate + request.data["rate"])/rate_for_tag.number_of_rating
                    rate_for_tag.save()
                design.save()
                return_data = {"id": rate_for_design.pk}
            else:
                return_data = {"error": "this design not exist"}
                sc = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            return_data = {"error": "invalid user"}
            sc = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(return_data, status=sc)


@api_view(['PUT', 'GET'])
def rate_operation(request, *args, **kwargs):
    pass


