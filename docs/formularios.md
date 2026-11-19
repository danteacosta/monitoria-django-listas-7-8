# Formulários: cadastrar um livro

Até aqui conseguimos ver livros que já estão no banco. Agora queremos digitar nome e autor em uma página e salvar um livro sem abrir o Admin. Esse complemento usa o mesmo catálogo das listas 7 e 8.

## Antes de começar

Carregue os dados de exemplo ou cadastre uma categoria no Admin. Todo livro precisa ter uma categoria. Neste exemplo, o formulário cadastra livros; as categorias continuam sendo cadastradas pelo Admin para manter a aula pequena.

## 1. Criar forms.py

Abra [catalogo/forms.py](../catalogo/forms.py):

```python
from django import forms
from .models import Livro


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ["nome", "autor", "descricao", "categoria"]
```

Um formulário reúne os campos que a pessoa vai preencher e verifica se os dados podem ser usados. `ModelForm` aproveita os campos que já definimos no model. Assim não precisamos escrever outra vez o tamanho máximo do nome e do autor.

A classe `Meta` guarda as configurações: qual model usar e quais campos mostrar. Aqui usamos apenas esses quatro campos. O ID é criado pelo Django e não é digitado pelo aluno.

Como a descrição tem `blank=True` no model, ela é opcional. Nome, autor e categoria são obrigatórios. A categoria aparece como uma lista de opções do banco.

## 2. Entender GET e POST na view

Abra a função `cadastrar_livro` em [catalogo/views.py](../catalogo/views.py). Ela usa estes imports:

```python
from django.shortcuts import redirect, render
from .forms import LivroForm
```

A função completa é:

```python
def cadastrar_livro(request):
    if request.method == "POST":
        form = LivroForm(request.POST)
        if form.is_valid():
            livro = form.save()
            return redirect("catalogo:detalhe", pk=livro.pk)
    else:
        form = LivroForm()
    return render(request, "catalogo/formulario.html", {"form": form})
```

Quando você abre a página, o navegador faz um **GET**. A view cria `LivroForm()` sem dados e mostra o formulário vazio. Abrir essa página não cadastra um livro.

Quando você clica em “Salvar livro”, o navegador faz um **POST**. `request.POST` traz os campos enviados, e `LivroForm(request.POST)` monta um formulário com esses dados.

`is_valid()` verifica os dados no servidor. Se estiver tudo certo, `save()` grava o livro. Depois, `redirect` manda o navegador abrir os detalhes do livro criado. Redirecionamos após salvar para que atualizar a página de detalhes não envie o mesmo cadastro outra vez.

Se houver erro, não entramos no bloco de `save()`. A última linha mostra o mesmo formulário com os dados digitados e os erros. Assim o aluno pode corrigir apenas o que faltou.

## 3. Mostrar o formulário no HTML

Abra [catalogo/templates/catalogo/formulario.html](../catalogo/templates/catalogo/formulario.html). O trecho principal é:

```django
<form method="post" action="{% url 'catalogo:cadastrar' %}">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Salvar livro</button>
</form>
```

`method="post"` escolhe como enviar os dados. `action` aponta para a rota que recebe o cadastro. `form.as_p` mostra os campos com seus rótulos e os erros de validação. Não precisamos escrever cada `<input>` manualmente neste primeiro exemplo.

`csrf_token` gera um campo escondido que o Django confere quando recebe o POST. Esse campo ajuda a impedir que outro site envie um pedido usando o navegador de alguém sem autorização. Não desative essa proteção para fazer o formulário funcionar.

CSRF não criptografa a conexão. Em um site publicado, HTTPS é o que protege os dados durante o transporte.

## 4. Conferir a rota

Em [catalogo/urls.py](../catalogo/urls.py), temos:

```python
path("livros/novo/", views.cadastrar_livro, name="cadastrar")
```

Esse é o endereço ligado à função que acabamos de ler. O menu leva até ele com `{% url 'catalogo:cadastrar' %}`.

O caminho de um cadastro fica assim:

```text
GET: abrir cadastro → view cria formulário vazio → HTML
POST: clicar em salvar → view recebe dados → valida → salva → abre detalhes
```

## 5. Experimentar

Abra “Cadastrar livro”, preencha os campos e salve. Confira o livro nos detalhes e na lista. Volte ao cadastro e tente deixar o autor vazio. O navegador pode avisar antes de enviar; o Django também valida no servidor, como os testes automáticos demonstram.

Experimente deixar só a descrição vazia: o cadastro deve funcionar. Atualize a página de detalhes depois de salvar e confira que isso não cria outro livro.

## Um primeiro contato com testes

Em [catalogo/tests.py](../catalogo/tests.py), há exemplos que fazem pedidos às páginas e conferem as respostas. Para rodar:

```bash
python manage.py test
```

O Django cria um banco temporário para os testes e o remove ao terminar. Seus livros do banco local não são apagados. Os testes verificam cadastro válido, campos obrigatórios, categoria inexistente, listagem e o erro 404. Há também um teste que envia POST sem token e espera 403, que significa pedido recusado.

Este é um formulário de estudo local. Ele não identifica quem cadastrou cada livro. Se o catálogo for publicado, o grupo precisará decidir quem pode cadastrar e proteger esse acesso.

Para consultar depois da aula: [referências oficiais usadas no exemplo](research/2026-11-19-django.md).
