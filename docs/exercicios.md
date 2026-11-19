# Exercícios curtos

Faça um exercício por vez. Antes de mudar o código, escreva o que você espera ver no navegador. Depois confira se aconteceu o que você previu.

## 1. Dê um nome ao catálogo

Troque “Estante da Turma” por um nome escolhido pelo seu grupo. Comece pelo valor de `nome_projeto`, dentro de `home_view`, em [views.py](../catalogo/views.py), e abra o início.

Observe que o nome também aparece no cabeçalho de [base.html](../catalogo/templates/base.html). Altere esse texto e o título padrão para combinar com o novo nome.

**Confira:** o início mostra o novo nome? O cabeçalho continua com ele quando você abre a lista e os detalhes?

**Explique:** qual texto veio da view e qual estava escrito diretamente no template?

## 2. Crie outra categoria

Entre no Admin e cadastre a categoria “Aventura”, com slug `aventura`. Depois cadastre um livro nessa categoria.

Abra a listagem e escolha Aventura. Experimente também digitar `/categorias-por-nome/Aventura/` depois do endereço do servidor.

**Confira:** o livro aparece em Aventura? Ele continua fora da categoria Ciência? As duas formas de abrir a categoria mostram o mesmo livro?

**Explique:** por que foi possível acrescentar uma categoria sem criar outra função em `views.py`?

## 3. Acrescente uma informação ao livro

Agora queremos guardar a editora. Em [models.py](../catalogo/models.py), acrescente este campo à classe `Livro`, junto dos outros campos:

```python
editora = models.CharField(max_length=100, blank=True)
```

O campo é opcional, assim os livros já cadastrados continuam válidos. No terminal, com o ambiente ativo, rode:

```bash
python manage.py makemigrations catalogo
python manage.py migrate
```

Em [forms.py](../catalogo/forms.py), acrescente `"editora"` à lista `fields`. Isso permite preencher a informação no formulário. Em [detalhe.html](../catalogo/templates/catalogo/detalhe.html), dentro de `block content`, acrescente:

```django
<p>Editora: {{ livro.editora|default:"Não informada" }}</p>
```

**Confira:** cadastre um livro com editora e abra seus detalhes. Depois abra um livro antigo, sem editora: deve aparecer “Não informada”.

**Explique:** por que mudar apenas o HTML não seria suficiente para guardar essa informação?

## Conte ao colega

Escolha um exercício e mostre a outro integrante o que você mudou. Peça que ele acompanhe o dado desde o model até a página. Se não conseguir explicar algum trecho, volte ao [roteiro](passo-a-passo.md) e localize a etapa correspondente.
