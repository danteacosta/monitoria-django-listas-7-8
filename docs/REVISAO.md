# Registro de validação

Data: 19/11/2026. Escopo: exemplo didático local das listas 7 e 8 com cadastro por formulário.

| Verificação | Resultado |
|---|---|
| Plano e questões das listas | Implementados e documentados |
| Casos de uso | Listagem, detalhes, filtro e cadastro testados |
| Casos vazios e inválidos | Mensagens, validação e 404 cobertos |
| Filosofia dos testes | Django real, sem mocks da aplicação; jornada com servidor real |
| Organização | MVT padrão; sem camadas extras |
| Legibilidade | Nomes em português e funções pequenas |
| Segurança | ModelForm com campos explícitos, ORM, escape e CSRF; auditoria sem vulnerabilidades conhecidas |

Os sete pontos foram revisados por agentes em tarefas separadas. As sugestões úteis foram incorporadas: descrição opcional, categoria vazia/inexistente também pela rota de nome e destino exato após o cadastro.

Comentários didáticos foram mantidos porque fazem parte do pedido da monitoria. Os arquivos gerados pelo Django mantêm suas indicações de configuração local. Não há pacote versionado nem mecanismo de release; não cabe criar uma release para esta primeira publicação do material.

A conferência de documentação verificou caminhos, nomes das rotas, comandos e a troca de Gist por repositório. As limitações de execução estão em [verificação](verificacao.md). Não há verificação estática de tipos configurada.
