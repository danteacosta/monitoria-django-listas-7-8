from django.urls import path

from . import views

app_name = "catalogo"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("livros/", views.listar_livros, name="listar"),
    path("livros/novo/", views.cadastrar_livro, name="cadastrar"),
    path("livros/<int:pk>/", views.detalhe_livro, name="detalhe"),
    path("categorias/<slug:slug>/", views.listar_categoria, name="categoria"),
    # A questão 6 pede str; a questão 2 pede slug. Mantemos as duas.
    path(
        "categorias-por-nome/<str:nome_categoria>/",
        views.listar_categoria_nome,
        name="categoria_nome",
    ),
]
