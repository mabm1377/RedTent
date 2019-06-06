from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from tag.models import Tag


@api_view(["GET"])
def get_list_designs_of_tags(request, *args, **kwargs):
    _from = 0
    _row = 10
    params = request.GET
    if "_from" in params:
        _from = int(params["_from"])
    if "_row" in params:
        _row = int(params["_row"])
    try:
        tag = Tag.objects.get(pk=kwargs["tag_id"])
        designs = tag.designs.all()[_from:_row]
        return_data = []
        for design in designs:
            return_data.append({"id": design.pk, "picture": str(design.picture)})
        return Response(data=return_data, status=status.HTTP_200_OK)
    except:
        return Response(data={"error": "tag does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

