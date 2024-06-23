# Necessário para criar uma página: url -> view -> template
from django.urls import path, include
from .views import Homepage, SobreNos, ManualUsuario, DetalhesCursos, Playlists, PesquisaVideo, Perfil, Cadastro, Quizzes, QuizzDesign, QuizzFrontend, QuizzBackend, QuizzProgramacao, QuizzMobile, LoginPersonalizado, CriarPost, ExcluirPostForum, DetalhesPostagem, AvaliacaoView
from django.contrib.auth import views as auth_view

app_name="curso"

urlpatterns = [
    path('', Homepage.as_view(), name="homepage"),
    path('criar-conta', Cadastro.as_view(), name="cadastro"),
    path('login', LoginPersonalizado.as_view(), name="login"),
    path('logout', auth_view.LogoutView.as_view(template_name="logout.html"), name="logout"),
    path('perfil/', Perfil.as_view(), name="perfil"),
    path('sobrenos', SobreNos.as_view(), name="sobrenos"),
    path('manualusuario', ManualUsuario.as_view(), name="manualusuario"),
    path('curso/<int:pk>', DetalhesCursos.as_view(), name="detalhescurso"),
    path('curso/playlist/<int:pk>', Playlists.as_view(), name="playlist"),
    path('pesquisa/', PesquisaVideo.as_view(), name="pesquisavideo"),
    path('quizzes/', Quizzes.as_view(), name="quizzes"),
    path('quizzes/quizz-design', QuizzDesign.as_view(), name="quizzdesign"),
    path('quizzes/quizz-frontend', QuizzFrontend.as_view(), name="quizzfront"),
    path('quizzes/quizz-backend', QuizzBackend.as_view(), name="quizzback"),
    path('quizzes/quizz-programacao', QuizzProgramacao.as_view(), name="quizzprog"),
    path('quizzes/quizz-mobile', QuizzMobile.as_view(), name="quizzmobile"),
    path('foruns/', CriarPost.as_view(), name="foruns"),
    path('excluir/<int:pk>/', ExcluirPostForum.as_view(), name='excluir_post'),
    path('foruns/<int:pk>/', DetalhesPostagem.as_view(), name='detalhes_post'),
    path('avaliacao/', AvaliacaoView.as_view(), name="avaliacao")
]