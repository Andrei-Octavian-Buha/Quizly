from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer


class CookieLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        access = validated_data.get("access")
        refresh = validated_data.get("refresh")
        user_data = validated_data.get("user")

        response = Response(
            {
                "detail": "Login successfully!",
                "user": user_data
            })
        
        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=True,
            samesite="Lax"
        )
        return response
    
class CookieLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass
        response = Response(
            {"detail":"Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."},
            status=status.HTTP_200_OK
        )

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response          
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "detail":"User created successfully!"
                }, status=status.HTTP_201_CREATED
            )
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)