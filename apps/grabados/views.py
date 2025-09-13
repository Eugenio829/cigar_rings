from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
from .models import Grabado, Maquina, TipoGrabado, Proceso
from django.db.models import Q
import operator
from functools import reduce

def index(request):
    return render(request, 'base.html')

def grabados_view(request):
    return render(request, 'grabados/base_grabados.html')

def grabado_consulta(request):
    # Get all filter options for the dropdowns
    maquinas = Maquina.objects.all()
    tipos_grabado = TipoGrabado.objects.all()
    procesos = Proceso.objects.all()

    # Get filter parameters from the request
    query = request.GET.get('q', '')
    estado = request.GET.get('estado', '')
    maquina_id = request.GET.get('maquina', '')
    tipo_grabado_id = request.GET.get('tipo_grabado', '')
    proceso_id = request.GET.get('proceso', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')

    # Start with all grabados
    grabados = Grabado.objects.all()

    # Apply multi-word search query filter
    if query:
        search_terms = query.split()
        if search_terms:
            # For each term, create a Q object that searches across multiple fields (OR)
            term_queries = [
                (
                    Q(of_referencia__icontains=term) |
                    Q(descripcion__icontains=term) |
                    Q(cliente__icontains=term) |
                    Q(tipo_grabado__nombre__icontains=term) |
                    Q(proceso__nombre__icontains=term) |
                    Q(maquina__nombre__icontains=term) |
                    Q(estado__icontains=term) |
                    Q(ubicacion__icontains=term)
                )
                for term in search_terms
            ]
            # Chain the Q objects for each term together with an AND operator
            combined_query = reduce(operator.and_, term_queries)
            grabados = grabados.filter(combined_query).distinct()

    # Apply advanced filters
    if estado:
        grabados = grabados.filter(estado=estado)
    if maquina_id:
        grabados = grabados.filter(maquina_id=maquina_id)
    if tipo_grabado_id:
        grabados = grabados.filter(tipo_grabado_id=tipo_grabado_id)
    if proceso_id:
        grabados = grabados.filter(proceso_id=proceso_id)
    if fecha_desde:
        grabados = grabados.filter(fecha_programacion__gte=fecha_desde)
    if fecha_hasta:
        grabados = grabados.filter(fecha_programacion__lte=fecha_hasta)

    context = {
        'grabados': grabados,
        'maquinas': maquinas,
        'tipos_grabado': tipos_grabado,
        'procesos': procesos,
        'query': query,
        'request': request,
    }

    # Check if it is an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'grabados/_grabado_table_rows.html', context)
    
    return render(request, 'grabados/grabado_consulta.html', context)

def importar_from_upload_view(request):
    if request.method == 'POST':
        if 'excel_file' not in request.FILES:
            messages.error(request, 'No se seleccionó ningún archivo.')
            return redirect('importar_upload')

        excel_file = request.FILES['excel_file']

        # Check if the file is an excel file
        if not excel_file.name.endswith(('.xls', '.xlsx')):
            messages.error(request, 'El archivo no es un formato de Excel válido (.xls o .xlsx).')
            return redirect('importar_upload')

        try:
            df = pd.read_excel(excel_file)
            
            required_columns = [
                'OF. Referencia', 'Descripción', 'Cliente', 'Tipo de grabado', 
                'Proceso', 'Máquina', 'Estado', 'Fecha de Programación', 'Ubicación'
            ]
            
            # Verify that all required columns are in the DataFrame
            if not all(col in df.columns for col in required_columns):
                messages.error(request, f"El archivo de Excel debe contener las siguientes columnas: {required_columns}")
                return redirect('importar_upload')

            imported_count = 0
            for index, row in df.iterrows():
                # Get or create related objects
                tipo_grabado, _ = TipoGrabado.objects.get_or_create(nombre=row['Tipo de grabado'])
                proceso, _ = Proceso.objects.get_or_create(nombre=row['Proceso'])
                maquina, _ = Maquina.objects.get_or_create(nombre=row['Máquina'])

                # Create the Grabado object, checking for existence
                grabado, created = Grabado.objects.update_or_create(
                    of_referencia=row['OF. Referencia'],
                    defaults={
                        'descripcion': row['Descripción'],
                        'cliente': row['Cliente'],
                        'tipo_grabado': tipo_grabado,
                        'proceso': proceso,
                        'maquina': maquina,
                        'estado': row['Estado'].upper(),
                        'fecha_programacion': row['Fecha de Programación'],
                        'ubicacion': row['Ubicación'],
                    }
                )
                if created:
                    imported_count += 1

            messages.success(request, f'Se importaron y/o actualizaron {len(df)} registros. {imported_count} registros fueron creados.')
            return redirect('grabado_consulta')

        except Exception as e:
            messages.error(request, f'Ocurrió un error al procesar el archivo: {e}')
            return redirect('importar_upload')

    return render(request, 'grabados/importar_upload.html')