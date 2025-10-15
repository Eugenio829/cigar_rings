from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
from .models import Grabado, Maquina, TipoGrabado, Proceso
from django.db.models import Q
import operator
from functools import reduce
from django.db import transaction, IntegrityError
from django.http import HttpResponse
import io
from .forms import GrabadoForm

# Vista principal, renderiza la plantilla base
def index(request):
    return render(request, 'base.html')

# Vista base para grabados
def grabados_view(request):
    return render(request, 'grabados/base_grabados.html')

# Vista para consultar grabados con filtros avanzados y búsqueda
def grabado_consulta(request):
    # Obtiene todas las opciones para los filtros desplegables
    maquinas = Maquina.objects.all()
    tipos_grabado = TipoGrabado.objects.all()
    procesos = Proceso.objects.all()

    # Obtiene los parámetros de filtro desde la petición
    query = request.GET.get('q', '')
    estado = request.GET.get('estado', '')
    maquina_id = request.GET.get('maquina', '')
    tipo_grabado_id = request.GET.get('tipo_grabado', '')
    proceso_id = request.GET.get('proceso', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')

    # Comienza con todos los grabados
    grabados = Grabado.objects.all()

    # Aplica filtro de búsqueda por palabras múltiples
    if query:
        search_terms = query.split()
        if search_terms:
            # Para cada término, crea un objeto Q que busca en varios campos (OR)
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

    # Aplica filtros avanzados según los parámetros recibidos
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

    # Contexto para la plantilla
    context = {
        'grabados': grabados,
        'maquinas': maquinas,
        'tipos_grabado': tipos_grabado,
        'procesos': procesos,
        'query': query,
        'request': request,
    }

    # Si la petición es AJAX, renderiza solo las filas de la tabla
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'grabados/_grabado_table_rows.html', context)
    
    # Renderiza la consulta completa
    return render(request, 'grabados/grabado_consulta.html', context)

# Vista para importar grabados desde un archivo Excel subido por el usuario
def importar_from_upload_view(request):
    if request.method != 'POST':
        return render(request, 'grabados/importar_upload.html')

    if 'excel_file' not in request.FILES:
        messages.error(request, 'No se seleccionó ningún archivo.')
        return redirect('importar_upload')

    excel_file = request.FILES['excel_file']
    if not excel_file.name.endswith(('.xls', '.xlsx')):
        messages.error(request, 'El archivo no es un formato de Excel válido (.xls o .xlsx).')
        return redirect('importar_upload')

    try:
        df = pd.read_excel(excel_file)
    except Exception as e:
        messages.error(request, f'No se pudo leer el archivo Excel. Error: {e}')
        return redirect('importar_upload')

    required_columns = [
        'OF.', 'OF. Referencia', 'Descripción', 'Cliente', 'Tipo de grabado',
        'Proceso', 'Máquina', 'Estado', 'Fecha de Programación', 'Ubicación'
    ]
    
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        messages.error(request, f"Faltan las siguientes columnas en el archivo: {', '.join(missing_cols)}")
        return redirect('importar_upload')

    errors = []
    imported_count = 0
    updated_count = 0

    try:
        with transaction.atomic():
            for index, row in df.iterrows():
                try:
                    # --- Validación y limpieza de datos ---
                    of_numero = row['OF.']
                    if pd.isna(of_numero):
                        raise ValueError("La columna 'OF.' no puede estar vacía.")
                    
                    # --- Obtener o crear objetos relacionados ---
                    tipo_grabado, _ = TipoGrabado.objects.get_or_create(nombre=row['Tipo de grabado'])
                    proceso, _ = Proceso.objects.get_or_create(nombre=row['Proceso'])
                    maquina, _ = Maquina.objects.get_or_create(nombre=row['Máquina'])

                    # --- Crear o actualizar el objeto principal ---
                    grabado_data = {
                        'of_referencia': row['OF. Referencia'],
                        'descripcion': row['Descripción'],
                        'cliente': row['Cliente'],
                        'tipo_grabado': tipo_grabado,
                        'proceso': proceso,
                        'maquina': maquina,
                        'estado': row['Estado'].upper(),
                        'fecha_programacion': row['Fecha de Programación'],
                        'ubicacion': row['Ubicación'],
                    }
                    
                    obj, created = Grabado.objects.update_or_create(
                        of_numero=int(of_numero),
                        defaults=grabado_data
                    )

                    if created:
                        imported_count += 1
                    else:
                        updated_count += 1

                except (ValueError, TypeError) as e:
                    errors.append(f"Fila {index + 2}: Error de datos - {e}. Verifique que los números y fechas sean correctos.")
                except IntegrityError:
                    errors.append(f"Fila {index + 2}: El número de OF '{int(of_numero)}' o la Referencia ya existen.")
            
            if errors:
                # Si hay errores, la transacción no se confirmará.
                raise Exception("Se encontraron errores durante la validación.")

    except Exception as e:
        # Captura la excepción elevada para detener la transacción o cualquier otro error general.
        if not errors: # Si el error fue inesperado y no de validación de fila
            messages.error(request, f"Ocurrió un error inesperado: {e}")
        else:
            for error in errors:
                messages.error(request, error)
        return redirect('importar_upload')

    messages.success(request, f'Importación completada. {imported_count} registros creados y {updated_count} actualizados.')
    return redirect('grabado_consulta')

def exportar_excel(request):
    """
    Exporta datos de grabados a un archivo Excel según el tipo solicitado.
    - tipo=plantilla: Exporta solo los encabezados.
    - tipo=ejemplo: Exporta encabezados y una fila de ejemplo.
    - tipo=todo: Exporta todos los registros de la base de datos.
    """
    export_type = request.GET.get('tipo', 'todo')
    
    # Definir las columnas que se usarán tanto para la plantilla como para la exportación
    columns = [
        'OF.', 'OF. Referencia', 'Descripción', 'Cliente', 'Tipo de grabado',
        'Proceso', 'Máquina', 'Estado', 'Fecha de Programación', 'Ubicación'
    ]
    
    # Crear un DataFrame de pandas
    df = pd.DataFrame(columns=columns)
    
    if export_type == 'ejemplo':
        # Añadir una fila de ejemplo al DataFrame
        example_data = {
            'OF.': [9999],
            'OF. Referencia': ['REF-EJEMPLO-2025'],
            'Descripción': ['Descripción de ejemplo para el grabado'],
            'Cliente': ['Cliente de Ejemplo S.A.'],
            'Tipo de grabado': ['Láser CO2'],
            'Proceso': ['Grabado'],
            'Máquina': ['Máquina 01'],
            'Estado': ['PENDIENTE'],
            'Fecha de Programación': ['2025-12-31'],
            'Ubicación': ['Taller Z - Mesa 99']
        }
        df = pd.DataFrame(example_data)

    elif export_type == 'todo':
        # Obtener todos los grabados de la base de datos
        grabados = Grabado.objects.all().values(
            'of_numero',
            'of_referencia',
            'descripcion',
            'cliente',
            'tipo_grabado__nombre',
            'proceso__nombre',
            'maquina__nombre',
            'estado',
            'fecha_programacion',
            'ubicacion'
        )
        
        # Renombrar las columnas para que coincidan con la plantilla
        df_data = pd.DataFrame(list(grabados)).rename(columns={
            'of_numero': 'OF.',
            'of_referencia': 'OF. Referencia',
            'descripcion': 'Descripción',
            'cliente': 'Cliente',
            'tipo_grabado__nombre': 'Tipo de grabado',
            'proceso__nombre': 'Proceso',
            'maquina__nombre': 'Máquina',
            'estado': 'Estado',
            'fecha_programacion': 'Fecha de Programación',
            'ubicacion': 'Ubicación'
        })
        df = pd.concat([df, df_data], ignore_index=True)

    # Usar un buffer en memoria para guardar el archivo Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Grabados')
    
    # Rebobinar el buffer
    output.seek(0)
    
    # Crear la respuesta HTTP
    filename = f"export_grabados_{export_type}.xlsx"
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

def grabado_crear(request):
    if request.method == 'POST':
        form = GrabadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grabado creado exitosamente.')
            return redirect('grabado_consulta')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = GrabadoForm()
    
    return render(request, 'grabados/grabado_form.html', {'form': form})