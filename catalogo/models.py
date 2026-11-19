from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=80, unique=True)
    # O slug é uma versão curta para a URL: "Ficção" vira "ficcao".
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nome


class Livro(models.Model):
    nome = models.CharField(max_length=150)
    autor = models.CharField(max_length=100)
    descricao = models.TextField("descrição", blank=True)
    # PROTECT impede apagar uma categoria que ainda tem livros.
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome
