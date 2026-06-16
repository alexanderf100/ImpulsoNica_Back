from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Avg
from .models import FactOfertaslaborales

class DashboardOfertasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. Agrupación por Sector
        ofertas_por_sector = FactOfertaslaborales.objects.using('dw_impulsonica').values(
            'sectorkey__nombresector'
        ).annotate(
            total_vacantes=Sum('cantidadvacantes'),
            total_postulaciones=Sum('totalpostulacionesrecibidas'),
            salario_promedio=Avg('salarioofrecido')
        ).order_by('-total_vacantes')

        # 2. Agrupación por Ubicación
        ofertas_por_ubicacion = FactOfertaslaborales.objects.using('dw_impulsonica').values(
            'ubicacionkey__departamento'
        ).annotate(
            total_vacantes=Sum('cantidadvacantes')
        ).order_by('-total_vacantes')

        # 3. Evolución Mensual
        ofertas_por_mes = FactOfertaslaborales.objects.using('dw_impulsonica').values(
            'tiempopublicacionkey__nombremes', 'tiempopublicacionkey__mes'
        ).annotate(
            total_vacantes=Sum('cantidadvacantes')
        ).order_by('tiempopublicacionkey__mes')

        # 4. Modalidad de Trabajo
        ofertas_por_modalidad = FactOfertaslaborales.objects.using('dw_impulsonica').values(
            'empleokey__modalidad'
        ).annotate(
            total_vacantes=Sum('cantidadvacantes')
        ).order_by('-total_vacantes')

        # --- NUEVOS GRÁFICOS (EXPRIMIENDO EL DW) ---

        # 5. Top 10 Empresas con más Vacantes
        top_empresas = FactOfertaslaborales.objects.using('dw_impulsonica').values(
            'empresakey__nombreempresa'
        ).annotate(
            total_vacantes=Sum('cantidadvacantes')
        ).order_by('-total_vacantes')[:10] # Solo las 10 mejores

        # 6. Distribución por Tipo de Empleo
        tipos_empleo = FactOfertaslaborales.objects.using('dw_impulsonica').values(
            'empleokey__tipoempleo'
        ).annotate(
            total_vacantes=Sum('cantidadvacantes')
        ).order_by('-total_vacantes')

        # 7. Salario Promedio por Sector
        salarios_sector = FactOfertaslaborales.objects.using('dw_impulsonica').values(
            'sectorkey__nombresector'
        ).annotate(
            promedio_salario=Avg('salarioofrecido')
        ).order_by('-promedio_salario')

        # 8. Tiempo Promedio de Cierre (Días Abierta)
        dias_abierta = FactOfertaslaborales.objects.using('dw_impulsonica').values(
            'sectorkey__nombresector'
        ).annotate(
            promedio_dias=Avg('diasabierta')
        ).order_by('-promedio_dias')

        # 9. Exigencia: Promedio de Requisitos
        requisitos_sector = FactOfertaslaborales.objects.using('dw_impulsonica').values(
            'sectorkey__nombresector'
        ).annotate(
            promedio_requisitos=Avg('cantidadrequisitos')
        ).order_by('-promedio_requisitos')

        return Response({
            "ofertas_por_sector": list(ofertas_por_sector),
            "ofertas_por_ubicacion": list(ofertas_por_ubicacion),
            "ofertas_por_mes": list(ofertas_por_mes),
            "ofertas_por_modalidad": list(ofertas_por_modalidad),
            "top_empresas": list(top_empresas),
            "tipos_empleo": list(tipos_empleo),
            "salarios_sector": list(salarios_sector),
            "dias_abierta": list(dias_abierta),
            "requisitos_sector": list(requisitos_sector)
        })