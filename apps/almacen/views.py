from django.shortcuts import render

def almacen_view(request):
    return render(request, 'almacen.html')