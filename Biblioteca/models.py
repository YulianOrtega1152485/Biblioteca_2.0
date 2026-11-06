from django.db import models
import datetime

# Create your models here.
class Estudiante(models.Model):
    codigo=models.CharField(max_length=10, blank=False, null=False,unique=True)
    nombre=models.CharField(max_length=100, blank=False, null=False)
    email=models.CharField(max_length=100, blank=False, null=False,unique=True)

    def __str__(self):
        return f"{codigo}-{nombre}"

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
        if(self.año_publicacion>datetime.date.today().year):
            raise ValueError("El AÑO ES SUPERIOR AL ACTUAL")
        if(self.año_publicacion<1000):
            raise ValueError("El AÑO NO PUEDE SER MENOR AL LOS 1000 AÑOS")



    def __str__(self):
        return f'{self.ISBN}-{self.titulo}({self.año_publicacion})'
    
