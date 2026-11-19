# Como conferir o exemplo

Siga o README para instalar e abrir o projeto. Este roteiro ajuda você a conferir o resultado antes de explicar o código.

## No navegador

1. Abra o início e siga o link “Conhecer os livros”. Confira os nomes e autores.
2. Abra um livro e volte à listagem pelo link.
3. Escolha Ficção, Ciência e História. Confira que os livros mudam e que História está vazia.
4. Digite `/livros/999999/` depois do endereço do servidor. A resposta deve ser 404.
5. Abra o cadastro e salve um livro. Ele deve aparecer nos detalhes e na lista.
6. Cadastre outro sem descrição: esse campo é opcional.
7. Tente deixar o nome ou o autor vazio. O cadastro não deve ser aceito.

## Capturas da execução no Safari

As capturas foram feitas em 19/11/2026. Usamos a porta 8767 para não ocupar a porta de outro projeto. No seu computador, o comando do README usa a porta 8000. O funcionamento é o mesmo.

- [Página inicial](imagens/01-inicio.png).
- [Formulário preenchido](imagens/02-formulario.png).
- [Detalhes do livro cadastrado pelo formulário](imagens/03-detalhe.png).

As três capturas abaixo mostram o filtro da questão 6 da lista 8:

| URL depois do endereço do servidor | Resultado |
|---|---|
| `/categorias-por-nome/Ficção/` | [Livros de Ficção](imagens/04-ficcao.png) |
| `/categorias-por-nome/Ciência/` | [Livros de Ciência](imagens/05-ciencia.png) |
| `/categorias-por-nome/História/` | [Categoria sem livros](imagens/06-historia.png) |

Na demonstração, cadastramos “Dom Casmurro” pelo formulário. Por isso a captura de Ficção tem um livro a mais do que os dados iniciais de exemplo. Esse livro existe apenas no banco local usado para a demonstração.

## Testes automáticos

Execute `python manage.py test`. Há testes das páginas, dos dados enviados e uma jornada que inicia um servidor temporário, envia o formulário com CSRF e consulta o livro salvo.

A verificação da sessão passou por 13 testes, `manage.py check`, conferência das migrações, lint com Ruff, compilação Python e auditoria das dependências. Não há ferramenta de análise estática de tipos configurada neste exemplo.

A jornada de cadastro e os filtros foram conferidos no Safari com banco real. A instalação não foi executada em Windows/Linux nem em celular físico. Não houve publicação do servidor na internet.
