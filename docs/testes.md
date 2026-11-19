# Seu primeiro teste com Django

Você já abriu o catálogo e conferiu o resultado no navegador. Um teste automático faz uma conferência por você: executa uma ação e compara o resultado com o que esperávamos.

Comece com uma página. Você não precisa entender todos os testes do projeto para acompanhar este exemplo.

## 1. Conferir o início

Abra [catalogo/tests.py](../catalogo/tests.py) e procure `test_inicio_oferece_lista_e_cadastro`. O trecho abaixo destaca a primeira conferência desse teste:

```python
resposta = self.client.get(reverse("catalogo:home"))
self.assertContains(resposta, "Estante da Turma")
```

A primeira linha pede a página inicial. `reverse` encontra o endereço pelo nome da rota. `self.client` é um recurso de teste do Django: ele faz o pedido à aplicação sem você precisar clicar no navegador.

A segunda linha confere se a resposta foi bem-sucedida e contém “Estante da Turma”. Se o texto não aparecer, o teste falha e mostra onde a conferência deu errado.

Para rodar só esse teste, use o terminal com o ambiente virtual ativo:

```bash
python manage.py test catalogo.tests.CatalogoTests.test_inicio_oferece_lista_e_cadastro
```

Esse comando já encontra o teste dentro da classe `CatalogoTests`. As duas linhas acima são um trecho para ler; não substitua o arquivo inteiro por elas.

## 2. Conferir um cadastro

Depois, procure `test_cadastro_valido_leva_ao_livro_e_aparece_na_lista`. Esse teste envia nome, autor, descrição e categoria por POST. Em seguida, confere se o livro aparece na resposta e na listagem.

É a mesma ideia do [cadastro de Maria](formularios.md#acompanhe-o-cadastro-de-maria): enviar os dados e verificar o que a pessoa verá depois. A preparação no começo da classe cria categorias e livros para os testes usarem. Assim eles não dependem do que você cadastrou no seu banco local.

Rode só esse teste:

```bash
python manage.py test catalogo.tests.CatalogoTests.test_cadastro_valido_leva_ao_livro_e_aparece_na_lista
```

Agora leia `test_cadastro_invalido_exibe_erros_e_preserva_dados`. Ele deixa o autor vazio e espera uma mensagem de erro. Testar também o erro ajuda a conferir que dados incompletos não são aceitos.

## 3. Rodar os testes juntos

```bash
python manage.py test
```

O Django cria um banco temporário para os testes e o remove ao terminar. Os livros do seu banco local não são apagados.

Se você fizer o exercício de mudar o nome do projeto, atualize também o texto esperado no teste. Primeiro decida qual deve ser o novo resultado; depois ajuste a conferência para esse resultado.

## Leitura opcional: uma jornada com servidor real

A classe `JornadaAoVivoTests`, no fim de `tests.py`, inicia um servidor temporário e envia pedidos HTTP reais. Ela guarda o cookie, lê o token CSRF da página, envia o cadastro e consulta o livro salvo.

Esse teste ajuda quem mantém o exemplo a conferir as partes funcionando juntas. Deixe essa leitura para depois que estiver confortável com GET, POST e os testes pequenos acima. Não é necessário copiar essa classe para resolver as listas 7 e 8.
