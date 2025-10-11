
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    BoloViewSet,
    PedidoViewSet,
    ImagemPortfolioViewSet
)

router = DefaultRouter()
router.register(r'bolos', BoloViewSet, basename='bolo')
router.register(r'pedidos', PedidoViewSet, basename='pedido')
router.register(r'portfolio', ImagemPortfolioViewSet, basename='portfolio')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    
    path('', include(router.urls)),
]