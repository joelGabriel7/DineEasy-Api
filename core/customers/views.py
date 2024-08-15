from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter
from .models import CustomerUser
from core.customers.serializer import (RegisterSerializer, UserProfileSerializer)


@extend_schema(tags=['Customers'])
class RegisterView(CreateAPIView):
    queryset = CustomerUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Registrar Usuario",
        description="Permite a un nuevo usuario registrarse en el sistema.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(tags=['Customers'])
class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_object(self):
        return self.request.user

    @extend_schema(
        summary="Obtener Perfil de Usuario",
        description="Recupera el perfil del usuario autenticado.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar Perfil de Usuario",
        description="Actualiza el perfil del usuario autenticado.",
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar Parcialmente Perfil de Usuario",
        description="Actualiza parcialmente el perfil del usuario autenticado.",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


@extend_schema(tags=['Customers'])
class UserListView(ListAPIView):
    queryset = CustomerUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    filter_backends = [SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']

    @extend_schema(
        summary="Listar Usuarios",
        description="Obtiene una lista de todos los usuarios registrados. Permite búsqueda por username, email, nombre y apellido.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
