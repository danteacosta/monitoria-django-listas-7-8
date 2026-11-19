# Construa o catálogo em três etapas

Você abriu o projeto pronto e encontrou vários arquivos. Vamos construir uma versão menor primeiro e acrescentar as outras partes aos poucos. Ao final de cada etapa, pare e confira o resultado no navegador.

Use uma **pasta nova**, separada do repositório baixado. Deixe o repositório aberto em outra janela do editor para consultar os arquivos. Não copie todos os arquivos de uma vez: alguns têm links para páginas que só vamos criar depois.

## Etapa 1: lista 7, início e livros do banco

Ao terminar esta etapa, você conseguirá abrir o início e ver os livros cadastrados no Admin. Ainda não haverá página de detalhes nem formulário de cadastro.

### Prepare a pasta

No terminal, dentro da pasta nova, crie e ative o ambiente virtual seguindo as instruções do [README](../README.md#como-executar). Depois rode:

```bash
python -m pip install Django==5.2.19
django-admin startproject config .
python manage.py startapp catalogo
```

Em `config/settings.py`, acrescente `"catalogo"` à lista `INSTALLED_APPS`. No mesmo arquivo, troque `LANGUAGE_CODE` para `"pt-br"`. Mantenha as demais configurações geradas pelo Django.

Copie o conteúdo de [models.py](../catalogo/models.py) e [admin.py](../catalogo/admin.py) para os arquivos de mesmo nome no seu aplicativo. Leia a [questão 6 da lista 7](lista-7.md#questão-6-criar-o-model) para entender os campos. Vamos usar as mesmas classes nas três etapas.

Crie `catalogo/urls.py` com **somente** estas duas rotas:

```python
from django.urls import path
from . import views

app_name = "catalogo"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("livros/", views.listar_livros, name="listar"),
]
```

Em `config/urls.py`, use o conteúdo de [config/urls.py do exemplo](../config/urls.py). Ele encaminha as URLs para o aplicativo e mantém o acesso ao Admin.

### Crie as duas funções

Substitua o conteúdo de `catalogo/views.py` por:

```python
from django.shortcuts import render
from .models import Livro


def home_view(request):
    contexto = {
        "nome_projeto": "Estante da Turma",
        "descricao": "Um catálogo para conhecer os livros da turma.",
    }
    return render(request, "catalogo/inicio.html", contexto)


def listar_livros(request):
    livros = Livro.objects.all().order_by("nome")
    return render(request, "catalogo/lista.html", {"lista_itens": livros})
```

A primeira função envia dois textos para o HTML. A segunda busca os livros no banco e envia a lista. As duas devolvem uma página com `render`.

### Crie as páginas

Crie a pasta `catalogo/templates/catalogo/`. Dentro dela, crie `inicio.html`:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>{{ nome_projeto }}</title>
</head>
<body>
    <h1>{{ nome_projeto }}</h1>
    <p>{{ descricao }}</p>
    <a href="{% url 'catalogo:listar' %}">Ver livros</a>
    <a href="{% url 'admin:index' %}">Painel administrativo</a>
</body>
</html>
```

Crie também `lista.html` nessa mesma pasta:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Livros da turma</title>
</head>
<body>
    <h1>Livros da turma</h1>
    <ul>
        {% for item in lista_itens %}
        <li>{{ item.nome }}: {{ item.autor }}</li>
        {% empty %}
        <li>Nenhum livro cadastrado.</li>
        {% endfor %}
    </ul>
    <a href="{% url 'catalogo:home' %}">Voltar ao início</a>
</body>
</html>
```

### Pare e confira

Prepare o banco, crie seu usuário do Admin e inicie o servidor:

```bash
python manage.py makemigrations catalogo
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abra [o início](http://127.0.0.1:8000/) e clique em “Ver livros”. Primeiro deve aparecer a mensagem de lista vazia. Volte e abra o painel administrativo. Cadastre uma categoria e depois um livro. Para a categoria, use nome `Ficção` e slug `ficcao`. O slug será usado na próxima etapa.

Volte à lista e atualize a página. O livro deve aparecer com nome e autor.

**Antes de continuar, explique:** de onde vieram o nome e o autor mostrados no HTML? Qual função buscou esses dados? Complete também o planejamento e os diagramas do [guia da lista 7](lista-7.md).

## Etapa 2: lista 8, detalhes e categorias

Agora cada livro terá sua própria página. Também vamos reaproveitar o cabeçalho e mostrar só os livros da categoria escolhida.

### Acrescente as rotas e as views

Em `catalogo/views.py`, mantenha `home_view` e substitua `listar_livros` pela versão de [views.py do exemplo](../catalogo/views.py). Essa versão envia as categorias junto com os livros.

Na primeira importação, acrescente `get_object_or_404` ao lado de `render`. Na importação dos models, acrescente `Categoria` ao lado de `Livro`.

Do mesmo arquivo do exemplo, copie apenas estas três funções para o fim do seu `views.py`: `detalhe_livro`, `listar_categoria_nome` e `listar_categoria`. Deixe `cadastrar_livro`, o import de `LivroForm` e `redirect` para a etapa 3.

Substitua `catalogo/urls.py` por:

```python
from django.urls import path
from . import views

app_name = "catalogo"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("livros/", views.listar_livros, name="listar"),
    path("livros/<int:pk>/", views.detalhe_livro, name="detalhe"),
    path("categorias-por-nome/<str:nome_categoria>/",
         views.listar_categoria_nome, name="categoria_nome"),
    path("categorias/<slug:slug>/", views.listar_categoria, name="categoria"),
]
```

Comece pelo endereço com o nome: `/categorias-por-nome/Ficção/`. A view recebe `Ficção`, encontra a categoria e consulta seus livros. Depois experimente `/categorias/ficcao/`: o resultado é o mesmo, mas a busca usa o slug. O [guia da lista 8](lista-8.md#comece-pelo-nome-da-categoria) compara as duas formas.

### Reaproveite a estrutura do HTML

Crie `catalogo/templates/base.html`, um nível acima da pasta que contém `inicio.html`:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Estante da Turma{% endblock %}</title>
</head>
<body>
    <nav>
        <a href="{% url 'catalogo:home' %}">Início</a>
        <a href="{% url 'catalogo:listar' %}">Ver livros</a>
    </nav>
    {% block content %}{% endblock %}
</body>
</html>
```

Agora substitua `catalogo/templates/catalogo/inicio.html` por:

```django
{% extends 'base.html' %}

{% block content %}
<h1>{{ nome_projeto }}</h1>
<p>{{ descricao }}</p>
<a href="{% url 'catalogo:listar' %}">Conhecer os livros</a>
<a href="{% url 'admin:index' %}">Painel administrativo</a>
{% endblock %}
```

A estrutura que ficava repetida nas páginas passou para `base.html`. O conteúdo de cada página fica dentro de `block content`.

Copie [lista.html](../catalogo/templates/catalogo/lista.html) do exemplo para a pasta correspondente do seu projeto. Remova apenas o link “Cadastrar livro” do final, pois o cadastro será criado na etapa 3.

Por último, copie [detalhe.html](../catalogo/templates/catalogo/detalhe.html) e [lista_categoria.html](../catalogo/templates/catalogo/lista_categoria.html) para essa mesma pasta.

### Pare e confira

Com o servidor rodando, abra a lista e clique em um livro. O endereço deve terminar com um número, como `/livros/1/`. Troque esse número por um ID que não exista: a resposta deve ser 404.

No Admin, cadastre outra categoria e outro livro. Experimente os filtros pelo nome e pelo slug. Confira que o livro de uma categoria não aparece na outra. Os guias e as capturas da [lista 8](lista-8.md) ajudam a comparar o resultado.

**Antes de continuar, explique:** o que mudou quando você trocou o parâmetro da URL? Por que `detalhe.html` já não tem `<html>` nem `<body>`?

## Etapa 3: formulário, cadastrar sem abrir o Admin

Até agora, você usou o Admin para colocar os livros no banco. Nesta etapa, o aluno terá uma página própria para cadastrar um livro.

Leia o [exemplo do cadastro de Maria](formularios.md#acompanhe-o-cadastro-de-maria). Depois siga as seções 1 a 4 daquele guia para entender o formulário, a view, o HTML e a rota.

Para completar sua versão, copie os arquivos finais do exemplo: `catalogo/forms.py`, `catalogo/views.py` e `catalogo/urls.py`. Copie também `base.html` e os cinco templates da pasta `catalogo/templates/catalogo/`. Agora as rotas de cadastro existem e os links “Cadastrar livro” podem aparecer nas páginas.

Os models são os mesmos: acrescentar esse formulário não exige outra migração. Mantenha as migrações que você criou e o banco que usou nas etapas anteriores.

### Pare e confira

Abra o cadastro, escolha uma categoria, preencha nome e autor e salve. O navegador deve abrir os detalhes do novo livro. Confira também a listagem.

Tente enviar sem autor. O cadastro deve ser recusado. Depois deixe só a descrição vazia: deve funcionar, pois esse campo é opcional.

**Antes de terminar, explique:** em qual momento acontece GET? Em qual acontece POST? Por que só chamamos `save()` depois de `is_valid()`?

Quando conseguir explicar as três etapas, experimente os [exercícios curtos](exercicios.md). Para conhecer os testes, comece pelo [primeiro exemplo](testes.md), sem precisar ler a jornada com servidor real.
