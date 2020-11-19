import logging

from django.db import migrations
from django.apps import apps


class CreateView(migrations.CreateModel):

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        fake_model = to_state.apps.get_model(app_label, self.name)

        if not self.allow_migrate_model(
                schema_editor.connection.alias, fake_model):
            raise

        model = self._get_model(fake_model, app_label, to_state)

        self._drop_view(fake_model, schema_editor)

        if hasattr(model, 'view'):
            self._create_standard_view(model, schema_editor)
        elif hasattr(model, 'get_view_str'):
            self._create_view_from_raw_sql(model.get_view_str(), schema_editor)
        else:
            raise Exception(f"{model} has neither view nor get_view_str")

    def database_backwards(self, app_label, schema_editor, from_state, to):
        fake_model = from_state.apps.get_model(app_label, self.name)
        self._drop_view(fake_model, schema_editor)

    def _get_model(self, state, app_label, fake_model):
        models = apps.get_app_config(app_label).models_module

        if hasattr(models, self.name):
            return getattr(models, self.name)

        # TODO: recursive search
        for submodule in models.__dict__.values():
            if hasattr(submodule, self.name):
                return getattr(submodule, self.name)

        logging.warning('Using fake model, this may fail with inherited views')
        return fake_model

    def _drop_view(self, model, schema_editor):
        sql_template = 'DROP VIEW IF EXISTS %(table)s CASCADE'
        args = {
            'table': schema_editor.quote_name(model._meta.db_table),
        }
        sql = sql_template % args
        schema_editor.execute(sql, None)

    def _create_standard_view(self, model, schema_editor):
        sql_template = 'CREATE VIEW %(table)s AS %(definition)s'
        qs = str(model.view())
        args = {
            'table': schema_editor.quote_name(model._meta.db_table),
            'definition': qs,
        }
        sql = sql_template % args
        self._create_view_from_raw_sql(sql, schema_editor)

    def _create_view_from_raw_sql(self, sql, schema_editor):
        schema_editor.execute(sql, None)
