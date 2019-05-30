from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_account.models import UserAccount
from designers.models import Designer,CommentForDesigner
from rest_framework import status


@api_view(['POST'])
def add_comment(request, *args, **kwargs):
    designer_id = request.data["designer_id"]
    designer = Designer.objects.get(designer_id)
    headers = request.header
    token = headers["Authorization"]
    user = UserAccount.objects.get(token=token)
    if user:
        if designer:
            comment = CommentForDesigner.objects.create(user=user, body=request.data["body"], isvalid=False,
                                                        designer=designer)
            return Response({"id": comment.pk}, status=status.HTTP_200_OK)
        else:
            return Response({"invalid designer"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"invalid user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['DELETE'])
def delete_comment(request, *args, **kwargs):
    designer_id = request.data["designer_id"]
    designer = Designer.objects.get(designer_id)
    headers = request.header
    token = headers["Authorization"]
    user = UserAccount.objects.get(token=token)
    if user:
        if designer:
            comment = CommentForDesigner.objects.get(request.body["comment_id"])
            comment.objects.remove()
            return Response({"comment was deleted"},status=status.HTTP_200_OK)
        else:
            return Response({"invalid designer"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"invalid user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
