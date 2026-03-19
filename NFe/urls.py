from django.urls import path
from . import views

urlpatterns = [
    path('', views.emitir_nfe, name='emitir_nfe'),
    path('<int:pk>/', views.gerenciar_nfe, name='gerenciar_nfe'),   
    path('emissao/', views.emitir_nfe, name='emissao_nfe'), 
    path('arquivos/<int:nfe_id>/', views.abrir_pasta_arquivos, name='abrir_pasta_arquivos'),
]
