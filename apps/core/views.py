from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Count
from apps.grabados.models import Grabado, Maquina, TipoGrabado
import json
from datetime import datetime, timedelta
from django.db.models.functions import TruncDate

class DashboardView(TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # --- KPIs ---
        treinta_dias_atras = datetime.now() - timedelta(days=30)
        
        context['kpi_pendientes'] = Grabado.objects.filter(estado='PENDIENTE').count()
        context['kpi_completados_30d'] = Grabado.objects.filter(estado='COMPLETADO', fecha_programacion__gte=treinta_dias_atras).count()
        context['kpi_total_ofs'] = Grabado.objects.count()
        
        cliente_principal = Grabado.objects.values('cliente').annotate(total=Count('cliente')).order_by('-total').first()
        context['kpi_cliente_principal'] = cliente_principal['cliente'] if cliente_principal else 'N/A'

        # --- Gráficos (existentes) ---
        # Gráfico 1: Grabados por Estado
        grabados_por_estado = Grabado.objects.values('estado').annotate(total=Count('estado')).order_by('estado')
        context['estados_labels'] = json.dumps([item['estado'] for item in grabados_por_estado])
        context['estados_data'] = json.dumps([item['total'] for item in grabados_por_estado])

        # Gráfico 2: Grabados por Máquina
        grabados_por_maquina = Maquina.objects.annotate(total_grabados=Count('grabado')).order_by('nombre')
        context['maquinas_labels'] = json.dumps([maquina.nombre for maquina in grabados_por_maquina])
        context['maquinas_data'] = json.dumps([maquina.total_grabados for maquina in grabados_por_maquina])

        # Gráfico 3: Grabados por Tipo
        grabados_por_tipo = TipoGrabado.objects.annotate(total_grabados=Count('grabado')).order_by('nombre')
        context['tipos_labels'] = json.dumps([tipo.nombre for tipo in grabados_por_tipo])
        context['tipos_data'] = json.dumps([tipo.total_grabados for tipo in grabados_por_tipo])

        # Gráfico 4: Gráfico de Tendencia (Últimos 30 días)
        grabados_por_dia = (
            Grabado.objects.filter(fecha_programacion__gte=treinta_dias_atras)
            .annotate(dia=TruncDate('fecha_programacion'))
            .values('dia')
            .annotate(total=Count('of_numero'))
            .order_by('dia')
        )

        # Preparar datos para el gráfico, rellenando días sin datos
        date_map = {item['dia']: item['total'] for item in grabados_por_dia}
        tendencia_labels = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]
        tendencia_data = [date_map.get(datetime.strptime(date, '%Y-%m-%d').date(), 0) for date in tendencia_labels]

        context['tendencia_labels'] = json.dumps(tendencia_labels)
        context['tendencia_data'] = json.dumps(tendencia_data)
        
        # Gráfico 5: Top 5 Clientes
        top_clientes = (
            Grabado.objects.values('cliente')
            .annotate(total=Count('cliente'))
            .order_by('-total')[:5]
        )
        context['clientes_labels'] = json.dumps([item['cliente'] for item in top_clientes])
        context['clientes_data'] = json.dumps([item['total'] for item in top_clientes])

        context['page_title'] = "Dashboard Ejecutivo"
        return context

# End of file