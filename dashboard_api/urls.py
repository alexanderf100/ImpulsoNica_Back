from django.urls import path
from .views import DashboardOfertasView

urlpatterns = [
    # Esta ruta devolverá todos los datos agrupados para pintar tus gráficas
    path('metricas-ofertas/', DashboardOfertasView.as_view(), name='metricas-ofertas'),
]