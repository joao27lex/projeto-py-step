from . import views
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False)),  
    path('login/', views.login_morador, name='login'),
    path('dashboard/', views.dashboard_morador, name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('lista_areas/', views.lista_areas, name='lista_areas'),
    path('lista_areas/reservas/', views.lista_reservas, name='lista_reservas'),
    path('lista_areas/reservas/adicionar/', views.adicionar_reserva, name='adicionar_reserva'),
    path('lista_areas/reservas/deletar/<int:reserva_id>/', views.deleta_reserva, name='deleta_reserva'),

    path('lista_visitantes/', views.lista_visitantes, name='lista_visitantes'),
    path('lista_visitantes/apagar/<int:visitante_id>/', views.deleta_visitantes, name='remover_visitante'),
    
    path('lista_veiculos/', views.lista_veiculos, name='lista_veiculos'),
]

