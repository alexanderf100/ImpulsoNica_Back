from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from .models import *
from .serializers import *

def home(request):
    return HttpResponse("Bienvenido a la API de ImpulsoNica 🚀")

# Vistas de Catálogos
class DepartamentosViewSet(viewsets.ModelViewSet):
    queryset = Departamentos.objects.all()
    serializer_class = DepartamentosSerializer
    permission_classes = [AllowAny] # Los catálogos también deberían ser públicos

class MunicipiosViewSet(viewsets.ModelViewSet):
    queryset = Municipios.objects.all()
    serializer_class = MunicipiosSerializer

class CatSectoresViewSet(viewsets.ModelViewSet):
    queryset = CatSectores.objects.all()
    serializer_class = CatSectoresSerializer

class CatTiposEmpresaViewSet(viewsets.ModelViewSet):
    queryset = CatTiposEmpresa.objects.all()
    serializer_class = CatTiposEmpresaSerializer

class CatGenerosViewSet(viewsets.ModelViewSet):
    queryset = CatGeneros.objects.all()
    serializer_class = CatGenerosSerializer

class CatEstadosCivilesViewSet(viewsets.ModelViewSet):
    queryset = CatEstadosCiviles.objects.all()
    serializer_class = CatEstadosCivilesSerializer

class CatNacionalidadesViewSet(viewsets.ModelViewSet):
    queryset = CatNacionalidades.objects.all()
    serializer_class = CatNacionalidadesSerializer

class CatNivelesEducativosViewSet(viewsets.ModelViewSet):
    queryset = CatNivelesEducativos.objects.all()
    serializer_class = CatNivelesEducativosSerializer

class CatIdiomasViewSet(viewsets.ModelViewSet):
    queryset = CatIdiomas.objects.all()
    serializer_class = CatIdiomasSerializer

class CatHabilidadesViewSet(viewsets.ModelViewSet):
    queryset = CatHabilidades.objects.all()
    serializer_class = CatHabilidadesSerializer

class CatTiposEmpleoViewSet(viewsets.ModelViewSet):
    queryset = CatTiposEmpleo.objects.all()
    serializer_class = CatTiposEmpleoSerializer

class CatModalidadesViewSet(viewsets.ModelViewSet):
    queryset = CatModalidades.objects.all()
    serializer_class = CatModalidadesSerializer

class CatEstadosViewSet(viewsets.ModelViewSet):
    queryset = CatEstados.objects.all()
    serializer_class = CatEstadosSerializer

# Vistas Principales
class AdministradoresViewSet(viewsets.ModelViewSet):
    queryset = Administradores.objects.all()
    serializer_class = AdministradoresSerializer

class EmpresasViewSet(viewsets.ModelViewSet):
    queryset = Empresas.objects.all()
    serializer_class = EmpresasSerializer

class CurriculumViewSet(viewsets.ModelViewSet):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer

class CandidatosViewSet(viewsets.ModelViewSet):
    queryset = Candidatos.objects.all()
    serializer_class = CandidatosSerializer

class EmpleosViewSet(viewsets.ModelViewSet):
    queryset = Empleos.objects.all()
    serializer_class = EmpleosSerializer
    permission_classes = [AllowAny] # <--- ¡Esto quita el candado!


class VacantesViewSet(viewsets.ModelViewSet):
    queryset = Vacantes.objects.all()
    serializer_class = VacantesSerializer

class PostulacionesViewSet(viewsets.ModelViewSet):
    queryset = Postulaciones.objects.all()
    serializer_class = PostulacionesSerializer

# Vistas Dependientes / Intersección
class ExperienciaLaboralViewSet(viewsets.ModelViewSet):
    queryset = ExperienciaLaboral.objects.all()
    serializer_class = ExperienciaLaboralSerializer

class ReferenciasViewSet(viewsets.ModelViewSet):
    queryset = Referencias.objects.all()
    serializer_class = ReferenciasSerializer

class CurriculumHabilidadesViewSet(viewsets.ModelViewSet):
    queryset = CurriculumHabilidades.objects.all()
    serializer_class = CurriculumHabilidadesSerializer

class CurriculumIdiomasViewSet(viewsets.ModelViewSet):
    queryset = CurriculumIdiomas.objects.all()
    serializer_class = CurriculumIdiomasSerializer

class EmpleoRequisitosViewSet(viewsets.ModelViewSet):
    queryset = EmpleoRequisitos.objects.all()
    serializer_class = EmpleoRequisitosSerializer