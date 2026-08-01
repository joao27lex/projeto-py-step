from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .models import  Visitante, AreaComum, Reserva, Encomenda, Veiculo


# Create your views here.

def login_morador(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'erro': 'Usuário ou senha inválidos'})
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

@login_required(login_url='login')
def listar_template(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})


@login_required
def lista_areas(request):
    # filtra as áreas comuns que estão ativas
    areas = AreaComum.objects.filter(ativo = True)

    #renderiza o template html passando as áreas como contexto
    return render(request, 'lista_areas.html', {'areas': areas})


@login_required
def lista_reservas(request):
    from datetime import date
    hoje = date.today()
    
    
    reservas = Reserva.objects.filter(morador=request.user.morador, data__gte=hoje).order_by('data', 'hora_inicio')
    
    areas = AreaComum.objects.filter(ativo=True)
    
    return render(request, 'core/lista_reservas.html', {'reservas': reservas, 'areas': areas})

@login_required
def adicionar_reserva(request):
    if request.method == 'POST':
        area_id = request.POST.get('area')
        data = request.POST.get('data')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fim = request.POST.get('hora_fim')
        morador = request.user.morador
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
            morador=morador,
            data=data,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim
        )
        
        messages.success(request, "Reserva efetuada com sucesso!")
        return redirect('lista_reservas')

    return redirect('lista_reservas')

@login_required
def deleta_reserva(request, reserva_id):

    # acessa o apartamento do morador relacionado ao usuário logado
    apartamento = request.user.morador.apartamento

    reserva = get_object_or_404(Reserva, id=reserva_id, apartamento=apartamento)

    if request.method == 'POST':
        reserva.delete()
        return redirect('lista_reservas')
    

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

@login_required
def lista_veiculos(request):

    # acessa o apartamento do morador relacionado ao usuário logado
    apartamento = request.user.morador.apartamento

    # filtra os veículos relacionados ao morador logado
    veiculos = Veiculo.objects.filter(apartamento = apartamento)

    # renderiza o template html passando os veículos como contexto
    return render(request, 'lista_veiculos.html', {'veiculos': veiculos})
    