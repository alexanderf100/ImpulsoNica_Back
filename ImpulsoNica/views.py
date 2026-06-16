import datetime
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpResponse
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Candidatos, Empresas
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import FileSystemStorage
import traceback


class SubirImagenView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        archivo = request.FILES.get('imagen')

        if not archivo:
            return Response({'error': 'No se envió ninguna imagen'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Buscamos quién hizo la petición: Si fue un candidato o una empresa
            candidato = Candidatos.objects.filter(correo=user.username).first()
            empresa = Empresas.objects.filter(correo=user.username).first()

            usuario_perfil = candidato or empresa

            if usuario_perfil:
                fs = FileSystemStorage()
                ext = archivo.name.split('.')[-1]

                # Asignamos un prefijo para que no choquen IDs iguales de tablas distintas
                prefijo = "candidato" if candidato else "empresa"
                nombre_archivo = f"perfil_{prefijo}_{user.id}.{ext}"

                if fs.exists(nombre_archivo):
                    fs.delete(nombre_archivo)

                saved_name = fs.save(nombre_archivo, archivo)
                foto_url = fs.url(saved_name)

                # Ambos modelos deben tener el campo fotoperfilurl creado en SQL Server
                usuario_perfil.fotoperfilurl = foto_url
                usuario_perfil.save()

                return Response({'foto_url': foto_url}, status=status.HTTP_200_OK)

            return Response({'error': 'Perfil no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("--- ERROR AL SUBIR IMAGEN ---")
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MiPerfilView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # ----------------------------------------------------
        # BLOQUE 1: RESPUESTA PARA CANDIDATOS
        # ----------------------------------------------------
        candidato = Candidatos.objects.filter(correo=user.username).first()
        if candidato:
            serializer = CandidatosSerializer(candidato)
            datos = serializer.data

            if candidato.fotoperfilurl:
                timestamp = int(datetime.datetime.now().timestamp())
                datos['foto_url'] = f"{candidato.fotoperfilurl}?t={timestamp}"
            else:
                datos['foto_url'] = None

            # 👇 AGREGAR ESTO: Inyectar datos de ubicación y nombres legibles 👇
            if hasattr(candidato, 'municipioid') and candidato.municipioid:
                datos['municipio_nombre'] = candidato.municipioid.nombre
                if hasattr(candidato.municipioid, 'departamentoid') and candidato.municipioid.departamentoid:
                    datos['departamento_nombre'] = candidato.municipioid.departamentoid.nombre
                    # Extraemos el ID del departamento para que el JS pueda hacer la cascada
                    datos['departamento_id'] = getattr(candidato.municipioid.departamentoid, 'departamentoid',
                                                       getattr(candidato.municipioid.departamentoid, 'id', None))

            if hasattr(candidato, 'generoid') and candidato.generoid:
                datos['genero_nombre'] = candidato.generoid.nombre
            if hasattr(candidato, 'estadocivilid') and candidato.estadocivilid:
                datos['estado_civil_nombre'] = candidato.estadocivilid.nombre
            if hasattr(candidato, 'nacionalidadid') and candidato.nacionalidadid:
                datos['nacionalidad_nombre'] = candidato.nacionalidadid.nombre
            # 👆 FIN DE LO NUEVO 👆

            if candidato.curriculumid:
                datos['titulo'] = candidato.curriculumid.profesion
                datos['nivel_educativo_id'] = candidato.curriculumid.niveleducativoid_id

                try:
                    if candidato.curriculumid.niveleducativoid:
                        datos['nivel_educativo_nombre'] = candidato.curriculumid.niveleducativoid.nombre
                except Exception:
                    datos['nivel_educativo_nombre'] = None

                habilidades_qs = CurriculumHabilidades.objects.filter(curriculumid=candidato.curriculumid)
                datos['habilidades'] = [h.habilidadid_id for h in habilidades_qs]
                datos['habilidades_nombres'] = [h.habilidadid.nombre for h in habilidades_qs if h.habilidadid]

                idiomas_qs = CurriculumIdiomas.objects.filter(curriculumid=candidato.curriculumid)
                datos['idiomas'] = [i.idiomaid_id for i in idiomas_qs]
                datos['idiomas_datos'] = [{'id': getattr(i.idiomaid, 'idiomaid', getattr(i.idiomaid, 'id', None)),
                                           'nombre': i.idiomaid.nombre, 'nivel': i.nivel} for i in idiomas_qs if
                                          i.idiomaid]

                # 👇 AGREGAR ESTAS LÍNEAS PARA EXTRAER EXPERIENCIA Y REFERENCIAS 👇
                experiencias_qs = ExperienciaLaboral.objects.filter(curriculumid=candidato.curriculumid).order_by(
                    '-fechainicio')
                datos['experiencias'] = [{
                    'experienciaid': getattr(exp, 'experienciaid', getattr(exp, 'id', None)),
                    'cargo': exp.cargo,
                    'empresa': exp.empresa,
                    'fechainicio': exp.fechainicio,
                    'fechafin': exp.fechafin,
                    'descripcion': exp.descripcion
                } for exp in experiencias_qs]

                referencias_qs = Referencias.objects.filter(curriculumid=candidato.curriculumid)
                datos['referencias'] = [{
                    'referenciaid': getattr(ref, 'referenciaid', getattr(ref, 'id', None)),
                    'nombrecontacto': ref.nombrecontacto,
                    'cargo': ref.cargo,
                    'empresa': ref.empresa,
                    'telefono': ref.telefono,
                    'correo': ref.correo
                } for ref in referencias_qs]
                # 👆 FIN DE LO NUEVO 👆

            return Response({'tipo': 'candidato', 'datos': datos})

        # ----------------------------------------------------
        # BLOQUE 2: RESPUESTA PARA EMPRESAS
        # ----------------------------------------------------
        try:
            empresa = Empresas.objects.filter(correo=user.username).first()
            if empresa:
                serializer = EmpresasSerializer(empresa)
                datos = serializer.data

                # 1. Foto anti-caché segura
                if hasattr(empresa, 'fotoperfilurl') and empresa.fotoperfilurl:
                    timestamp = int(datetime.datetime.now().timestamp())
                    datos['foto_url'] = f"{empresa.fotoperfilurl}?t={timestamp}"
                else:
                    datos['foto_url'] = None

                # 2. Enriquecer con nombres legibles (con validación de seguridad)
                datos['sector_nombre'] = empresa.sectorid.nombre if hasattr(empresa,
                                                                            'sectorid') and empresa.sectorid else None
                datos['tipo_empresa_nombre'] = empresa.tipoempresaid.nombre if hasattr(empresa,
                                                                                       'tipoempresaid') and empresa.tipoempresaid else None

                if hasattr(empresa, 'municipioid') and empresa.municipioid:
                    datos['municipio_nombre'] = empresa.municipioid.nombre
                    if hasattr(empresa.municipioid, 'departamentoid') and empresa.municipioid.departamentoid:
                        datos['departamento_nombre'] = empresa.municipioid.departamentoid.nombre
                        # ID para preseleccionar en el modal de edición
                        datos['departamento_id'] = getattr(empresa.municipioid.departamentoid, 'departamentoid', None)
                else:
                    datos['municipio_nombre'] = None

                return Response({'tipo': 'empresa', 'datos': datos})
        except Exception as e:
            print("--- ERROR AL CARGAR DATOS DE LA EMPRESA ---")
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'error': 'Perfil no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        user = request.user
        data = request.data

        # Actualizar si es candidato
        candidato = Candidatos.objects.filter(correo=user.username).first()
        if candidato:
            serializer = CandidatosSerializer(candidato, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()

                if candidato.curriculumid:
                    curriculum = candidato.curriculumid

                    if 'titulo' in data:
                        curriculum.profesion = data['titulo']

                    if 'nivel_educativo_id' in data and data['nivel_educativo_id']:
                        curriculum.niveleducativoid_id = data['nivel_educativo_id']

                    curriculum.save()

                    if 'habilidades' in data and isinstance(data['habilidades'], list):
                        CurriculumHabilidades.objects.filter(curriculumid=curriculum).delete()
                        for hab_id in data['habilidades']:
                            CurriculumHabilidades.objects.create(
                                curriculumid=curriculum,
                                habilidadid_id=hab_id
                            )

                    if 'idiomas' in data and isinstance(data['idiomas'], list):
                        CurriculumIdiomas.objects.filter(curriculumid=curriculum).delete()
                        for idioma_obj in data['idiomas']:
                            # Verificamos si viene como objeto (con nivel) o solo el número
                            if isinstance(idioma_obj, dict):
                                i_id = idioma_obj.get('id')
                                i_nivel = idioma_obj.get('nivel', 'Básico')
                            else:
                                i_id = idioma_obj
                                i_nivel = 'Básico'

                            if i_id:
                                CurriculumIdiomas.objects.create(
                                    curriculumid=curriculum,
                                    idiomaid_id=i_id,
                                    nivel=i_nivel
                                )

                return Response({'mensaje': '¡Perfil actualizado exitosamente!'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Actualizar si es empresa
        empresa = Empresas.objects.filter(correo=user.username).first()
        if empresa:
            serializer = EmpresasSerializer(empresa, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'mensaje': '¡Perfil actualizado exitosamente!'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Perfil no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        user = request.user
        try:
            # Borrado lógico: Desactivamos al usuario de Django Auth.
            # Esto impide que pueda volver a iniciar sesión sin borrar sus datos físicos (mantiene el DW intacto).
            user.is_active = False
            user.save()
            return Response({'mensaje': 'Cuenta desactivada exitosamente.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegistroUsuarioView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        data = request.data
        tipo = data.get('tipo')

        email = data.get('email')
        password = data.get('password')

        # Nuevos campos del frontend
        nombre_recibido = data.get('nombre', '').strip()
        apellido_recibido = data.get('apellido', '').strip()

        username = email

        if not email or not password:
            return Response({'error': 'El correo y la contraseña son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Ya existe una cuenta con este correo electrónico'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Crear el usuario en el sistema de autenticación de Django
            user = User.objects.create_user(username=username, email=email, password=password)

            # Obtener registros por defecto para que SQL Server no arroje error por NOT NULL
            muni_defecto = Municipios.objects.first()

            if tipo == 'candidato':
                genero_defecto = CatGeneros.objects.first()
                estado_c_defecto = CatEstadosCiviles.objects.first()
                nac_defecto = CatNacionalidades.objects.first()
                nivel_defecto = CatNivelesEducativos.objects.first()

                cv_nuevo = Curriculum.objects.create(profesion="Profesional en búsqueda de oportunidades",
                                                     niveleducativoid=nivel_defecto)

                Candidatos.objects.create(
                    correo=email,
                    nombre=nombre_recibido if nombre_recibido else "Pendiente",
                    apellido=apellido_recibido if apellido_recibido else "Pendiente",
                    fechanacimiento=datetime.date(2000, 1, 1),
                    generoid=genero_defecto,
                    estadocivilid=estado_c_defecto,
                    nacionalidadid=nac_defecto,
                    municipioid=muni_defecto,
                    curriculumid=cv_nuevo
                )
            elif tipo == 'empresa':
                sector_defecto = CatSectores.objects.first()
                tipo_emp_defecto = CatTiposEmpresa.objects.first()

                Empresas.objects.create(
                    correo=email,
                    nombreempresa=nombre_recibido if nombre_recibido else "Empresa Pendiente",
                    sectorid=sector_defecto,
                    tipoempresaid=tipo_emp_defecto,
                    municipioid=muni_defecto
                )
            else:
                raise Exception("Tipo de usuario no válido")

            return Response({'mensaje': '¡Registro exitoso!'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Si algo falla (ej. llaves foráneas), revierte toda la transacción (borra el User también)
            transaction.set_rollback(True)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


def home(request):
    return HttpResponse("Bienvenido a la API de ImpulsoNica 🚀")


# =========================================================
# VISTAS DE CATÁLOGOS
# =========================================================
class DepartamentosViewSet(viewsets.ModelViewSet):
    queryset = Departamentos.objects.all()
    serializer_class = DepartamentosSerializer
    permission_classes = [AllowAny]


class MunicipiosViewSet(viewsets.ModelViewSet):
    queryset = Municipios.objects.all()
    serializer_class = MunicipiosSerializer
    filterset_fields = ['departamentoid']
    permission_classes = [AllowAny]


class CatSectoresViewSet(viewsets.ModelViewSet):
    queryset = CatSectores.objects.all()
    serializer_class = CatSectoresSerializer
    permission_classes = [AllowAny]


class CatTiposEmpresaViewSet(viewsets.ModelViewSet):
    queryset = CatTiposEmpresa.objects.all()
    serializer_class = CatTiposEmpresaSerializer
    permission_classes = [AllowAny]


class CatGenerosViewSet(viewsets.ModelViewSet):
    queryset = CatGeneros.objects.all()
    serializer_class = CatGenerosSerializer


class CatEstadosCivilesViewSet(viewsets.ModelViewSet):
    queryset = CatEstadosCiviles.objects.all()
    serializer_class = CatEstadosCivilesSerializer


class CatNacionalidadesViewSet(viewsets.ReadOnlyModelViewSet):
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


# =========================================================
# VISTAS PRINCIPALES
# =========================================================
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
    queryset = Empleos.objects.all().order_by('-empleoid')
    serializer_class = EmpleosSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['empresaid', 'empresaid__sectorid', 'empresaid__municipioid']


class VacantesViewSet(viewsets.ModelViewSet):
    queryset = Vacantes.objects.all()
    serializer_class = VacantesSerializer


class PostulacionesViewSet(viewsets.ModelViewSet):
    queryset = Postulaciones.objects.all()
    serializer_class = PostulacionesSerializer
    filterset_fields = ['empleoid', 'candidatoid']


# =========================================================
# VISTAS DEPENDIENTES / INTERSECCIÓN
# =========================================================
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
    permission_classes = [AllowAny]
    filterset_fields = ['empleoid']