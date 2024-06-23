from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, PostForum, ComentariosPost, Avaliacao
from django import forms


class CadastroForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']

        if len(username) < 5:
            raise forms.ValidationError('Nome de usuário deve ter pelo menos 5 caracteres.')
        
        if ' ' in username:
            raise forms.ValidationError('Nome de usuário não pode conter espaços.')

        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError("Nome de usuário já cadastrado")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("E-mail já cadastrado. Faça login para continuar")
        return email
    
    def clean_password2(self):
        senha1 = self.cleaned_data.get("password1")
        senha2 = self.cleaned_data["password2"]
        username = self.cleaned_data.get("username")

        if senha1 and senha2 and senha1 != senha2:
            raise forms.ValidationError("As senhas não conferem. Verifique novamente")
        if username and username.lower() in senha2.lower():
            raise forms.ValidationError("Seu nome de usuário não pode estar contido na senha")
        if len(senha2) < 8:
            raise forms.ValidationError("Senha deve conter, no mínimo, 8 caracteres")
        return senha2
    
    def clean_password1(self):
        username = self.cleaned_data.get("username")
        senha1 = self.cleaned_data["password1"]

        if len(senha1) < 8:
            raise forms.ValidationError("Senha deve conter, no mínimo, 8 caracteres")
        if username and username.lower() in senha1.lower():
            raise forms.ValidationError("Seu nome de usuário não pode estar contido na senha")
        return senha1


class PostForm(forms.ModelForm):
    class Meta:
        model = PostForum
        fields = ["curso", "titulo", "conteudo"]

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = ComentariosPost
        fields = ['comentario']


from django import forms
from .models import Avaliacao

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['design', 'frontend', 'backend', 'programacao', 'mobile', 'facilidade_navegacao', 'qualidade_conteudo']
        widgets = {
            'design': forms.RadioSelect,
            'frontend': forms.RadioSelect,
            'backend': forms.RadioSelect,
            'programacao': forms.RadioSelect,
            'mobile': forms.RadioSelect,
            'facilidade_navegacao': forms.RadioSelect,
            'qualidade_conteudo': forms.RadioSelect,
        } 