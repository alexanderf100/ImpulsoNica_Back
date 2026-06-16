from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Obtenemos los tokens por defecto
        data = super().validate(attrs)
        user = self.user

        # Lógica de validación: Buscamos en qué tabla existe este usuario
        rol = 'candidato'  # Rol por defecto

        if user.is_superuser:
            rol = 'admin'
        elif Administradores.objects.filter(correo=user.email).exists() or Administradores.objects.filter(
                usuario=user.username).exists():
            rol = 'admin'
        elif Empresas.objects.filter(correo=user.email).exists() or Empresas.objects.filter(
                correo=user.username).exists():
            rol = 'empresa'
        elif Candidatos.objects.filter(correo=user.email).exists() or Candidatos.objects.filter(
                correo=user.username).exists():
            rol = 'candidato'

        # Agregamos el rol a la respuesta JSON que recibe el frontend
        data['rol'] = rol
        return data


# =====================================================================
# SERIALIZADORES DE CATÁLOGOS
# =====================================================================
class DepartamentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamentos
        fields = '__all__'


class MunicipiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipios
        fields = '__all__'


class CatSectoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatSectores
        fields = '__all__'


class CatTiposEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatTiposEmpresa
        fields = '__all__'


class CatGenerosSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatGeneros
        fields = '__all__'


class CatEstadosCivilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatEstadosCiviles
        fields = '__all__'


class CatNacionalidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatNacionalidades
        fields = '__all__'


class CatNivelesEducativosSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatNivelesEducativos
        fields = '__all__'


class CatIdiomasSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatIdiomas
        fields = '__all__'


class CatHabilidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatHabilidades
        fields = '__all__'


class CatTiposEmpleoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatTiposEmpleo
        fields = '__all__'


class CatModalidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatModalidades
        fields = '__all__'


class CatEstadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatEstados
        fields = '__all__'


# =====================================================================
# SERIALIZADORES DE TABLAS PRINCIPALES
# =====================================================================
class AdministradoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administradores
        fields = '__all__'


class EmpresasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresas
        fields = '__all__'


class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = '__all__'


# --- SERIALIZADOR DEL CANDIDATO MEJORADO ---
class CandidatosSerializer(serializers.ModelSerializer):
    genero_nombre = serializers.CharField(source='generoid.nombre', read_only=True, default=None)
    nacionalidad_nombre = serializers.CharField(source='nacionalidadid.nombre', read_only=True, default=None)
    estado_civil_nombre = serializers.CharField(source='estadocivilid.nombre', read_only=True, default=None)
    departamento_nombre = serializers.CharField(source='departamentoid.nombre', read_only=True, default=None)
    municipio_nombre = serializers.CharField(source='municipioid.nombre', read_only=True, default=None)

    class Meta:
        model = Candidatos
        fields = '__all__'


class EmpleosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleos
        fields = '__all__'
        # Eliminamos depth = 1 para que NO bloquee los POST/PUT.

    # Usamos este método para que "magicamente" recupere los datos expandidos SOLO cuando pedimos la lista (GET)
    def to_representation(self, instance):
        response = super().to_representation(instance)

        # Enriquecemos la respuesta con los datos de las tablas relacionadas
        if instance.empresaid:
            response['empresaid'] = EmpresasSerializer(instance.empresaid).data
        if instance.tipoempleoid:
            response['tipoempleoid'] = CatTiposEmpleoSerializer(instance.tipoempleoid).data
        if instance.modalidadid:
            response['modalidadid'] = CatModalidadesSerializer(instance.modalidadid).data
        if instance.estadoid:
            response['estadoid'] = CatEstadosSerializer(instance.estadoid).data

        return response


class VacantesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacantes
        fields = '__all__'


class PostulacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postulaciones
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.candidatoid:
            response['candidatoid'] = CandidatosSerializer(instance.candidatoid).data
        if instance.estadoid:
            response['estadoid'] = CatEstadosSerializer(instance.estadoid).data
        return response


class ExperienciaLaboralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienciaLaboral
        fields = '__all__'


class ReferenciasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referencias
        fields = '__all__'


class CurriculumHabilidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumHabilidades
        fields = '__all__'


class CurriculumIdiomasSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumIdiomas
        fields = '__all__'


class EmpleoRequisitosSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpleoRequisitos
        fields = '__all__'