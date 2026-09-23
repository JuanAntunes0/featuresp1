from django.db import models


class Prato(models.Model):
    CATEGORIA_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('PRINCIPAL', 'Prato principal'),
        ('SOBREMESA', 'Sobremesa'),
        ('BEBIDA', 'Bebida'),
    ]

    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='PRINCIPAL')
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Combo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Mesa(models.Model):
    numero = models.IntegerField(unique=True)

    STATUS_CHOICES = [
        ('LIVRE', 'Livre'),
        ('OCUPADA', 'Ocupada'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='LIVRE'
    )

    def __str__(self):
        return f'Mesa {self.numero}'


class Comanda(models.Model):
    mesa = models.ForeignKey(
        Mesa,
        on_delete=models.CASCADE
    )

    data_abertura = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('ABERTA', 'Aberta'),
        ('FECHADA', 'Fechada'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ABERTA'
    )

    def __str__(self):
        return f'Comanda da Mesa {self.mesa.numero}'


class Item(models.Model):
    comanda = models.ForeignKey(
        Comanda,
        on_delete=models.CASCADE,
        related_name='itens'
    )

    prato = models.ForeignKey(
        Prato,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    combo = models.ForeignKey(
        Combo,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    quantidade = models.IntegerField(default=1)

    def __str__(self):
        if self.prato:
            return f'{self.quantidade}x {self.prato.nome}'
        return f'{self.quantidade}x {self.combo.nome}'