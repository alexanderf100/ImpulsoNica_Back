from rest_framework import serializers
from .models import *

# Generador dinámico o manual de serializadores para cada tabla
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

class CandidatosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidatos
        fields = '__all__'

class EmpleosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleos
        fields = '__all__'

class VacantesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacantes
        fields = '__all__'

class PostulacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postulaciones
        fields = '__all__'

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