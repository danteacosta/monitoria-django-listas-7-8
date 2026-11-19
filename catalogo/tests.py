import re

from django.test import Client, LiveServerTestCase, TestCase
from django.urls import reverse

from .models import Categoria, Livro


class CatalogoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ficcao = Categoria.objects.create(nome="Ficção", slug="ficcao")
        cls.ciencia = Categoria.objects.create(nome="Ciência", slug="ciencia")
        cls.vazia = Categoria.objects.create(nome="História", slug="historia")
        cls.livro = Livro.objects.create(
            nome="O pequeno príncipe",
            autor="Antoine de Saint-Exupéry",
            descricao="Uma viagem por pequenos planetas.",
            categoria=cls.ficcao,
        )
        Livro.objects.create(nome="Cosmos", autor="Carl Sagan", categoria=cls.ciencia)

    def test_inicio_oferece_lista_e_cadastro(self):
        resposta = self.client.get(reverse("catalogo:home"))
        self.assertContains(resposta, "Estante da Turma")
        self.assertContains(resposta, reverse("catalogo:listar"))
        self.assertContains(resposta, reverse("catalogo:cadastrar"))

    def test_lista_mostra_nome_em_maiusculas_autor_e_link(self):
        resposta = self.client.get(reverse("catalogo:listar"))
        self.assertContains(resposta, "O PEQUENO PRÍNCIPE")
        self.assertContains(resposta, self.livro.autor)
        self.assertContains(resposta, reverse("catalogo:detalhe", args=[self.livro.pk]))

    def test_lista_vazia_orienta_aluno(self):
        Livro.objects.all().delete()
        self.assertContains(
            self.client.get(reverse("catalogo:listar")), "Nenhum livro cadastrado."
        )

    def test_detalhe_exibe_dados_e_id_inexistente_retorna_404(self):
        resposta = self.client.get(reverse("catalogo:detalhe", args=[self.livro.pk]))
        self.assertContains(resposta, self.livro.descricao)
        self.assertContains(resposta, self.ficcao.nome)
        self.assertEqual(
            self.client.get(reverse("catalogo:detalhe", args=[9999])).status_code, 404
        )

    def test_categoria_por_slug_e_por_nome_filtra_livros(self):
        for rota, parametro in [
            ("categoria", "ficcao"),
            ("categoria_nome", "Ficção"),
            ("categoria_nome", "ficção"),
        ]:
            with self.subTest(rota=rota):
                resposta = self.client.get(
                    reverse("catalogo:" + rota, args=[parametro])
                )
                self.assertContains(resposta, self.livro.nome)
                self.assertNotContains(resposta, "Cosmos")

    def test_categoria_vazia_e_categoria_desconhecida(self):
        for rota, categoria in [
            ("categoria", "historia"),
            ("categoria_nome", "História"),
        ]:
            with self.subTest(rota=rota):
                resposta = self.client.get(
                    reverse("catalogo:" + rota, args=[categoria])
                )
                self.assertContains(resposta, "Nenhum livro nesta categoria.")
                resposta = self.client.get(
                    reverse("catalogo:" + rota, args=["nao-existe"])
                )
                self.assertEqual(resposta.status_code, 404)

    def test_formulario_get_nao_cadastra(self):
        quantidade = Livro.objects.count()
        resposta = self.client.get(reverse("catalogo:cadastrar"))
        self.assertContains(resposta, 'name="csrfmiddlewaretoken"')
        self.assertEqual(Livro.objects.count(), quantidade)

    def test_cadastro_valido_leva_ao_livro_e_aparece_na_lista(self):
        resposta = self.client.post(
            reverse("catalogo:cadastrar"),
            {
                "nome": "A ilha do tesouro",
                "autor": "Robert Louis Stevenson",
                "descricao": "Uma aventura no mar.",
                "categoria": self.ficcao.pk,
            },
            follow=True,
        )
        self.assertContains(resposta, "A ilha do tesouro")
        self.assertContains(resposta, "Uma aventura no mar.")
        self.assertContains(
            self.client.get(reverse("catalogo:listar")), "A ILHA DO TESOURO"
        )

    def test_cadastro_invalido_exibe_erros_e_preserva_dados(self):
        quantidade = Livro.objects.count()
        resposta = self.client.post(
            reverse("catalogo:cadastrar"),
            {
                "nome": "Livro incompleto",
                "autor": "",
                "categoria": self.ficcao.pk,
            },
        )
        self.assertContains(resposta, "Este campo é obrigatório.")
        self.assertContains(resposta, "Livro incompleto")
        self.assertEqual(Livro.objects.count(), quantidade)

    def test_categoria_invalida_nao_e_aceita(self):
        resposta = self.client.post(
            reverse("catalogo:cadastrar"),
            {
                "nome": "Teste",
                "autor": "Autor",
                "categoria": 9999,
            },
        )
        self.assertContains(resposta, "Faça uma escolha válida")

    def test_post_sem_csrf_e_recusado(self):
        cliente = Client(enforce_csrf_checks=True)
        resposta = cliente.post(
            reverse("catalogo:cadastrar"),
            {
                "nome": "Teste",
                "autor": "Autor",
                "categoria": self.ficcao.pk,
            },
        )
        self.assertEqual(resposta.status_code, 403)

    def test_conteudo_do_livro_nao_vira_html(self):
        self.livro.descricao = "<script>alert('oi')</script>"
        self.livro.save()
        resposta = self.client.get(reverse("catalogo:detalhe", args=[self.livro.pk]))
        self.assertContains(resposta, "&lt;script&gt;")
        self.assertNotContains(resposta, "<script>")


class JornadaAoVivoTests(LiveServerTestCase):
    def test_cadastrar_e_consultar_livro_com_servidor_real(self):
        from http.cookiejar import CookieJar
        from urllib.parse import urlencode
        from urllib.request import HTTPCookieProcessor, build_opener

        categoria = Categoria.objects.create(nome="Aventura", slug="aventura")
        navegador = build_opener(HTTPCookieProcessor(CookieJar()))
        inicio = navegador.open(self.live_server_url + reverse("catalogo:home"))
        self.assertIn("Estante da Turma", inicio.read().decode())
        formulario = navegador.open(
            self.live_server_url + reverse("catalogo:cadastrar")
        )
        token = re.search(
            r'name="csrfmiddlewaretoken" value="([^"]+)"', formulario.read().decode()
        ).group(1)
        dados = urlencode(
            {
                "nome": "Livro da jornada",
                "autor": "Autor da turma",
                "categoria": categoria.pk,
                "csrfmiddlewaretoken": token,
            }
        ).encode()
        resposta = navegador.open(
            self.live_server_url + reverse("catalogo:cadastrar"), dados
        )
        self.assertIn("Livro da jornada", resposta.read().decode())
        livro = Livro.objects.get(nome="Livro da jornada")
        self.assertEqual(
            resposta.url,
            self.live_server_url + reverse("catalogo:detalhe", args=[livro.pk]),
        )
        self.assertEqual(Livro.objects.count(), 1)
        self.assertIn(
            "Sem descrição por enquanto.", navegador.open(resposta.url).read().decode()
        )
        lista = navegador.open(self.live_server_url + reverse("catalogo:listar"))
        self.assertIn("LIVRO DA JORNADA", lista.read().decode())
        filtrada = navegador.open(
            self.live_server_url + reverse("catalogo:categoria", args=["aventura"])
        )
        self.assertIn("Livro da jornada", filtrada.read().decode())
