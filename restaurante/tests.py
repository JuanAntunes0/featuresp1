from django.test import TestCase

from .forms import PratoForm
from .models import Prato


class FeatureP1TestCase(TestCase):
    def test_preco_nao_pode_ser_zero(self):
        form = PratoForm(data={
            'nome': 'Prato Teste',
            'categoria': 'PRINCIPAL',
            'descricao': 'Descrição do prato',
            'preco': '0',
            'disponivel': 'on',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('preco', form.errors)

    def test_busca_e_filtro_por_categoria(self):
        Prato.objects.create(
            nome='Hambúrguer Artesanal',
            categoria='PRINCIPAL',
            descricao='Hambúrguer da casa',
            preco=25,
            disponivel=True,
        )
        Prato.objects.create(
            nome='Brownie',
            categoria='SOBREMESA',
            descricao='Brownie de chocolate',
            preco=12,
            disponivel=True,
        )

        response = self.client.get('/pratos/', {
            'q': 'Hambúrguer',
            'categoria': 'PRINCIPAL',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hambúrguer Artesanal')
        self.assertNotContains(response, 'Brownie')
