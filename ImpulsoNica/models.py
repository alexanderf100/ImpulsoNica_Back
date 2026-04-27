from django.db import models

# --------------------------------------------------------------
# 1. TABLAS CATÁLOGO (DOMINIOS)
# --------------------------------------------------------------

class Departamentos(models.Model):
    departamentoid = models.AutoField(primary_key=True, db_column='DepartamentoId')
    nombre = models.CharField(max_length=100, unique=True, db_column='Nombre')

    class Meta:
        managed = False
        db_table = 'Departamentos'

class Municipios(models.Model):
    municipioid = models.AutoField(primary_key=True, db_column='MunicipioId')
    nombre = models.CharField(max_length=100, db_column='Nombre')
    departamentoid = models.ForeignKey(Departamentos, models.DO_NOTHING, db_column='DepartamentoId')

    class Meta:
        managed = False
        db_table = 'Municipios'

class CatSectores(models.Model):
    sectorid = models.AutoField(primary_key=True, db_column='SectorId')
    nombre = models.CharField(max_length=100, unique=True, db_column='Nombre')

    class Meta:
        managed = False
        db_table = 'Cat_Sectores'

class CatTiposEmpresa(models.Model):
    tipoempresaid = models.AutoField(primary_key=True, db_column='TipoEmpresaId')
    nombre = models.CharField(max_length=100, unique=True, db_column='Nombre')

    class Meta:
        managed = False
        db_table = 'Cat_TiposEmpresa'

class CatGeneros(models.Model):
    generoid = models.AutoField(primary_key=True, db_column='GeneroId')
    nombre = models.CharField(max_length=50, unique=True, db_column='Nombre')

    class Meta:
        managed = False
        db_table = 'Cat_Generos'

class CatEstadosCiviles(models.Model):
    estadocivilid = models.AutoField(primary_key=True, db_column='EstadoCivilId')
    nombre = models.CharField(max_length=50, unique=True, db_column='Nombre')

    class Meta:
        managed = False
        db_table = 'Cat_EstadosCiviles'

class CatNacionalidades(models.Model):
    nacionalidadid = models.AutoField(primary_key=True, db_column='NacionalidadId')
    nombre = models.CharField(max_length=100, unique=True, db_column='Nombre')

    class Meta:
        managed = False
        db_table = 'Cat_Nacionalidades'

class CatNivelesEducativos(models.Model):
    niveleducativoid = models.AutoField(primary_key=True, db_column='NivelEducativoId')
    nombre = models.CharField(max_length=100, unique=True, db_column='Nombre')

    class Meta:
        managed = False
        db_table = 'Cat_NivelesEducativos'

class CatIdiomas(models.Model):
    idiomaid = models.AutoField(primary_key=True, db_column='IdiomaId')
    nombre = models.CharField(max_length=100, unique=True, db_column='Nombre')

    class Meta:
        managed = False
        db_table = 'Cat_Idiomas'

class CatHabilidades(models.Model):
    habilidadid = models.AutoField(primary_key=True, db_column='HabilidadId')
    nombre = models.CharField(max_length=100, unique=True, db_column='Nombre')

    class Meta:
        managed = False
        db_table = 'Cat_Habilidades'

class CatTiposEmpleo(models.Model):
    tipoempleoid = models.AutoField(primary_key=True, db_column='TipoEmpleoId')
    nombre = models.CharField(max_length=100, unique=True, db_column='Nombre')

    class Meta:
        managed = False
        db_table = 'Cat_TiposEmpleo'

class CatModalidades(models.Model):
    modalidadid = models.AutoField(primary_key=True, db_column='ModalidadId')
    nombre = models.CharField(max_length=100, unique=True, db_column='Nombre')

    class Meta:
        managed = False
        db_table = 'Cat_Modalidades'

class CatEstados(models.Model):
    estadoid = models.AutoField(primary_key=True, db_column='EstadoId')
    nombre = models.CharField(max_length=50, db_column='Nombre')
    contexto = models.CharField(max_length=50, db_column='Contexto')

    class Meta:
        managed = False
        db_table = 'Cat_Estados'
        unique_together = (('nombre', 'contexto'),)

# --------------------------------------------------------------
# 2. TABLAS PRINCIPALES
# --------------------------------------------------------------

class Administradores(models.Model):
    administradorid = models.AutoField(primary_key=True, db_column='AdministradorId')
    nombre = models.CharField(max_length=100, db_column='Nombre')
    apellido = models.CharField(max_length=100, db_column='Apellido')
    correo = models.CharField(max_length=150, unique=True, db_column='Correo')
    telefono = models.CharField(max_length=20, blank=True, null=True, db_column='Telefono')
    usuario = models.CharField(max_length=50, unique=True, db_column='Usuario')
    contrasena = models.CharField(max_length=255, db_column='Contrasena')
    fecharegistro = models.DateTimeField(blank=True, null=True, db_column='FechaRegistro')
    municipioid = models.ForeignKey(Municipios, models.DO_NOTHING, db_column='MunicipioId')

    class Meta:
        managed = False
        db_table = 'Administradores'

class Empresas(models.Model):
    empresaid = models.AutoField(primary_key=True, db_column='EmpresaId')
    nombreempresa = models.CharField(max_length=150, db_column='NombreEmpresa')
    correo = models.CharField(max_length=150, unique=True, db_column='Correo')
    telefono = models.CharField(max_length=20, blank=True, null=True, db_column='Telefono')
    direccion = models.CharField(max_length=255, blank=True, null=True, db_column='Direccion')
    sectorid = models.ForeignKey(CatSectores, models.DO_NOTHING, db_column='SectorId')
    tipoempresaid = models.ForeignKey(CatTiposEmpresa, models.DO_NOTHING, db_column='TipoEmpresaId')
    fecharegistro = models.DateTimeField(blank=True, null=True, db_column='FechaRegistro')
    municipioid = models.ForeignKey(Municipios, models.DO_NOTHING, db_column='MunicipioId')

    class Meta:
        managed = False
        db_table = 'Empresas'

class Curriculum(models.Model):
    curriculumid = models.AutoField(primary_key=True, db_column='CurriculumId')
    profesion = models.CharField(max_length=100, db_column='Profesion')
    niveleducativoid = models.ForeignKey(CatNivelesEducativos, models.DO_NOTHING, db_column='NivelEducativoId')
    fecharegistro = models.DateTimeField(blank=True, null=True, db_column='FechaRegistro')

    class Meta:
        managed = False
        db_table = 'Curriculum'

class Candidatos(models.Model):
    candidatoid = models.AutoField(primary_key=True, db_column='CandidatoId')
    nombre = models.CharField(max_length=100, db_column='Nombre')
    apellido = models.CharField(max_length=100, db_column='Apellido')
    correo = models.CharField(max_length=150, unique=True, db_column='Correo')
    telefono = models.CharField(max_length=20, blank=True, null=True, db_column='Telefono')
    direccion = models.CharField(max_length=255, blank=True, null=True, db_column='Direccion')
    fechanacimiento = models.DateField(db_column='FechaNacimiento')
    generoid = models.ForeignKey(CatGeneros, models.DO_NOTHING, db_column='GeneroId')
    estadocivilid = models.ForeignKey(CatEstadosCiviles, models.DO_NOTHING, db_column='EstadoCivilId')
    nacionalidadid = models.ForeignKey(CatNacionalidades, models.DO_NOTHING, db_column='NacionalidadId')
    fecharegistro = models.DateTimeField(blank=True, null=True, db_column='FechaRegistro')
    municipioid = models.ForeignKey(Municipios, models.DO_NOTHING, db_column='MunicipioId')
    curriculumid = models.OneToOneField(Curriculum, models.DO_NOTHING, db_column='CurriculumId')

    class Meta:
        managed = False
        db_table = 'Candidatos'

class Empleos(models.Model):
    empleoid = models.AutoField(primary_key=True, db_column='EmpleoId')
    nombreempleo = models.CharField(max_length=150, db_column='NombreEmpleo')
    descripcion = models.CharField(max_length=500, db_column='Descripcion')
    salario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column='Salario')
    tipoempleoid = models.ForeignKey(CatTiposEmpleo, models.DO_NOTHING, db_column='TipoEmpleoId')
    modalidadid = models.ForeignKey(CatModalidades, models.DO_NOTHING, db_column='ModalidadId')
    estadoid = models.ForeignKey(CatEstados, models.DO_NOTHING, db_column='EstadoId')
    fechapublicacion = models.DateTimeField(blank=True, null=True, db_column='FechaPublicacion')
    fechacierre = models.DateTimeField(blank=True, null=True, db_column='FechaCierre')
    empresaid = models.ForeignKey(Empresas, models.DO_NOTHING, db_column='EmpresaId')

    class Meta:
        managed = False
        db_table = 'Empleos'

class Vacantes(models.Model):
    vacanteid = models.AutoField(primary_key=True, db_column='VacanteId')
    empleoid = models.ForeignKey(Empleos, models.DO_NOTHING, db_column='EmpleoId')
    cantidad = models.IntegerField(blank=True, null=True, db_column='Cantidad')
    fechainicio = models.DateTimeField(blank=True, null=True, db_column='FechaInicio')
    fechafin = models.DateTimeField(blank=True, null=True, db_column='FechaFin')
    estadoid = models.ForeignKey(CatEstados, models.DO_NOTHING, db_column='EstadoId')
    observaciones = models.CharField(max_length=500, blank=True, null=True, db_column='Observaciones')

    class Meta:
        managed = False
        db_table = 'Vacantes'

class Postulaciones(models.Model):
    postulacionid = models.AutoField(primary_key=True, db_column='PostulacionId')
    fechapostulacion = models.DateTimeField(blank=True, null=True, db_column='FechaPostulacion')
    estadoid = models.ForeignKey(CatEstados, models.DO_NOTHING, db_column='EstadoId')
    candidatoid = models.ForeignKey(Candidatos, models.DO_NOTHING, db_column='CandidatoId')
    empleoid = models.ForeignKey(Empleos, models.DO_NOTHING, db_column='EmpleoId')

    class Meta:
        managed = False
        db_table = 'Postulaciones'

# --------------------------------------------------------------
# 3. TABLAS DEPENDIENTES Y DE INTERSECCIÓN
# --------------------------------------------------------------

class ExperienciaLaboral(models.Model):
    experienciaid = models.AutoField(primary_key=True, db_column='ExperienciaId')
    curriculumid = models.ForeignKey(Curriculum, models.DO_NOTHING, db_column='CurriculumId')
    empresa = models.CharField(max_length=150, db_column='Empresa')
    cargo = models.CharField(max_length=100, db_column='Cargo')
    fechainicio = models.DateField(db_column='FechaInicio')
    fechafin = models.DateField(blank=True, null=True, db_column='FechaFin')
    descripcion = models.CharField(max_length=500, blank=True, null=True, db_column='Descripcion')

    class Meta:
        managed = False
        db_table = 'ExperienciaLaboral'

class Referencias(models.Model):
    referenciaid = models.AutoField(primary_key=True, db_column='ReferenciaId')
    curriculumid = models.ForeignKey(Curriculum, models.DO_NOTHING, db_column='CurriculumId')
    nombrecontacto = models.CharField(max_length=150, db_column='NombreContacto')
    cargo = models.CharField(max_length=100, blank=True, null=True, db_column='Cargo')
    empresa = models.CharField(max_length=150, blank=True, null=True, db_column='Empresa')
    telefono = models.CharField(max_length=20, db_column='Telefono')
    correo = models.CharField(max_length=150, blank=True, null=True, db_column='Correo')

    class Meta:
        managed = False
        db_table = 'Referencias'

class CurriculumHabilidades(models.Model):
    curriculumid = models.ForeignKey(Curriculum, models.DO_NOTHING, db_column='CurriculumId', primary_key=True)
    habilidadid = models.ForeignKey(CatHabilidades, models.DO_NOTHING, db_column='HabilidadId')

    class Meta:
        managed = False
        db_table = 'Curriculum_Habilidades'
        unique_together = (('curriculumid', 'habilidadid'),)

class CurriculumIdiomas(models.Model):
    curriculumid = models.ForeignKey(Curriculum, models.DO_NOTHING, db_column='CurriculumId', primary_key=True)
    idiomaid = models.ForeignKey(CatIdiomas, models.DO_NOTHING, db_column='IdiomaId')
    nivel = models.CharField(max_length=50, db_column='Nivel')

    class Meta:
        managed = False
        db_table = 'Curriculum_Idiomas'
        unique_together = (('curriculumid', 'idiomaid'),)

class EmpleoRequisitos(models.Model):
    requisitoid = models.AutoField(primary_key=True, db_column='RequisitoId')
    empleoid = models.ForeignKey(Empleos, models.DO_NOTHING, db_column='EmpleoId')
    descripcion = models.CharField(max_length=255, db_column='Descripcion')
    esobligatorio = models.BooleanField(blank=True, null=True, db_column='EsObligatorio')

    class Meta:
        managed = False
        db_table = 'Empleo_Requisitos'