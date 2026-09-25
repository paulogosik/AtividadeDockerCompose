from django.db import models


class Arquivo(models.Model):
    nome = models.CharField(max_length=255)
    # O banco guarda o caminho; o conteúdo do arquivo fica em MEDIA_ROOT.
    arquivo = models.FileField(upload_to="uploads/", max_length=300)
    enviado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-enviado_em"]

    def __str__(self):
        return self.nome
