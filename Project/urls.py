from django.urls import path
from . import views

urlpatterns = [
    path('', views.emitir_nfe, name='emitir_nfe'),
    path('<int:pk>/', views.emitir_nfe, name='emitir_nfe'),    
]