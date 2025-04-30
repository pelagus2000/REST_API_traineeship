from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pereval.views import PerevalViewSet, PerevalDetailView, UserPerevalListView, TermsAgreementView, TermsRedirectView, \
    ModerationView, PerevalSearchView
from django.conf import settings
from django.conf.urls.static import static

# Импорты для Swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'submitData', PerevalViewSet, basename='submitdata')

# Настройка Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Pereval API",
        default_version='v1',
        description="API для работы с перевалами",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@pereval.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),

    # URLs для CRUD операций с перевалами
    path('api/v1/pereval/<int:pk>/', PerevalDetailView.as_view(), name='pereval-detail'),
    path('api/v1/pereval/user/', UserPerevalListView.as_view(), name='user-pereval-list'),

    # URLs для соглашения с условиями
    path('terms/', TermsAgreementView.as_view(), name='terms'),
    path('terms-redirect/', TermsRedirectView.as_view(), name='terms-redirect'),

    # URLs для Swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    #for moderators
    path('api/v1/pereval/<int:pk>/moderate/', ModerationView.as_view(), name='pereval-moderate'),

    #search instrument
    path('api/v1/pereval/search/', PerevalSearchView.as_view(), name='pereval-search'),
]


# Настройка для обработки медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)