from rest_framework.decorators import api_view
from rest_framework.response import  Response
@api_view(['POST', 'GET'])
def test(request,**kwargs):
    return Response({"asd":"hoora"})