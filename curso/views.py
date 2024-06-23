from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Avg
from django.shortcuts import render, redirect
from .models import Curso, Playlist, Video, PostForum, ComentariosPost, Avaliacao
from .forms import CadastroForm, PostForm, ComentarioForm, AvaliacaoForm
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse, reverse_lazy
from collections import defaultdict
import random

# Create your views here.
class Homepage(TemplateView):
    template_name = "index.html"


class SobreNos(TemplateView):
    template_name = "sobre.html"


class ManualUsuario(TemplateView):
    template_name = "manual.html"


class DetalhesCursos(LoginRequiredMixin, DetailView):
    template_name = "curso.html"
    model = Curso


class Playlists(LoginRequiredMixin, DetailView):
    template_name = "playlist.html"
    queryset = Playlist.objects.all() 
    
    def get(self, request, *args, **kwargs):
        playlist = self.get_object()
        request.user.playlists_acessadas.add(playlist)
        return super().get(request, *args, **kwargs)


class PesquisaVideo(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Video

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = Video.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None


class Perfil(LoginRequiredMixin, TemplateView):
    template_name = "perfil.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user

        playlists_acessadas = usuario.playlists_acessadas.all()
        playlists_acessadas_ids = playlists_acessadas.values_list('id', flat=True)
        cursos_acessados_ids = playlists_acessadas.values_list('curso__id', flat=True)

        # Recomenda playlists aleatórias que o usuário ainda não acessou
        playlists_recomendadas = Playlist.objects.filter(curso_id__in=cursos_acessados_ids).exclude(id__in=playlists_acessadas_ids).order_by('?')[:9]
    
        context['usuario'] = usuario
        context['playlists_acessadas'] = playlists_acessadas
        context['playlists_recomendadas'] = playlists_recomendadas
    
        return context


class Cadastro(FormView):
    template_name = "cadastro.html"
    form_class = CadastroForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("curso:login")
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, dados_post=self.request.POST))


class LoginPersonalizado(AuthLoginView):
    template_name = 'login.html'
    success_url = reverse_lazy("curso:homepage")

    def form_invalid(self, form):
        messages.error(self.request, 'Nome de usuário ou senha incorretos.')
        return super().form_invalid(form)

class Quizzes(TemplateView):
    template_name = "quizzes.html"


class QuizzDesign(TemplateView):
    template_name = "quizzdesign.html"


class QuizzFrontend(TemplateView):
    template_name = "quizzfront.html"


class QuizzBackend(TemplateView):
    template_name = "quizzback.html"


class QuizzProgramacao(TemplateView):
    template_name = "quizzprog.html"


class QuizzMobile(TemplateView):
    template_name = "quizzmobile.html"


class CriarPost(LoginRequiredMixin, CreateView):
    template_name = "foruns.html"
    model = PostForum
    form_class = PostForm
    success_url = reverse_lazy('curso:foruns')

    def form_valid(self, form):
        form.instance.autor = self.request.user  # Associa o autor ao usuário autenticado
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = PostForum.objects.order_by('-data_postagem')
        return context

class ExcluirPostForum(DeleteView):
    model = PostForum
    template_name = 'confirmar-excluir.html'
    success_url = reverse_lazy('curso:foruns')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()  # Passa o objeto post para o contexto do template
        return context
    

class ComentarPost(FormView):
    model = ComentariosPost
    form_class = ComentarioForm

    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.post_id = self.kwargs['post_id']  # Obtém o ID da postagem a partir dos parâmetros da URL
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('curso:detalhes_post', kwargs={'post_id': self.kwargs['post_id']})


class DetalhesPostagem(FormMixin, DetailView):
    template_name = "discussao.html"
    model = PostForum
    form_class = ComentarioForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['comentarios'] = self.object.comentarios.all().order_by('-data_comentario')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.post = self.object
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('curso:detalhes_post', kwargs={'pk': self.object.pk})


class AvaliacaoView(LoginRequiredMixin, FormView):
    template_name = 'avaliacao.html'

    form_class = AvaliacaoForm
    success_url = reverse_lazy('curso:avaliacao')

    def form_valid(self, form):
        avaliacao = form.save(commit=False)
        avaliacao.usuario = self.request.user
        avaliacao.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medias'] = Avaliacao.objects.aggregate(
            media_design=Avg('design'),
            media_frontend=Avg('frontend'),
            media_backend=Avg('backend'),
            media_programacao=Avg('programacao'),
            media_mobile=Avg('mobile'),
            media_facilidade_navegacao=Avg('facilidade_navegacao'),
            media_qualidade_conteudo=Avg('qualidade_conteudo')
        )
        return context