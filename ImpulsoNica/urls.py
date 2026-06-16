from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

# =====================================================================
# ENRUTADOR AUTOMÁTICO DE VIEWSETS (Evita errores 404)
# =====================================================================
router = DefaultRouter()

# Catálogos y Geografía
router.register(r'departamentos', DepartamentosViewSet)
router.register(r'municipios', MunicipiosViewSet)
router.register(r'cat-sectores', CatSectoresViewSet)
router.register(r'cat-tiposempresa', CatTiposEmpresaViewSet)
router.register(r'generos', CatGenerosViewSet)
router.register(r'estadosciviles', CatEstadosCivilesViewSet)
router.register(r'nacionalidades', CatNacionalidadesViewSet)
router.register(r'cat-niveleseducativos', CatNivelesEducativosViewSet)
router.register(r'cat-idiomas', CatIdiomasViewSet)
router.register(r'cat-habilidades', CatHabilidadesViewSet)
router.register(r'cat-tiposempleo', CatTiposEmpleoViewSet)
router.register(r'cat-modalidades', CatModalidadesViewSet)
router.register(r'cat-estados', CatEstadosViewSet)

# Tablas principales
router.register(r'administradores', AdministradoresViewSet)
router.register(r'empresas', EmpresasViewSet)
router.register(r'curriculum', CurriculumViewSet)
router.register(r'candidatos', CandidatosViewSet)
router.register(r'empleos', EmpleosViewSet)
router.register(r'vacantes', VacantesViewSet)
router.register(r'postulaciones', PostulacionesViewSet)

# Tablas dependientes / Intersecciones (AQUÍ ESTABAN LOS 404)
router.register(r'experiencialaboral', ExperienciaLaboralViewSet)
router.register(r'referencias', ReferenciasViewSet)
router.register(r'empleorequisitos', EmpleoRequisitosViewSet)
router.register(r'curriculumhabilidades', CurriculumHabilidadesViewSet)
router.register(r'curriculumidiomas', CurriculumIdiomasViewSet)

# =====================================================================
# REGISTRO DE RUTAS FINALES
# =====================================================================
urlpatterns = [
    # Incluir todas las rutas automáticas del router
    path('', include(router.urls)),

    # Rutas de Autenticación y Perfil (APIViews normales)
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('mi-perfil/', MiPerfilView.as_view(), name='mi_perfil'),
    path('upload-imagen/', SubirImagenView.as_view(), name='upload_imagen'),
]