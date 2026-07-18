from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import Morador, Visitante, AreaComum, HorariosFuncionamento, Reserva, Encomenda, Veiculo


# Create your views here.

def login_morador(request):
    return render(request, 'login.html')

# apenas quem tem login acessa
@login_required
def dashboard_morador(request):
    # acessa o morador relacionado ao usuário logado
    apartamento = request.user.morador.apartamento 

    #filtra as encomendas do apartamento do morador que estao pendentes
    encomendas = Encomenda.objects.filter(apartamento = apartamento, status = 'pendente')

    # renderiza o template html passando as encomendas como contexto
    return render(request, 'dashboard.html', {'encomendas': encomendas})  


@login_required
def lista_areas(request):
    # filtra as áreas comuns que estão ativas
    areas = AreaComum.objects.filter(ativo = True)

    #renderiza o template html passando as áreas como contexto
    return render(request, 'lista_areas.html', {'areas': areas})


@login_required
def lista_reservas(request):
    hoje = date.today()

    # acessa o morador relacionado ao usuário logado
    apartamento = request.user.morador.apartamento
    
    #filtra as reservas do morador de hoje em diante
    #ordenado por data e hora de início
    reservas = Reserva.objects.filter(apartamento = apartamento, data__gte = hoje).order_by('data', 'hora_inicio')

    # renderiza o template html passando as reservas como contexto
    return render(request, 'lista_reservas.html', {'reservas': reservas})

@login_required
def deleta_reserva(request, reserva_id):

    # acessa o apartamento do morador relacionado ao usuário logado
    apartamento = request.user.morador.apartamento

    reserva = get_object_or_404(Reserva, id=reserva_id, apartamento=apartamento)

    if request.method == 'POST':
        reserva.delete()
        return redirect('lista_reservas')
    
    # renderiza o template html de confirmação de deletar reserva, passando a reserva como contexto
    return render(request, 'deleta_reserva.html', {'reserva': reserva})

@login_required
def lista_visitantes(request):

    # acessa o apartamento do morador relacionado ao usuário logado
    apartamento = request.user.morador.apartamento

    # filtra os visitantes relacionados ao apartamento do morador
    visitantes = Visitante.objects.filter(apartamento=apartamento)

    # renderiza o template html passando os visitantes como contexto
    return render(request, 'lista_visitantes.html', {'visitantes': visitantes})


@login_required
def deleta_visitantes(request, visitante_id):

    # acessa o apartamento do morador relacionado ao usuário logado
    apartamento = request.user.morador.apartamento

    #filtra o visitante pelo id e pelo apartamento do morador, garantindo que o morador só possa deletar visitantes do seu próprio apartamento
    visitante = get_object_or_404(Visitante, id=visitante_id, apartamento = apartamento)
    if request.method == 'POST':
        visitante.delete()

        # redireciona para a lista de visitantes após a exclusão
        return redirect('lista_visitantes')
    
    # renderiza o template html de confirmação de deletar visitante, passando o visitante como contexto
    return render(request, 'deleta_visitantes.html', {'visitante': visitante})

@login_required
def lista_veiculos(request):

    # acessa o apartamento do morador relacionado ao usuário logado
    apartamento = request.user.morador.apartamento

    # filtra os veículos relacionados ao morador logado
    veiculos = Veiculo.objects.filter(apartamento = apartamento)

    # renderiza o template html passando os veículos como contexto
    return render(request, 'lista_veiculos.html', {'veiculos': veiculos})
    