from django.urls import path
from . import views


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('pratos/', views.lista_pratos, name='lista_pratos'),
    path('pratos/novo/', views.criar_prato, name='criar_prato'),
    path('pratos/<int:prato_id>/editar/', views.editar_prato, name='editar_prato'),
    path('pratos/<int:prato_id>/excluir/', views.excluir_prato, name='excluir_prato'),
    path('combos/', views.lista_combos, name='lista_combos'),
    path('mesas/', views.lista_mesas, name='lista_mesas'),
    path('mesa/<int:mesa_id>/comanda/', views.abrir_comanda, name='abrir_comanda'),
    path('comanda/<int:comanda_id>/adicionar-prato/<int:prato_id>/', views.adicionar_prato, name='adicionar_prato'),
    path('comanda/<int:comanda_id>/adicionar-combo/<int:combo_id>/', views.adicionar_combo, name='adicionar_combo'),
    path('comanda/<int:comanda_id>/fechar/', views.fechar_comanda, name='fechar_comanda'),
    path('item/<int:item_id>/remover/', views.remover_item, name='remover_item'),
]
