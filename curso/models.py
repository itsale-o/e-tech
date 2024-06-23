from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# criar cursos 
class Curso(models.Model):
    titulo = models.CharField(max_length=100)
    
    def __str__(self):
        return self.titulo

# criar as playlists
class Playlist(models.Model):
    curso = models.ForeignKey("Curso", related_name="playlists", on_delete=models.CASCADE)
    nome = models.CharField(max_length=500)
    canal = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse('curso:playlist', args=[self.pk])

    def __str__(self):
        return f"{self.pk}. {self.nome} - {self.canal} ({self.curso})"

# criar os vídeos
class Video(models.Model):
    playlist = models.ForeignKey("Playlist", related_name="videos", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=500)
    link = models.URLField()
    
    def __str__(self):
        return f"{self.titulo} - {self.playlist.canal}"


# criar os usuários
class Usuario(AbstractUser): 
    playlists_acessadas = models.ManyToManyField("Playlist")


class PostForum(models.Model):
    curso = models.ForeignKey("Curso", related_name="post", on_delete=models.CASCADE)
    autor = models.ForeignKey("Usuario", null=False, blank=False, related_name="usuario_post", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    conteudo = models.TextField()
    data_postagem = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.curso}"

class ComentariosPost(models.Model):
    post = models.ForeignKey("PostForum", related_name="comentarios", on_delete=models.CASCADE)
    autor = models.ForeignKey("Usuario", on_delete=models.CASCADE)
    comentario = models.TextField()
    data_comentario = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.autor} em {self.postagem}"


class Avaliacao(models.Model):
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE)
    design = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    frontend = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    backend = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    programacao = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    mobile = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    facilidade_navegacao = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    qualidade_conteudo = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Avaliação de {self.usuario.username} em {self.data_avaliacao}'