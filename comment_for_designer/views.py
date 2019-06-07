from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_account.models import UserAccount
from designers.models import Designer,CommentForDesigner
from rest_framework import status
import jwt
from redtent.settings import SECRET_KEY


@api_view(['GET'])
def comment_list(request, *args, **kwargs):
    try:
        headers = request.headers
        token = headers["Authorization"]
        header_information = jwt.decode(token, SECRET_KEY)
        requestingـuser = UserAccount.objects.get(pk=header_information["user_id"])
    except:
        return Response(data={"error": "invalid user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if requestingـuser.kind != "admin":
        return Response(data={"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
    params=request.GET
    _from = 0
    _row = 10
    is_valid = True
    if "_from" in params.keys():
        _from = params["_from"]
    if "_row" in params.keys():
        _row = params["_row"]
    if "_is_valid" in params.keys():
        is_valid = params["_is_valid"]
    try:
        comments = CommentForDesigner.objects.filter(isvalid=is_valid)[_from:_row]
        all_comments = []
        if requestingـuser.kind != "admin":
            return Response(data={})
        for comment in comments:
            all_comments.append({"designer_id":comment.designer.pk, "user_id":comment.user.pk})
    except:
        pass


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
