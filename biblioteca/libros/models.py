from django.db import models
from django.shortcuts import render

# Modelo para libros físicos
class LibroFisico(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    anio_publicacion = models.PositiveIntegerField()
    num_paginas = models.IntegerField()

    def __str__(self):
        return self.titulo
    
    @classmethod
    def filtrar_por_anio(cls, anio):
        return cls.objects.filter(anio_publicacion=anio)

    # Método de instancia para obtener detalles del libro
    def obtener_detalles(self):
        return f"'{self.titulo}' por {self.autor}, publicado en {self.anio_publicacion} con {self.num_paginas} páginas."

# Modelo para libros digitales
class LibroDigital(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    anio_publicacion = models.DateField()
    formato = models.CharField(max_length=50)
    tamanio_mb = models.FloatField()

    def __str__(self):
        return self.titulo
    
    @classmethod
    def buscar_por_formato(cls, formato):
        return cls.objects.filter(formato__icontains=formato)

    # Método de instancia para obtener una descripción
    def descripcion(self):
        return f"'{self.titulo}' por {self.autor}, tamaño: {self.tamanio_mb}MB, formato: {self.formato}."   

# Relación muchos a muchos con autores
class Autor(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class LibroAutor(models.Model):
    libro = models.ForeignKey(LibroFisico, on_delete=models.CASCADE, related_name='libros_autor', null=True, blank=True)
    libro_digital = models.ForeignKey(LibroDigital, on_delete=models.CASCADE, related_name='libros_autor', null=True, blank=True)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.libro.titulo if self.libro else self.libro_digital.titulo} - {self.autor.nombre}"

# Relación muchos a muchos con categorías
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class LibroCategoria(models.Model):
    libro = models.ForeignKey(LibroFisico, on_delete=models.CASCADE, related_name='libros_categoria', null=True, blank=True)
    libro_digital = models.ForeignKey(LibroDigital, on_delete=models.CASCADE, related_name='libros_categoria', null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.libro.titulo if self.libro else self.libro_digital.titulo} - {self.categoria.nombre}"

# Modelo para editoriales
class Editorial(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

# Relación con editoriales
class LibroEditorial(models.Model):
    libro = models.ForeignKey(LibroFisico, on_delete=models.CASCADE, related_name='libros_editorial', null=True, blank=True)
    libro_digital = models.ForeignKey(LibroDigital, on_delete=models.CASCADE, related_name='libros_editorial', null=True, blank=True)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.libro.titulo if self.libro else self.libro_digital.titulo} - {self.editorial.nombre}"

# Modelo para ventas de libros
class Venta(models.Model):
    libro = models.ForeignKey(LibroFisico, on_delete=models.CASCADE, related_name='ventas_libro', null=True, blank=True)
    libro_digital = models.ForeignKey(LibroDigital, on_delete=models.CASCADE, related_name='ventas_libro', null=True, blank=True)
    fecha_venta = models.DateField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta de {self.libro.titulo if self.libro else self.libro_digital.titulo} - {self.precio} USD"


# Vista para la página principal
def home(request):
    # Obtener los libros físicos y digitales
    libros_fisicos = LibroFisico.objects.all()
    libros_digitales = LibroDigital.objects.all()

    # Pasar los libros al contexto
    return render(request, 'base.html', {
        'libros_fisicos': libros_fisicos,
        'libros_digitales': libros_digitales,
    })
