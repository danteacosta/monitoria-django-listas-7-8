# Lista 8: continuar o mesmo catálogo

Agora vamos fazer os endereços levarem informações para a view. Ao abrir um livro, o endereço informa seu ID. Ao escolher uma categoria, informa qual categoria queremos ver. Também vamos reaproveitar a estrutura HTML com `base.html`.

## Questão 1: acompanhar o pedido do navegador

O enunciado usa `/produtos/42/`. No nosso projeto, o exemplo equivalente é `/livros/42/`.

**a)** `urls.py` procura uma rota que combine com esse caminho. A rota `livros/<int:pk>/` reconhece o número 42 e chama a view com `pk=42`.

**b)** A função recebe obrigatoriamente `request`, que representa o pedido do navegador. Nesta rota também recebe `pk`. Ela deve devolver uma resposta HTTP. Aqui usamos `render`, que devolve uma página HTML pronta.

**c)** Usamos `get_object_or_404(Livro, pk=pk)`. Se o livro existir, a função o devolve. Se não existir, o Django responde com o erro **404: página não encontrada**. Não devolvemos uma página de sucesso com um livro inexistente.

Com `DEBUG=True`, o Django mostra uma página de 404 com informações para quem está programando. Não é a aparência que um site publicado deve usar.

## Questão 2: criar rotas com parâmetros

Veja o arquivo completo em [catalogo/urls.py](../catalogo/urls.py). As três rotas pedidas na questão são estas:

```python
from django.urls import path
from . import views

app_name = "catalogo"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("livros/<int:pk>/", views.detalhe_livro, name="detalhe"),
    path("categorias/<slug:slug>/", views.listar_categoria, name="categoria"),
]
```

O arquivo do projeto inclui ainda a listagem, o cadastro e uma rota com `str` para a questão 6. Se você copiar apenas as três rotas acima para o projeto pronto, os links das demais páginas deixarão de funcionar. Para executar o exemplo completo, mantenha o arquivo do repositório.

`<int:pk>` aceita um número inteiro. `<slug:slug>` aceita um texto com letras sem acento, números, hífen e sublinhado, como `ficcao-cientifica`. O que vem depois de `:` é o nome do argumento que a view vai receber.

`app_name` cria um namespace: uma identificação para as rotas desse aplicativo. Por isso escrevemos `catalogo:home` e `catalogo:detalhe` nos links. Isso evita confundir rotas de aplicativos diferentes que tenham o mesmo nome.

## Questão 3: criar a view de detalhes

Em [catalogo/views.py](../catalogo/views.py):

```python
from django.shortcuts import get_object_or_404, render
from .models import Livro


def detalhe_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    contexto = {"livro": livro}
    return render(request, "catalogo/detalhe.html", contexto)
```

Se a URL trouxer o número 1, procuramos o livro de ID 1. `pk` significa chave primária: o identificador do registro. O Django cria esse identificador automaticamente.

O contexto permite usar `{{ livro.nome }}` e `{{ livro.autor }}` no template. Os nomes do dicionário e do HTML precisam combinar.

## Questão 4: usar herança de templates

Abra [base.html](../catalogo/templates/base.html). Ele tem `<!DOCTYPE html>`, `<html>`, `<head>` e `<body>`, além do cabeçalho e dos links que aparecem em todas as páginas.

O trecho abaixo reserva um espaço para o conteúdo de cada página:

```django
<main>
    {% block content %}{% endblock %}
</main>
```

Agora veja [detalhe.html](../catalogo/templates/catalogo/detalhe.html):

```django
{% extends 'base.html' %}

{% block content %}
<h1>{{ livro.nome }}</h1>
<p>Autor: {{ livro.autor }}</p>
{% endblock %}
```

`extends` diz “use a estrutura de base.html”. O bloco preenche o espaço reservado. O arquivo de detalhes não precisa repetir `<html>` nem `<body>`. Se mudarmos o menu em `base.html`, a mudança aparece em todas as páginas que o usam.

Os trechos aqui destacam a ideia. Os arquivos vinculados têm o código completo, inclusive descrição, categoria e link de volta.

## Questão 5: mostrar uma lista com DTL

DTL é a linguagem de templates do Django. O trecho da questão está em [lista.html](../catalogo/templates/catalogo/lista.html):

```django
{% if lista_itens %}
<ul>
    {% for item in lista_itens %}
    <li>
        <a href="{% url 'catalogo:detalhe' item.pk %}">{{ item.nome|upper }}</a>
        <br>Autor: {{ item.autor }}
    </li>
    {% endfor %}
</ul>
{% else %}
<p>Nenhum livro cadastrado.</p>
{% endif %}
```

`if` verifica se há livros. `for` percorre a lista e cria um `<li>` para cada livro. `{{ item.nome }}` mostra o nome e `|upper` o apresenta em maiúsculas, sem alterar o que está salvo no banco.

A tag `url` monta o link usando o nome da rota e o ID. Se mudarmos o caminho da rota, não será preciso corrigir um endereço escrito à mão em cada template.

## Questão 6: filtrar pela categoria da URL

A questão 2 pede o conversor `slug`, mas esta questão pede explicitamente `str`. Para atender às duas, o projeto oferece duas rotas. A que esta questão pede é:

```python
path(
    "categorias-por-nome/<str:nome_categoria>/",
    views.listar_categoria_nome,
    name="categoria_nome",
)
```

`str` aceita um trecho de texto sem `/`, inclusive nomes com acentos e espaços. O navegador pode representar esses caracteres com códigos no endereço. Já o slug usa a versão curta, como `ficcao`.

A função, em [views.py](../catalogo/views.py), é:

```python
def listar_categoria_nome(request, nome_categoria):
    categoria = get_object_or_404(Categoria, nome__iexact=nome_categoria)
    livros = Livro.objects.filter(categoria=categoria).order_by("nome")
    contexto = {"categoria": categoria, "lista_itens": livros}
    return render(request, "catalogo/lista_categoria.html", contexto)
```

`nome__iexact` busca o nome completo sem diferenciar maiúsculas de minúsculas. `filter` seleciona apenas os livros daquela categoria. A versão por slug faz a mesma coisa, mas encontra a categoria pelo campo `slug`.

Abra [lista_categoria.html](../catalogo/templates/catalogo/lista_categoria.html). Ele herda `base.html` e usa `for` para mostrar os livros filtrados. O trecho `empty` mostra uma mensagem se a categoria existir, mas ainda não tiver livros. Se a própria categoria não existir, a resposta é 404.

Com os dados de exemplo carregados, abra e tire capturas de:

- [Ficção pelo nome](http://127.0.0.1:8000/categorias-por-nome/Fic%C3%A7%C3%A3o/): dois livros.
- [Ciência pelo nome](http://127.0.0.1:8000/categorias-por-nome/Ci%C3%AAncia/): Cosmos.
- [História pelo nome](http://127.0.0.1:8000/categorias-por-nome/Hist%C3%B3ria/): mensagem de categoria vazia.

Você pode trocar só o nome da categoria na barra de endereços para observar o resultado. Os links da aplicação usam `url`; esses endereços no guia são exemplos para digitar no navegador.

**Onde entra o CSRF?** A listagem faz apenas uma consulta por GET. O formulário que salva um livro por POST precisa de `{% csrf_token %}` dentro de `<form>`, como mostra [formulario.html](../catalogo/templates/catalogo/formulario.html).

CSRF protege contra pedidos forjados por outro site. Não criptografa os dados. A criptografia da conexão é responsabilidade do HTTPS.

## O que mostrar na entrega

Mostre `urls.py`, a view de detalhes, a relação entre `base.html` e `detalhe.html`, o laço de `lista.html` e as capturas do filtro por categoria. Os arquivos estão prontos para leitura e execução neste repositório; o grupo deve praticar a explicação do que acontece ao trocar um número ou um nome na URL.
