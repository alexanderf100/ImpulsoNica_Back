from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

# Catálogos
router.register(r'departamentos', DepartamentosViewSet)
router.register(r'municipios', MunicipiosViewSet)
router.register(r'cat-sectores', CatSectoresViewSet)
router.register(r'cat-tipos-empresa', CatTiposEmpresaViewSet)
router.register(r'cat-generos', CatGenerosViewSet)
router.register(r'cat-estados-civiles', CatEstadosCivilesViewSet)
router.register(r'cat-nacionalidades', CatNacionalidadesViewSet)
router.register(r'cat-niveles-educativos', CatNivelesEducativosViewSet)
router.register(r'cat-idiomas', CatIdiomasViewSet)
router.register(r'cat-habilidades', CatHabilidadesViewSet)
router.register(r'cat-tipos-empleo', CatTiposEmpleoViewSet)
router.register(r'cat-modalidades', CatModalidadesViewSet)
router.register(r'cat-estados', CatEstadosViewSet)

# Principales
router.register(r'administradores', AdministradoresViewSet)
router.register(r'empresas', EmpresasViewSet)
router.register(r'curriculum', CurriculumViewSet)
router.register(r'candidatos', CandidatosViewSet)
router.register(r'empleos', EmpleosViewSet)
router.register(r'vacantes', VacantesViewSet)
router.register(r'postulaciones', PostulacionesViewSet)

# Intersección y Dependientes
router.register(r'experiencia-laboral', ExperienciaLaboralViewSet)
router.register(r'referencias', ReferenciasViewSet)
router.register(r'curriculum-habilidades', CurriculumHabilidadesViewSet)
router.register(r'curriculum-idiomas', CurriculumIdiomasViewSet)
router.register(r'empleo-requisitos', EmpleoRequisitosViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('home/', home), # Opcional: si quieres mantener tu ruta de bienvenida separada
]