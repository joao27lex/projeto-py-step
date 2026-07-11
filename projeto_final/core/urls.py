from django.urls import path
from .views import LoginMoradorView, dashboard_morador
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', LoginMoradorView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard_morador, name='dashboard'),
    path('lista_areas/', dashboard_morador, name='lista_reservas'),
    path('lista_visitantes/', dashboard_morador, name='lista_visitantes'),
    path('lista_veiculos/', dashboard_morador, name='lista_veiculos'),
]

