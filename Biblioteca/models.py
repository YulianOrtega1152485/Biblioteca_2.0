from django.db import models
import datetime
from django.core.exceptions import ValidationError

# Create your models here.
class Estudiante(models.Model):
    codigo=models.CharField(max_length=10, blank=False, null=False,unique=True)
    nombre=models.CharField(max_length=100, blank=False, null=False)
    email=models.EmailField(blank=False, null=False,unique=True)

    def __str__(self):
        return f"{self.codigo}-{self.nombre}"

class Categoria(models.Model):
    descripcion=models.CharField(max_length=100, blank=False,null=False, unique=True) 
    
    def __str__(self):
        return self.descripcion

class Autor(models.Model):
    nombre=models.CharField(max_length=150)

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    titulo=models.CharField(max_length=250,blank=False,null=False)
    año_publicacion=models.PositiveIntegerField(blank=False,null=False)
    ISBN=models.CharField(max_length=17,blank=False,null=False,unique=True)
    categoria=models.ForeignKey(Categoria,on_delete=models.PROTECT,related_name='libros',blank=False,null=False)
    autor=models.ManyToManyField(Autor,related_name='libros')

    def clean(self):
        if self.año_publicacion is not None:
            if(self.año_publicacion>datetime.date.today().year):
                raise ValidationError({'año_publicacion':"El AÑO ES SUPERIOR AL ACTUAL"})
            if(self.año_publicacion<1000):
                raise ValidationError({'año_publicacion',"El AÑO NO PUEDE SER MENOR AL LOS 1000 AÑOS"})

    def __str__(self):
        return f'{self.ISBN}-{self.titulo}({self.año_publicacion})'

class Copia_Fisica(models.Model):
    class Condicion(models.TextChoices):
        NUEVO='nuevo','Nuevo'
        USADO='usado','Usado'
        DANADO='danado','Dañado'
    SKU=models.CharField(max_length=50, blank=False,null=False,unique=True)
    condicion=models.CharField(max_length=10,choices=Condicion.choices,default=Condicion.NUEVO, blank=True,null=False)
    libro=models.ForeignKey(Libro,on_delete=models.PROTECT,related_name='copias_fisicas',null=False,blank=False)
    observaciones=models.TextField(blank=True)

    def __str__(self):
        return f'{self.SKU}-{self.libro.titulo}-{self.condicion}'

class Prestamo(models.Model):
    
    def fecha_limite_default():
        return datetime.date.today()+datetime.timedelta(days=15)

    copia_fisica=models.ForeignKey(Copia_Fisica,on_delete=models.PROTECT,related_name='prestamos',null=False,blank=False)
    estudiante=models.ForeignKey(Estudiante,on_delete=models.PROTECT,related_name='prestamos',null=False,blank=False)
    fecha_prestamo=models.DateField(auto_now_add=True)
    fecha_limite=models.DateField(default=fecha_limite_default)
    fecha_devolucion=models.DateField(null=True,blank=True)
    
    class Meta:
        constraints=[models.UniqueConstraint(fields=['copia_fisica'],condition=models.Q(fecha_devolucion__isnull=True),name='unique_copia_prestada')]

    
    def clean(self):
        if self.fecha_devolucion is None and self.copia_fisica_id:
            existe_prestamo_activo=Prestamo.objects.filter(
                copia_fisica=self.copia_fisica,
                fecha_devolucion__isnull=True
            ).exclude(pk=self.pk).exists()
            if existe_prestamo_activo:
                raise ValidationError("Lo siento, esta copia fisica ya ha sido prestada")
    
    def __str__(self):
        return f'{fecha_prestamo}-{estudiante}-{copia_fisica}-{fecha_limite}'