from django.db import models


class DimEmpleo(models.Model):
    empleokey = models.AutoField(db_column='EmpleoKey', primary_key=True)
    empleoid_natural = models.IntegerField(db_column='EmpleoId_Natural')
    nombreempleo = models.CharField(db_column='NombreEmpleo', max_length=150)
    modalidad = models.CharField(db_column='Modalidad', max_length=100)
    tipoempleo = models.CharField(db_column='TipoEmpleo', max_length=100)

    class Meta:
        managed = False
        db_table = 'Dim_Empleo'


class DimEmpresa(models.Model):
    empresakey = models.AutoField(db_column='EmpresaKey', primary_key=True)
    empresaid_natural = models.IntegerField(db_column='EmpresaId_Natural')
    nombreempresa = models.CharField(db_column='NombreEmpresa', max_length=150)
    tipoempresa = models.CharField(db_column='TipoEmpresa', max_length=100)

    class Meta:
        managed = False
        db_table = 'Dim_Empresa'


class DimSector(models.Model):
    sectorkey = models.AutoField(db_column='SectorKey', primary_key=True)
    nombresector = models.CharField(db_column='NombreSector', max_length=100)

    class Meta:
        managed = False
        db_table = 'Dim_Sector'


class DimTiempo(models.Model):
    tiempokey = models.IntegerField(db_column='TiempoKey', primary_key=True)
    fecha = models.DateField(db_column='Fecha')
    anio = models.IntegerField(db_column='Anio', blank=True, null=True)
    trimestre = models.IntegerField(db_column='Trimestre', blank=True, null=True)
    mes = models.IntegerField(db_column='Mes', blank=True, null=True)
    nombremes = models.CharField(db_column='NombreMes', max_length=20, blank=True, null=True)
    dia = models.IntegerField(db_column='Dia', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dim_Tiempo'


class DimUbicacion(models.Model):
    ubicacionkey = models.AutoField(db_column='UbicacionKey', primary_key=True)
    departamento = models.CharField(db_column='Departamento', max_length=100)
    municipio = models.CharField(db_column='Municipio', max_length=100)

    class Meta:
        managed = False
        db_table = 'Dim_Ubicacion'


class FactOfertaslaborales(models.Model):
    ofertaid = models.AutoField(db_column='OfertaId', primary_key=True)
    tiempopublicacionkey = models.ForeignKey(DimTiempo, models.DO_NOTHING, db_column='TiempoPublicacionKey',
                                             related_name='fact_publicacion')
    tiempocierrekey = models.ForeignKey(DimTiempo, models.DO_NOTHING, db_column='TiempoCierreKey', blank=True,
                                        null=True, related_name='fact_cierre')
    ubicacionkey = models.ForeignKey(DimUbicacion, models.DO_NOTHING, db_column='UbicacionKey')
    sectorkey = models.ForeignKey(DimSector, models.DO_NOTHING, db_column='SectorKey')
    empresakey = models.ForeignKey(DimEmpresa, models.DO_NOTHING, db_column='EmpresaKey')
    empleokey = models.ForeignKey(DimEmpleo, models.DO_NOTHING, db_column='EmpleoKey')

    cantidadvacantes = models.IntegerField(db_column='CantidadVacantes')
    salarioofrecido = models.DecimalField(db_column='SalarioOfrecido', max_digits=10, decimal_places=2, blank=True,
                                          null=True)
    diasabierta = models.IntegerField(db_column='DiasAbierta', blank=True, null=True)
    totalpostulacionesrecibidas = models.IntegerField(db_column='TotalPostulacionesRecibidas', blank=True, null=True)
    cantidadrequisitos = models.IntegerField(db_column='CantidadRequisitos', blank=True, null=True)
    fechacargadw = models.DateTimeField(db_column='FechaCargaDW', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Fact_OfertasLaborales'