# Estante da Turma

Vamos montar um catálogo de livros com Django. Você poderá ver os livros, abrir os detalhes de um deles, escolher uma categoria e cadastrar um novo livro pelo formulário.

Este é um exemplo para a monitoria de POO do ensino médio. A lista 7 começa o projeto; a lista 8 continua esse mesmo projeto. O formulário é um complemento para praticar `forms.py`, GET, POST e validação.

## Como executar

Você precisa do Python 3.10 ou mais recente e de um terminal. No Windows, se `python` não funcionar, tente `py`. No macOS/Linux, pode ser necessário usar `python3`.

Baixe o ZIP pelo botão **Code → Download ZIP**, extraia e abra o terminal dentro da pasta do projeto. Ou use Git:

```bash
git clone https://github.com/danteacosta/monitoria-django-listas-7-8.git
cd monitoria-django-listas-7-8
```

Crie um ambiente virtual. Ele guarda as bibliotecas deste projeto separadas das de outros projetos:

```bash
python -m venv .venv
```

Ative o ambiente conforme seu sistema:

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (Prompt de Comando)
.venv\Scripts\activate.bat

# macOS ou Linux
source .venv/bin/activate
```

Se o PowerShell bloquear a ativação, você pode usar o Prompt de Comando com a opção acima. Não é necessário mudar as configurações do computador.

Com o ambiente ativo, instale o Django e prepare o banco:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata exemplo
python manage.py runserver
```

Abra [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Para parar o servidor, use `Ctrl+C` no terminal.

O comando `loaddata exemplo` coloca alguns livros e categorias no banco para você testar. Rode uma vez no começo: repetir esse comando recoloca os valores dos registros de exemplo.

## Por onde estudar

Comece pelo [roteiro em três etapas](docs/passo-a-passo.md). Ele mostra como reconstruir o catálogo em uma pasta nova e o que conferir antes de avançar:

| Etapa | O que você vai fazer | Como saber que funcionou |
|---|---|---|
| 1: lista 7 | Início, models, Admin e listagem | Um livro cadastrado no Admin aparece na lista |
| 2: lista 8 | Detalhes, categorias e herança de templates | Trocar o ID ou a categoria muda a página |
| 3: formulário | Cadastro com GET, POST e validação | O livro enviado aparece nos detalhes e na lista |

Para consultar as respostas por questão:

1. [Lista 7: planejar e montar o projeto](docs/lista-7.md).
2. [Lista 8: continuar com rotas e templates](docs/lista-8.md).
3. [Formulários: cadastrar um livro passo a passo](docs/formularios.md).

O código deste repositório já reúne as três etapas. Se você baixou o projeto pronto, pode executá-lo pelo README e acompanhar as funções na ordem do roteiro. Depois pratique com os [exercícios curtos](docs/exercicios.md).

## O que tem em cada arquivo

```text
manage.py                         Comandos para cuidar do projeto
config/settings.py                Configurações, como idioma e banco
config/urls.py                    Encaminha as URLs para o aplicativo
catalogo/models.py                Categoria e Livro
catalogo/admin.py                 Cadastro dos models no painel
catalogo/urls.py                   Endereços das páginas
catalogo/views.py                  Funções que atendem cada página
catalogo/forms.py                  Formulário de cadastro
catalogo/templates/base.html       Estrutura comum das páginas
catalogo/templates/catalogo/       Conteúdo de cada página
catalogo/migrations/               Histórico da estrutura do banco
catalogo/fixtures/exemplo.json     Dados para experimentar
catalogo/tests.py                  Testes automáticos do exemplo
```

## Abrir o painel administrativo

Pare o servidor e crie seu próprio usuário administrador:

```bash
python manage.py createsuperuser
python manage.py runserver
```

Entre em [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/). Use o usuário e a senha que acabou de criar. Ao digitar a senha no terminal, os caracteres não aparecem, mas estão sendo recebidos.

Você verá **Categorias** e **Livros**. Para uma nova categoria, preencha nome e slug. Exemplo: nome `Ficção científica`, slug `ficcao-cientifica`.

## Conferir se está funcionando

```bash
python manage.py test
python manage.py check
```

O primeiro comando executa os testes. O segundo procura problemas de configuração. Para entender um teste pequeno antes de ler o arquivo inteiro, siga o [guia de testes para começar](docs/testes.md). Veja também o [roteiro para testar no navegador](docs/verificacao.md).

Este exemplo usa SQLite e o servidor local do Django. O cadastro de livros está aberto para facilitar a aula. Não há login para cadastrar, editar ou excluir pela aplicação. O projeto não tem edição nem exclusão fora do Admin. Antes de colocar o site na internet, será necessário tratar permissões e configurações de produção. O Gist ou o GitHub guardam os arquivos; não executam o servidor Django.

Os nomes dos integrantes, as contribuições reais e a apresentação devem ser preparados pelo grupo. Use o exemplo para entender o fluxo e adaptar o seu projeto.
