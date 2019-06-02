from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from tag.models import Tag


@api_view(["GET"])
def get_list_designs_of_tags(request, *args, **kwargs):
    _from = 0
    _row = 10
    if "_from" in kwargs.keys() and kwargs["_from"]:
        _from = int(kwargs["_from"])
    if "_row" in kwargs.keys() and kwargs["_row"]:
        _row = int(kwargs["_row"])
    try:
        tag = Tag.objects.get(pk=kwargs["tag_id"])
        designs = tag.designs.all()[_from:_row]
        return_data = []
        for design in designs:
            return_data.append({"id": design.pk, "path": design.picture})
        return Response(data=return_data, status=status.HTTP_200_OK)
    except:
        return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

