from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_rights(request):
    user = request.user
    is_admin = False

    if user.is_superuser or user.is_staff:
        is_admin = True

    return Response({"is_admin": is_admin})


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username:
            return Response({"message": "Uživatelské jméno je povinné!",
                             "error": "no username"},
                            status=status.HTTP_400_BAD_REQUEST)

        elif not password:
            return Response({"message": "Heslo je povinné!",
                             "error": "no password"},
                            status=status.HTTP_400_BAD_REQUEST)

        elif User.objects.filter(username=username).exists():
            return Response({"message": "Uživatelské jméno už existuje!",
                             "error": "username exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        User.objects.create(username=username,
                            password=make_password(password))
        return Response({"message": "Účet vytvořen!"},
                        status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(type(e).__name__, e.args)
            return Response(status=status.HTTP_400_BAD_REQUEST)