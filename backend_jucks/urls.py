

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter


from bolos_pedidos.views import RegisterView, BoloViewSet, PedidoViewSet, ImagemPortfolioViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'bolos', BoloViewSet, basename='bolo')
router.register(r'pedidos', PedidoViewSet, basename='pedido')

router.register(r'portfolio', ImagemPortfolioViewSet, basename='portfolio')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/registro/', RegisterView.as_view(), name='registro'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
