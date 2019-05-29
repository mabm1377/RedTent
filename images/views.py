from rest_framework.decorators import api_view
from django.http import FileResponse


@api_view(['POST', 'GET'])
def image(request, **kwargs):
    if request.method == 'GET':
        a = "/home/alibashari/PycharmProjects/new_red_tent/RedTent/" + request.path.split('/')[-1]
        response = FileResponse(open(a, 'rb'))
        return response
