# Plano do exemplo da monitoria

## Scope
Catálogo de livros para ensino médio. Lista 7 estabelece o projeto; Lista 8 continua o mesmo projeto; complemento usa ModelForm para cadastrar livro. Explicações em português simples, sem camadas adicionais.

## Codebase Findings
Não há projeto existente indicado pelo usuário. O projeto começa do zero. Exemplos locais anteriores tinham recursos além do necessário. Não havia índice CCE para este novo projeto.

## Acceptance Tests
1. Ao abrir início e lista, o aluno navega pelos links e vê livros com nome e autor; sem livros, recebe mensagem clara.
2. Ao acessar um livro por ID, vê seus dados; um ID inexistente retorna 404.
3. Ao escolher categoria, vê apenas seus livros. A rota slug e a rota str funcionam; categoria conhecida vazia mostra mensagem; desconhecida retorna 404.
4. Ao enviar cadastro válido, vai para detalhes do livro salvo; ao enviar dados inválidos, vê erros e mantém o que digitou. GET não grava e POST sem CSRF é recusado.
5. No Safari, percorre início → cadastro → detalhe → lista → categoria com servidor e banco reais; o guia cobre todas as questões e diferencia planejamento de contribuições reais do grupo.

## Implementation Plan
1. Criar estrutura padrão Django com tests.py antes da implementação.
2. Confirmar falha dos testes pelos comportamentos ausentes.
3. Implementar models, URLs, FBVs, templates com herança e forms.py.
4. Gerar migrações e dados fictícios de demonstração.
5. Escrever guia por questão com diagramas simples e comandos de execução.
6. Testar no Safari, revisar código e publicar o código e os guias em repositório GitHub.

## Structural Decisions
Sem padrão adicional. MVT padrão Django, ModelForm e ORM bastam. SQLite e servidor local.

## Risks / Open Questions
Sem autenticação no cadastro, conforme escopo didático local. Não é configuração de produção. Não inventar integrantes ou participação. Screenshots de teste local serão guardados separadamente; os grupos devem capturar sua própria execução.

## Melhoria da sequência de ensino

Pedido de 19/11/2026: apresentar a construção em três etapas, acompanhar um cadastro concreto, acrescentar exercícios curtos e separar testes introdutórios da jornada opcional. Roteiro em `docs/passo-a-passo.md`, com paradas para verificar cada etapa; guias por questão preservados. Os arquivos da aplicação permanecem a versão final para consulta.

Verificação: reconstruir as etapas 1 e 2 em pasta temporária a partir dos trechos e instruções, consultar suas páginas pelo cliente Django e conferir os comandos dos testes introdutórios na etapa final. Revisar os links dos guias antes de publicar.
