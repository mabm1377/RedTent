from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def post_rate(request, *args, **kwargs):
    pass


@api_view(['PUT', 'GET'])
def rate_operation(request, *args, **kwargs):
    pass


