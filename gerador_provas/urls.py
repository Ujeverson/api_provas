"""
URL configuration for gerador_provas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import ( # Importando as views do Simple JWT
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView

# Configuração do Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API de Geração de Provas",
        default_version='v1',
        description="Ujeverson Tavares Sampaio \n \n API para criação de provas personalizadas com base em critérios como tema, nível de dificuldade (Taxonomia de Bloom) e formato das questões. \n \n Projeto final da disciplina de Construção de APIs para Inteligência Artificial da Especialização em Sistemas e Agentes Inteligentes UFG.",
        
        terms_of_service="https:bit.ly/ujeverson", 
        contact=openapi.Contact(email="ujeverson@gmail.com"),  
        license=openapi.License(name="MIT License"),  
    ),
    public=True,
    permission_classes=(permissions.AllowAny,), #Qualquer um pode ver
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('provas.urls')),

    # URLs do Swagger e Redoc
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # URLs do Simple JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
