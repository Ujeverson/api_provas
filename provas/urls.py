from django.urls import path
from .views import GerarProvaView, DetalharProvaView, DetalharGabaritoView

urlpatterns = [
    path('gerar-prova/', GerarProvaView.as_view(), name='gerar-prova'),
    path('provas/<int:id>/', DetalharProvaView.as_view(), name='detalhar-prova'),
    path('gabarito/<int:prova__id>/', DetalharGabaritoView.as_view(), name='detalhar-gabarito'),
]