from tempfile import TemporaryDirectory

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from .models import Arquivo


class UploadTests(TestCase):
    def setUp(self):
        # Os testes não deixam arquivos no volume usado pela aplicação.
        pasta = TemporaryDirectory()
        self.addCleanup(pasta.cleanup)
        configuracao = override_settings(MEDIA_ROOT=pasta.name)
        configuracao.enable()
        self.addCleanup(configuracao.disable)

    def test_upload_salva_conteudo_e_aparece_na_lista(self):
        resposta = self.client.post(
            "/", {"arquivo": SimpleUploadedFile("aula.txt", b"Ola, Docker!")}
        )
        self.assertRedirects(resposta, "/")
        arquivo = Arquivo.objects.get()
        self.assertEqual(arquivo.nome, "aula.txt")
        with arquivo.arquivo.open("rb") as conteudo:
            self.assertEqual(conteudo.read(), b"Ola, Docker!")
        self.assertContains(self.client.get("/"), arquivo.arquivo.url)

    def test_arquivos_com_mesmo_nome_nao_sao_sobrescritos(self):
        for conteudo in [b"primeiro", b"segundo"]:
            self.client.post(
                "/", {"arquivo": SimpleUploadedFile("aula.txt", conteudo)}
            )
        arquivos = list(Arquivo.objects.order_by("id"))
        self.assertEqual(len(arquivos), 2)
        self.assertNotEqual(arquivos[0].arquivo.name, arquivos[1].arquivo.name)
        for arquivo, esperado in zip(arquivos, [b"primeiro", b"segundo"]):
            with arquivo.arquivo.open("rb") as conteudo:
                self.assertEqual(conteudo.read(), esperado)

    def test_upload_sem_arquivo_e_rejeitado(self):
        resposta = self.client.post("/", {})
        self.assertContains(resposta, "Este campo é obrigatório.")
        self.assertEqual(Arquivo.objects.count(), 0)

    def test_arquivo_acima_de_10_mb_e_rejeitado(self):
        arquivo = SimpleUploadedFile("grande.txt", b"x" * (10 * 1024 * 1024 + 1))
        resposta = self.client.post("/", {"arquivo": arquivo})
        self.assertContains(resposta, "O arquivo deve ter no máximo 10 MB.")
        self.assertEqual(Arquivo.objects.count(), 0)
