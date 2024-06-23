from django.contrib import admin
from .models import Curso, Playlist, Video, Usuario, Avaliacao
from django.contrib.auth.admin import UserAdmin

# esta edição existe pois o usuário é personalizado e não o padrão do django
campos = list(UserAdmin.fieldsets)
campos.append(
    ("Histórico", {'fields': ('playlists_acessadas',)})
)

UserAdmin.fieldsets = tuple(campos)

# Register your models here.
admin.site.register(Curso)
admin.site.register(Video)
admin.site.register(Playlist)
admin.site.register(Usuario, UserAdmin)
admin.site.register(Avaliacao)

