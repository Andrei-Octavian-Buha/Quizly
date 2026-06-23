from django.db import transaction, IntegrityError
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for handling new user registration requests.
    
    Validates user credentials, ensures email uniqueness, confirms password 
    matching, and creates user records safely using database transactions.
    """
    password = serializers.CharField(write_only=True)
    confirmed_password = serializers.CharField(write_only=True)
    class Meta():
        model = User
        fields = ['username','email','password','confirmed_password']
    
    def validate(self, data):
        if data["password"] != data["confirmed_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already  exist")
        return value
    
    def create(self, validated_data):
        validated_data.pop("confirmed_password")
        try:
            with transaction.atomic():
                user = User.objects.create_user(**validated_data)
                return user
        except IntegrityError:
            raise serializers.ValidationError({"detail":"Try again! We have a error to save your data right now"})
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT Token serializer extending SimpleJWT's base class.
    
    Injects a serialized representation of the user's basic profile details 
    directly into the validation payload, allowing authentication views to 
    extract and pass user meta-information down to the client.
    """
    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"]= {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
        }
        return data



























        