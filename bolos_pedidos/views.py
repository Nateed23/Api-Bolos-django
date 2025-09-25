

from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from .models import Bolo, Pedido, ImagemPortfolio
from .serializers import (
    RegisterSerializer,
    BoloSerializer,
    PedidoSerializer,
    CriarPedidoSerializer,
    ImagemPortfolioSerializer 
)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        return Response({
            "message": "Utilizador registado com sucesso!",
            "refresh": str(token),
            "access": str(token.access_token)
        }, status=status.HTTP_201_CREATED)


class BoloViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bolo.objects.filter(disponivel=True)
    serializer_class = BoloSerializer
    permission_classes = [permissions.AllowAny]



class PedidoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Pedido.objects.filter(cliente=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CriarPedidoSerializer
        return PedidoSerializer

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)


class ImagemPortfolioViewSet(viewsets.ReadOnlyModelViewSet):
 
    queryset = ImagemPortfolio.objects.all()
    serializer_class = ImagemPortfolioSerializer
    permission_classes = [permissions.AllowAny]
