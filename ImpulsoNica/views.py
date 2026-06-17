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
from .models import Candidatos, Empresas, Administradores
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
            # 👇 BÚSQUEDA ROBUSTA ABSOLUTA PARA TODOS LOS ROLES 👇
            candidato = Candidatos.objects.filter(correo=user.username).first() or Candidatos.objects.filter(
                correo=user.email).first()
            empresa = Empresas.objects.filter(correo=user.username).first() or Empresas.objects.filter(
                correo=user.email).first()

            admin = Administradores.objects.filter(usuario=user.username).first()
            if not admin:
                admin = Administradores.objects.filter(correo=user.username).first()
            if not admin and user.email:
                admin = Administradores.objects.filter(correo=user.email).first()

            usuario_perfil = candidato or empresa or admin

            if usuario_perfil:
                fs = FileSystemStorage()
                ext = archivo.name.split('.')[-1]

                # Asignamos un prefijo para que no choquen IDs iguales de tablas distintas
                if candidato:
                    prefijo = "candidato"
                elif empresa:
                    prefijo = "empresa"
                else:
                    prefijo = "admin"

                nombre_archivo = f"perfil_{prefijo}_{user.id}.{ext}"

                if fs.exists(nombre_archivo):
                    fs.delete(nombre_archivo)

                saved_name = fs.save(nombre_archivo, archivo)
                foto_url = fs.url(saved_name)

                # Todos los modelos (Candidatos, Empresas, Administradores) ahora tienen fotoperfilurl
                usuario_perfil.fotoperfilurl = foto_url
                usuario_perfil.save()

                return Response({'foto_url': foto_url}, status=status.HTTP_200_OK)

            return Response({'error': 'Perfil no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("--- ERROR AL SUBIR IMAGEN ---")
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MiPerfilView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # ----------------------------------------------------
        # BLOQUE 0: RESPUESTA PARA ADMINISTRADORES
        # ----------------------------------------------------
        if user.is_superuser or Administradores.objects.filter(
                correo=user.email).exists() or Administradores.objects.filter(usuario=user.username).exists():
            admin_db = Administradores.objects.filter(correo=user.email).first() or Administradores.objects.filter(
                usuario=user.username).first()

            # Verificamos si el admin ya subió una foto a la BD, si no, usa el avatar por defecto
            foto_url = '/imgn/cv.png'
            if admin_db and hasattr(admin_db, 'fotoperfilurl') and admin_db.fotoperfilurl:
                timestamp = int(datetime.datetime.now().timestamp())
                foto_url = f"{admin_db.fotoperfilurl}?t={timestamp}"

            return Response({
                'tipo': 'admin',
                'datos': {
                    'nombre': admin_db.nombre if admin_db else 'Super',
                    'apellido': admin_db.apellido if admin_db else 'Administrador',
                    'correo': admin_db.correo if admin_db else (user.email or user.username),
                    'foto_url': foto_url
                }
            }, status=status.HTTP_200_OK)

        # ----------------------------------------------------
        # BLOQUE 1: RESPUESTA PARA CANDIDATOS
        # ----------------------------------------------------
        candidato = Candidatos.objects.filter(correo=user.username).first() or Candidatos.objects.filter(
            correo=user.email).first()
        if candidato:
            serializer = CandidatosSerializer(candidato)
            datos = serializer.data

            if candidato.fotoperfilurl:
                timestamp = int(datetime.datetime.now().timestamp())
                datos['foto_url'] = f"{candidato.fotoperfilurl}?t={timestamp}"
            else:
                datos['foto_url'] = None

            if hasattr(candidato, 'municipioid') and candidato.municipioid:
                datos['municipio_nombre'] = candidato.municipioid.nombre
                if hasattr(candidato.municipioid, 'departamentoid') and candidato.municipioid.departamentoid:
                    datos['departamento_nombre'] = candidato.municipioid.departamentoid.nombre
                    datos['departamento_id'] = getattr(candidato.municipioid.departamentoid, 'departamentoid',
                                                       getattr(candidato.municipioid.departamentoid, 'id', None))

            if hasattr(candidato, 'generoid') and candidato.generoid:
                datos['genero_nombre'] = candidato.generoid.nombre
            if hasattr(candidato, 'estadocivilid') and candidato.estadocivilid:
                datos['estado_civil_nombre'] = candidato.estadocivilid.nombre
            if hasattr(candidato, 'nacionalidadid') and candidato.nacionalidadid:
                datos['nacionalidad_nombre'] = candidato.nacionalidadid.nombre

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

            return Response({'tipo': 'candidato', 'datos': datos})

        # ----------------------------------------------------
        # BLOQUE 2: RESPUESTA PARA EMPRESAS
        # ----------------------------------------------------
        try:
            empresa = Empresas.objects.filter(correo=user.username).first() or Empresas.objects.filter(
                correo=user.email).first()
            if empresa:
                serializer = EmpresasSerializer(empresa)
                datos = serializer.data

                if hasattr(empresa, 'fotoperfilurl') and empresa.fotoperfilurl:
                    timestamp = int(datetime.datetime.now().timestamp())
                    datos['foto_url'] = f"{empresa.fotoperfilurl}?t={timestamp}"
                else:
                    datos['foto_url'] = None

                datos['sector_nombre'] = empresa.sectorid.nombre if hasattr(empresa,
                                                                            'sectorid') and empresa.sectorid else None
                datos['tipo_empresa_nombre'] = empresa.tipoempresaid.nombre if hasattr(empresa,
                                                                                       'tipoempresaid') and empresa.tipoempresaid else None

                if hasattr(empresa, 'municipioid') and empresa.municipioid:
                    datos['municipio_nombre'] = empresa.municipioid.nombre
                    if hasattr(empresa.municipioid, 'departamentoid') and empresa.municipioid.departamentoid:
                        datos['departamento_nombre'] = empresa.municipioid.departamentoid.nombre
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

        # 1. Intentar actualizar si es Candidato
        candidato = Candidatos.objects.filter(correo=user.username).first() or Candidatos.objects.filter(
            correo=user.email).first()
        if candidato:
            serializer = CandidatosSerializer(candidato, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()

                # Guardar habilidades e idiomas si es candidato
                if 'habilidades' in data:
                    CurriculumHabilidades.objects.filter(curriculumid=candidato.curriculumid).delete()
                    for hab_id in data['habilidades']:
                        CurriculumHabilidades.objects.create(curriculumid=candidato.curriculumid, habilidadid_id=hab_id)
                if 'idiomas' in data:
                    CurriculumIdiomas.objects.filter(curriculumid=candidato.curriculumid).delete()
                    for idioma in data['idiomas']:
                        CurriculumIdiomas.objects.create(curriculumid=candidato.curriculumid, idiomaid_id=idioma['id'],
                                                         nivel=idioma['nivel'])

                return Response({'mensaje': '¡Perfil actualizado exitosamente!'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 2. Intentar actualizar si es Empresa
        empresa = Empresas.objects.filter(correo=user.username).first() or Empresas.objects.filter(
            correo=user.email).first()
        if empresa:
            serializer = EmpresasSerializer(empresa, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'mensaje': '¡Perfil de empresa actualizado exitosamente!'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 3. Búsqueda total para el Administrador
        admin = Administradores.objects.filter(usuario=user.username).first()
        if not admin:
            admin = Administradores.objects.filter(correo=user.username).first()
        if not admin and user.email:
            admin = Administradores.objects.filter(correo=user.email).first()

        if admin:
            serializer = AdministradoresSerializer(admin, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'mensaje': '¡Perfil de administrador actualizado exitosamente!'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Si el usuario logueado no existe en ninguna de las 3 tablas, devuelve 404
        return Response({'error': 'Perfil no encontrado en la base de datos para actualizar.'},
                        status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        user = request.user
        try:
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

        nombre_recibido = data.get('nombre', '').strip()
        apellido_recibido = data.get('apellido', '').strip()

        username = email

        if not email or not password:
            return Response({'error': 'El correo y la contraseña son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Ya existe una cuenta con este correo electrónico'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
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