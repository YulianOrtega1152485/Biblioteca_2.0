from django.contrib import admin
from .models import Estudiante,Libro,Categoria,Autor,Copia_Fisica,Prestamo
from datetime import date
from django.contrib import messages
# Register your models here.
@admin.register(Estudiante)
class Estudiante_admin(admin.ModelAdmin):
    list_display=('codigo','nombre','email')
    search_fields=('codigo','nombre')

@admin.register(Categoria)
class Categoria_admin(admin.ModelAdmin):
    list_display=('descripcion',)

@admin.register(Autor)
class Autor_admin(admin.ModelAdmin):
    list_display=('nombre',)

class copia_fisica_inline(admin.TabularInline):
    model=Copia_Fisica
    extra=1
@admin.register(Libro)
class Libro_admin(admin.ModelAdmin):
    list_display=('ISBN','titulo','año_publicacion','categoria')
    search_fields=('ISBN','titulo')
    list_filter=('categoria',)
    inlines=[copia_fisica_inline]

@admin.register(Copia_Fisica)
class Copia_Fisica_admin(admin.ModelAdmin):
    list_display=('SKU','libro','condicion')
    search_fields=('SKU','libro__titulo')
    list_editable=('condicion',)
    list_filter=('condicion','libro')


class Estado_Prestamo_Filter(admin.SimpleListFilter):
    title='Estado'
    parameter_name='estado'

    def lookups(self, request,model_admin):
        return[
            ('activo','Sin devolver'),
            ('devuelto','Devuelto'),
        ]
    def queryset(self,request,queryset):
        if self.value()=='activo':
            return queryset.filter(fecha_devolucion__isnull=True)
        elif self.value()=='devuelto':
            return queryset.filter(fecha_devolucion__isnull=False)
        return queryset

@admin.register(Prestamo)
class Prestamo_admin(admin.ModelAdmin):
    list_display=('copia_fisica','estudiante','fecha_prestamo','fecha_limite','fecha_devolucion')
    search_fields=('estudiante__nombre','copia_fisica__SKU')
    readonly_fields=('fecha_prestamo',)
    list_filter=(Estado_Prestamo_Filter,)
    actions=['marcar_devueltos']

    @admin.action(description="Marcar prestamos seleccionados como devueltos")
    def marcar_devueltos(self,request,queryset):
        actualizados=queryset.filter(fecha_devolucion__isnull=True).update(fecha_devolucion=date.today())
        self.message_user(request,f'{actualizados} prestamo(s) marcado(s) como devuelto(s)',
        messages.SUCCESS)