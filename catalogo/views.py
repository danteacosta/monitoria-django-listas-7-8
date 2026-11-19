from django.shortcuts import get_object_or_404, redirect, render

from .forms import LivroForm
from .models import Categoria, Livro


def home_view(request):
    contexto = {
        "nome_projeto": "Estante da Turma",
        "descricao": "Um catálogo para conhecer os livros da turma.",
    }
    return render(request, "catalogo/inicio.html", contexto)


def listar_livros(request):
    contexto = {
        "lista_itens": Livro.objects.all().order_by("nome"),
        "categorias": Categoria.objects.all().order_by("nome"),
    }
    return render(request, "catalogo/lista.html", contexto)


def detalhe_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    contexto = {"livro": livro}
    return render(request, "catalogo/detalhe.html", contexto)


def listar_categoria(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    livros = Livro.objects.filter(categoria=categoria).order_by("nome")
    contexto = {"categoria": categoria, "lista_itens": livros}
    return render(request, "catalogo/lista_categoria.html", contexto)


def listar_categoria_nome(request, nome_categoria):
    categoria = get_object_or_404(Categoria, nome__iexact=nome_categoria)
    livros = Livro.objects.filter(categoria=categoria).order_by("nome")
    contexto = {"categoria": categoria, "lista_itens": livros}
    return render(request, "catalogo/lista_categoria.html", contexto)


def cadastrar_livro(request):
    if request.method == "POST":
        form = LivroForm(request.POST)
        if form.is_valid():
            livro = form.save()
            # Redirecionar após salvar evita repetir o POST ao atualizar a página.
            return redirect("catalogo:detalhe", pk=livro.pk)
    else:
        form = LivroForm()
    # Se o POST for inválido, o mesmo form volta com os erros e os dados digitados.
    return render(request, "catalogo/formulario.html", {"form": form})
