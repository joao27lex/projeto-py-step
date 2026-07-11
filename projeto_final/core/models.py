from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Morador, representando um usuário do sistema que reside no condomínio.
class Morador(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    apartamento = models.CharField(max_length = 4)
    cpf = models.CharField(max_length = 11, unique = True, null=True, blank=True)  

    def __str__(self):
        return f'{self.user.username} - Apartamento {self.apartamento}'
    

class Visitante(models.Model):
    nome = models.CharField(max_length = 100)
    cpf = models.CharField(max_length = 11, unique = True)
    apartamento = models.ForeignKey(Morador, on_delete = models.CASCADE)
    data_visita = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.nome} - {self.cpf}'

# Area de uso comum do condomínio, como salão de festas, churrasqueira, piscina, etc.
class AreaComum(models.Model):
    nome = models.CharField(max_length = 100)
    descricao = models.TextField(blank = True)
    ativo = models.BooleanField(default = True)

    def __str__(self):
        return f'{self.nome}, {self.descricao}, {"Ativo" if self.ativo else "Inativo"}'


# Modelo de horários de funcionamento para cada área comum, permitindo definir horários diferentes para cada dia da semana.
class HorariosFuncionamento(models.Model):

    DIAS_DA_SEMANA = [(0, 'Segunda'), (1, 'Terça'), (2, 'Quarta'), (3, 'Quinta'), (4, 'Sexta'), (5, 'Sábado'), (6, 'Domingo'),]

    area = models.ForeignKey(AreaComum, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.IntegerField(choices=DIAS_DA_SEMANA)
    abertura = models.TimeField()
    fechamento = models.TimeField()

    class Meta:
        ordering = ['dia_semana']

    def __str__(self):
        return f"{self.area.nome} - {self.get_dia_semana_display()}"
    

# Reserva de uma área comum por um morador, incluindo a data e o horário da reserva.
class Reserva(models.Model):
    area = models.ForeignKey(AreaComum, on_delete = models.CASCADE, related_name = 'reservas')
    morador = models.ForeignKey(Morador, on_delete = models.CASCADE)
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    criado_em = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Reserva de {self.morador} para {self.area.nome} em {self.data} das {self.hora_inicio} às {self.hora_fim}"
    

class Encomenda(models.Model):
    apartamento = models.ForeignKey(Morador, on_delete = models.CASCADE)
    descricao = models.CharField(max_length = 255, blank = True)
    recebido_em = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Encomenda para {self.apartamento} - {self.descricao}"

class TipoVeiculo(models.TextChoices):
    CARRO = 'Carro', 'Carro' #valor(supabase), valor legível
    MOTO = 'Moto', 'Moto'
    OUTRO = 'Outro', 'Outro'

class Veiculo(models.Model):
    morador = models.ForeignKey(Morador, on_delete = models.CASCADE)
    placa = models.CharField(max_length = 10)
    tipo = models.CharField(max_length = 20, choices=TipoVeiculo.choices)
    modelo = models.CharField(max_length = 100)
    cor = models.CharField(max_length = 50)

    def __str__(self):
        return f"{self.modelo} - {self.placa} ({self.cor})"
    