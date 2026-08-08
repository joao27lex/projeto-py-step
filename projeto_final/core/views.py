from datetime import date

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Morador, Visitante, AreaComum, HorariosFuncionamento, Reserva, Encomenda, Veiculo, StatusEncomenda


# Create your views here.

def login_morador(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def get_morador(user):
    # retorna o morador relacionado ao usuário, criando caso ainda não exista
    return Morador.objects.get_or_create(user=user, defaults={'apartamento': '0000'})[0]

# apenas quem tem login acessa
@login_required
def dashboard_morador(request):
    # acessa o morador relacionado ao usuário logado
    morador = get_morador(request.user)

    #filtra as encomendas do apartamento do morador que estao pendentes
    encomendas = Encomenda.objects.filter(apartamento = morador, status = StatusEncomenda.PENDENTE)

    contexto = {
        "encomendas": encomendas,
        "total_encomendas": encomendas.count()
    }

    # renderiza o template html passando as encomendas como contexto
    return render(request, 'dashboard.html',  contexto)  


@login_required
def lista_areas(request):
    # filtra as áreas comuns que estão ativas
    areas = AreaComum.objects.filter()

    #renderiza o template html passando as áreas como contexto
    return render(request, 'lista-areas.html', {'areas': areas})


@login_required
def lista_reservas(request):
    from datetime import date
    hoje = date.today()
    
    
    reservas = Reserva.objects.filter(apartamento=get_morador(request.user), data__gte=hoje).order_by('data', 'hora_inicio')
    
    areas = AreaComum.objects.filter(ativo=True)
    
    return render(request, 'lista-reservas.html', {'reservas': reservas, 'areas': areas})

@login_required
def adicionar_reserva(request):
    if request.method == 'POST':
        area_id = request.POST.get('area')
        data = request.POST.get('data')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fim = request.POST.get('hora_fim')
        morador = get_morador(request.user)
        area = get_object_or_404(AreaComum, id=area_id)

        # verifica se existe alguma reserva no mesmo dia que se sobreponha ao horário pedido
        conflitos = Reserva.objects.filter(
            area=area,
            data=data,
            hora_inicio__lt=hora_fim,  # A hora de início da reserva existente é menor que a nova hora de fim
            hora_fim__gt=hora_inicio   # A hora de fim da reserva existente é maior que a nova hora de início
        )

        if conflitos.exists():
            messages.error(request, f"Lamentamos, mas a área '{area.nome}' já está reservada neste horário.")
            return redirect('lista_reservas')

        #se nao tiver conflito, cria a reserva
        Reserva.objects.create(
            area=area,
            apartamento=morador,
            data=data,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim
        )
        
        messages.success(request, "Reserva efetuada com sucesso!")
        return redirect('lista_reservas')

    return redirect('lista_reservas')

@login_required
def deleta_reserva(request, reserva_id):

    morador = get_morador(request.user)

    reserva = get_object_or_404(Reserva, id=reserva_id, apartamento=morador)

    if request.method == 'POST':
        reserva.delete()
        return redirect('lista_reservas')
    
    # renderiza o template html de confirmação de deletar reserva, passando a reserva como contexto
    return render(request, 'deleta-reservas.html', {'reserva': reserva})

@login_required
def lista_visitantes(request):

    # acessa o apartamento do morador relacionado ao usuário logado
    morador = get_morador(request.user)

    # filtra os visitantes relacionados ao apartamento do morador
    visitantes = Visitante.objects.filter(apartamento=morador)

    # renderiza o template html passando os visitantes como contexto
    return render(request, 'lista-visitantes.html', {'visitantes': visitantes})


@login_required
def deleta_visitantes(request, visitante_id):
    morador = get_morador(request.user)

    #filtra o visitante pelo id e pelo apartamento do morador, garantindo que o morador só possa deletar visitantes do seu próprio apartamento
    visitante = get_object_or_404(Visitante, id=visitante_id, apartamento = morador)
    if request.method == 'POST':
        visitante.delete()

        # redireciona para a lista de visitantes após a exclusão
        return redirect('lista_visitantes')
    
    # renderiza o template html de confirmação de deletar visitante, passando o visitante como contexto
    return render(request, 'deleta-visitantes.html', {'visitante': visitante})

@login_required
def lista_veiculos(request):

    morador = get_morador(request.user)

    # filtra os veículos relacionados ao morador logado
    veiculos = Veiculo.objects.filter(apartamento = morador)

    # renderiza o template html passando os veículos como contexto
    return render(request, 'lista-veiculos.html', {'veiculos': veiculos})
    