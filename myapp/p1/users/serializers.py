from rest_framework import serializers
from cpre.models.custom_user import CustomUser
from cpre.models.role import Role
from django.core.mail import send_mail
import random
import string
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        if user.role:
            token['role'] = user.role.name
        return token
    

class PasswordUpdatedSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    old_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('password', 'old_password')

    def update(self, instance, validated_data):
        old_password = validated_data.get('old_password')
        new_password = validated_data.get('password')

        if not instance.check_password(old_password):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})

        instance.set_password(new_password)
        instance.save()
        return instance

    def validate(self, data):
        password = data.get('password')
        old_password = data.get('old_password')
        if not password or not old_password:
            raise serializers.ValidationError("Password and old password are required.")
        return data

class AdminAuthorAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone_number', 'first_name', 'last_name', 'username']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'email': {'required': False},
            'phone_number': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'username': {'required': False},
        }
    def get_queryset(self):
        return CustomUser.objects.filter(is_staff=False)
    
    def update(self, instance, validated_data):
    #  print('it reach  here')
     for attr, value in validated_data.items():
         if attr == 'password':
                continue 
         setattr(instance, attr, value)
         instance.save()
     return instance
    
class AuthorSerializer(serializers.ModelSerializer):
    verification_code = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['password', 'email', 'phone_number', 'first_name', 'last_name', 'username', 'verification_code']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'email': {'required': False},
            'phone_number': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'username': {'required': False},
        }

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        user.verification_code = verification_code
        user.save()
        send_mail(
            'Your verification code',
            f'Your verification code is {verification_code}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return user

    def validate_verification_code(self, value):
        if not value:
            raise serializers.ValidationError("Verification code is required")
        return value

    def verify_email(self, email, verification_code):
        try:
            user = CustomUser.objects.get(email=email, verification_code=verification_code)
            user.is_active = True
            user.verification_code = ''
            user.save()
            return user
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid verification code")
        
    def update_password(self, instance, password, old_password):
        if instance.check_password(old_password):
            instance.set_password(password)
            instance.save()
            return True
        return False
    
    def update(self, instance, validated_data):
     for attr, value in validated_data.items():
         if attr == 'password':
                continue 
         setattr(instance, attr, value)
         instance.save()
     return instance
    
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['password', 'email', 'phone_number', 'is_staff', 'role', 'first_name', 'last_name', 'username']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'email': {'required': False},
            'phone_number': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'username': {'required': False},
        }

    def create(self, validated_data):
        if validated_data['role'] and not validated_data.get('is_staff'):
            raise serializers.ValidationError("Non-staff users cannot have a role assigned.")
        
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
    def update_password(self, instance, password, old_password):
        if instance.check_password(old_password):
            instance.set_password(password)
            instance.save()
            return True
        return False

    def update(self, instance, validated_data):
     print('it reach  here')
     for attr, value in validated_data.items():
         if attr == 'password':
                continue 
         setattr(instance, attr, value)
         instance.save()
     return instance
    
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name', 'description', 'can_read', 'can_create', 'can_update', 'can_delete' ]