from rest_framework import generics, permissions
from cpre.models.custom_user import CustomUser
from cpre.models.role import Role
from .serializers import AuthorSerializer , RoleSerializer, AdminSerializer, PasswordUpdatedSerializer, AdminAuthorAllSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .permissions import IsStaffUser, IsRoleCreate, IsRoleReader, IsRoleCanUpdate, IsRoleCanDelete, IsUserAuthor
from rest_framework import serializers

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class RigisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AuthorSerializer

    # def post(self, request, *args, **kwargs):
    #     response =  super().create(request, *args, **kwargs)
    #     print('😀😀😀😀😀',response.data['verification_code'])
    #     response.headers['X-CONTENT-verification_code'] = response.data['verification_code']
    #     return response

class VerifyEmailView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = AuthorSerializer()
        email = request.data.get('email')
        verification_code = request.data.get('verification_code')
        try:
            user = serializer.verify_email(email, verification_code)
            return Response({'detail': 'Email verified successfully.'}, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class UpdatePasswordView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsUserAuthor)
    queryset = CustomUser.objects.all()
    serializer_class = PasswordUpdatedSerializer

class AdminAuthorAll(viewsets.ModelViewSet):
    permission_classes = (IsRoleReader, permissions.IsAuthenticated, IsStaffUser, IsRoleCanUpdate)
    queryset = CustomUser.objects.all()
    serializer_class = AdminAuthorAllSerializer
    
class UpdateAdminPasswordView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsStaffUser, IsRoleCanUpdate)
    queryset = CustomUser.objects.all()
    serializer_class = PasswordUpdatedSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffUser, IsRoleCreate]

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserAuthor]

class RegisterAdminView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsStaffUser, IsRoleCreate)
    serializer_class = AdminSerializer
    queryset = CustomUser.objects.all()
