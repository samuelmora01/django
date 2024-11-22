from django.shortcuts import render, redirect, get_object_or_404
from .forms import LibroFisicoForm, LibroDigitalForm
from django.db.models import Q
from .models import LibroFisico, LibroDigital

def index(request):
    libros_fisicos = LibroFisico.objects.all()
    libros_digitales = LibroDigital.objects.all()

    form = None

    if request.method == "POST":
        tipo_libro = request.POST.get("type")

        if tipo_libro == "fisico":
            form = LibroFisicoForm(request.POST)
        elif tipo_libro == "digital":
            form = LibroDigitalForm(request.POST)
        else:
            form = None

        if form and form.is_valid():
            form.save()
            return redirect("/")

    else:
        tipo_libro = request.GET.get("type")
        if tipo_libro == "fisico":
            form = LibroFisicoForm()
        elif tipo_libro == "digital":
            form = LibroDigitalForm()
        else:
            form = None

    return render(request, "base.html", {
        "libros_fisicos": libros_fisicos,
        "libros_digitales": libros_digitales,
        "form": form,
    })

def editar_libro(request, libro_id, tipo):
    if tipo == "fisico":
        libro = get_object_or_404(LibroFisico, id=libro_id)
        form_class = LibroFisicoForm
        template = "formulario-fisico.html"
    elif tipo == "digital":
        libro = get_object_or_404(LibroDigital, id=libro_id)
        form_class = LibroDigitalForm
        template = "formulario-digital.html"
    else:
        return redirect("/")

    if request.method == "POST":
        form = form_class(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = form_class(instance=libro)

    return render(request, template, {"form": form, "libro": libro})

def eliminar_libro(request, libro_id, tipo):
    if tipo == "fisico":
        libro = get_object_or_404(LibroFisico, id=libro_id)
    elif tipo == "digital":
        libro = get_object_or_404(LibroDigital, id=libro_id)
    else:
        return redirect("/")

    if request.method == "POST":
        libro.delete()
        return redirect("/")

    return render(request, "confirmDelete.html", {"libro": libro})

def libro_list(request):
    libros_fisicos = LibroFisico.objects.all()
    libros_digitales = LibroDigital.objects.all()

    return render(request, 'libros/libro_list.html', {
        'libros_fisicos': libros_fisicos,
        'libros_digitales': libros_digitales,
    })

def home(request):
    libros_fisicos = LibroFisico.objects.all()
    libros_digitales = LibroDigital.objects.all()

    return render(request, 'base.html', {
        'libros_fisicos': libros_fisicos,
        'libros_digitales': libros_digitales,
    })

def buscar_libros(request):
    query = request.GET.get('q', '')  # Obtener el término de búsqueda
    resultados_fisicos = []
    resultados_digitales = []

    if query:
        # Buscar en ambos modelos
        resultados_fisicos = LibroFisico.objects.filter(
            Q(titulo__icontains=query) | Q(autor__icontains=query)
        )
        resultados_digitales = LibroDigital.objects.filter(
            Q(titulo__icontains=query) | Q(autor__icontains=query)
        )

    return render(request, "buscar_libros.html", {
        "query": query,
        "resultados_fisicos": resultados_fisicos,
        "resultados_digitales": resultados_digitales,
    })