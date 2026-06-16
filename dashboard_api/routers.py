class DWRouter:
    """
    Un enrutador para controlar todas las operaciones de base de datos
    en los modelos de la aplicación dashboard_api.
    """
    route_app_labels = {'dashboard_api'}

    def db_for_read(self, model, **hints):
        """Apunta las operaciones de lectura a la base de datos DW."""
        if model._meta.app_label in self.route_app_labels:
            return 'dw_impulsonica'
        return None

    def db_for_write(self, model, **hints):
        """Apunta las operaciones de escritura a la base de datos DW."""
        if model._meta.app_label in self.route_app_labels:
            return 'dw_impulsonica'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Permite relaciones si ambos objetos están en la app dashboard_api."""
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Asegura que la app dashboard_api solo aparezca en la base de datos DW."""
        if app_label in self.route_app_labels:
            return db == 'dw_impulsonica'
        return None