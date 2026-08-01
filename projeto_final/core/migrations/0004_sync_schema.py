import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_morador_cpf'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reserva',
            old_name='morador',
            new_name='apartamento',
        ),
        migrations.RenameField(
            model_name='veiculo',
            old_name='morador',
            new_name='apartamento',
        ),
        migrations.RenameField(
            model_name='veiculo',
            old_name='tipo',
            new_name='tipo_veiculo',
        ),
        migrations.AddField(
            model_name='encomenda',
            name='status',
            field=models.CharField(choices=[('Pendente', 'Pendente'), ('Entregue', 'Entregue')], default='Pendente', max_length=20),
        ),
        migrations.AlterField(
            model_name='veiculo',
            name='tipo_veiculo',
            field=models.CharField(choices=[('Carro', 'Carro'), ('Moto', 'Moto'), ('Outro', 'Outro')], default='Carro', max_length=20),
        ),
        migrations.AddField(
            model_name='veiculo',
            name='marca',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='veiculo',
            name='ano',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
