from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def add_comment(request, *args, **kwargs):
    pass


@api_view(['DELETE'])
def delete_comment(request, *args, **kwargs):
    pass
