from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import Morador, Visitante, AreaComum, HorariosFuncionamento, Reserva, Encomenda, Veiculo


# Create your views here.
class LoginMoradorView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/dashboard/' 

# Dashboard protegido que apenas moradores logados acessam
@login_required
def dashboard_morador(request):
    morador = request.user.morador  # Acessando o morador relacionado ao usuário logado

    #filtra dados específicos do morador
    contexto = {
        'encomendas': Encomenda.objects.filter(apartamento=morador),
        'reservas': Reserva.objects.filter(morador = morador),
        'veiculos': Veiculo.objects.filter(morador = morador),
        'visitantes': Visitante.objects.filter(apartamento = morador),
    }

    return render(request, 'dashboard.html', contexto)  


@login_required
def lista_visitantes(request):
    visitantes = Visitante.objects.filter(apartamento=request.user.morador)
    return render(request, 'lista_visitantes.html', {'visitantes': visitantes})
