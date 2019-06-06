from rest_framework.decorators import api_view
from user_account.models import UserAccount
from rest_framework.response import Response
from rest_framework import status
from site_images.models import OtherImages
import jwt
from redtent.settings import SECRET_KEY


@api_view(["POST"])
def add_image(request, *args, **kwargs):
    if request.method == "POST":

        try:
            headers = request.headers
            token = headers["Authorization"]
            requestingـuser = UserAccount.objects.get(pk=jwt.decode(token, SECRET_KEY)["user_id"])
        except:
            return Response(data={"error": "invalid user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if requestingـuser.kind != "admin":
        return Response(data={"error": "access denied"}, status=status.HTTP_403_FORBIDDEN)
    other_images = OtherImages(image=request.data["image"])
    other_images.save()
    return Response(data={"image": str(other_images.image)}, status=status.HTTP_200_OK)

