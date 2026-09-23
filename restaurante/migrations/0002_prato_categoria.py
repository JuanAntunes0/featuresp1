from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurante', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prato',
            name='categoria',
            field=models.CharField(
                choices=[
                    ('ENTRADA', 'Entrada'),
                    ('PRINCIPAL', 'Prato principal'),
                    ('SOBREMESA', 'Sobremesa'),
                    ('BEBIDA', 'Bebida'),
                ],
                default='PRINCIPAL',
                max_length=20,
            ),
        ),
    ]
