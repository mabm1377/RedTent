from rest_framework.decorators import api_view
from rest_framework.response import Response
from designers.models import RateForDesigner
from  user_account.models import UserAccount
from designers.models import Designer
from rest_framework import status


@api_view(['POST'])
def post_rate(request, *args, **kwargs):
    headers = request.header
    token = headers["Authorization"]
    user = UserAccount.objects.get(token=token)
    designer_id = request.data["designer_id"]
    designer = Designer.objects.get(designer_id)
    if user:
        if designer:
            rate = RateForDesigner.objects.create(rate=request.body["rate"], user=user, designer=designer)
            return Response({"rate_id": rate.pk}, status=status.HTTP_200_OK)

        else:
            return Response({"Wrong designer"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"invalid user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def rate_operation(request, rate_for_designer_id, **kwargs):
    rate = RateForDesigner.objects.get(rate_for_designer_id)
    if rate:
        return Response({"rate_id": rate_for_designer_id, "rate": rate.rate, "user": rate.user.pk,
                         "designer": rate.designer.pk})
    else:
        return Response({"No rate"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

