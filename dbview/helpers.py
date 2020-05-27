from django.db import migrations
from django.apps import apps


class CreateView(migrations.CreateModel):
    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        model = to_state.apps.get_model(app_label, self.name)

        if not self.allow_migrate_model(schema_editor.connection.alias, model):
            raise
        models = apps.get_app_config(app_label).models_module
        model = getattr(models, self.name)

        sql = 'DROP VIEW IF EXISTS %(table)s;'

        args = {
            'table' : schema_editor.quote_name(model._meta.db_table),
        }

        sql = sql % args

        schema_editor.execute(sql, None)

        sql = 'CREATE VIEW %(table)s AS %(definition)s'

        if hasattr(model, 'view'):
            qs = str(model.view())
        else:
            raise Exception('Your view needs to define either view or ' +
                            'get_view_str')

        args['definition'] = qs

        sql = sql % args

        schema_editor.execute(sql, None)

    def database_backwards(self, app_label, schema_editor, from_state, to):
        model = from_state.apps.get_model(app_label, self.name)
        sql = 'DROP VIEW IF EXISTS %s' % \
              schema_editor.quote_name(model._meta.db_table)
        schema_editor.execute(sql, None)
