"""HELPERS to create SQL VIEW
https://github.com/manuelnaranjo/django-database-view updated helper
(issue created. fork with solve created: https://github.com/Seriouskosk/django-database-view)
For Create/Drop SQL VIEW you must do:
1) set True in db_route.py in allow_migrate
2) manage.py makemigrations
3) set False in db_route.py in allow_migrate
4) manage.py migrate"""
import logging
import types

from django.apps import apps
from django.db import migrations


class SQLViewsMixin:
    """Mixin for work with SQL VIEWS"""

    @staticmethod
    def _drop_view(model, schema_editor):
        """DROP VIEW from DB"""
        if hasattr(model, "drop_view_sql"):
            sql_template = model.drop_view_sql
        else:
            sql_template = "DROP VIEW IF EXISTS %(table)s"
        args = {
            "table": schema_editor.quote_name(model._meta.db_table),
        }
        sql = sql_template % args
        schema_editor.execute(sql, None)

    def get_model_instance(self, submodules):
        """get model recursive"""
        attrs = [attr for attr in dir(submodules) if '_' not in attr]
        for attr in attrs:
            value = getattr(submodules, attr)
            if self.name in str(value):
                return value
            if isinstance(value, types.ModuleType):
                return self.get_model_instance(value)
        return None

    def _get_model(self, app_label, fake_model):
        """
        :fake_model: loaded from code
        :return model: loaded from App"""
        models = apps.get_app_config(app_label).models_module

        if hasattr(models, self.name):
            return getattr(models, self.name)

        sub_model = self.get_model_instance(models)
        if sub_model:
            return sub_model

        logging.warning("Using fake model, this may fail with inherited views")
        return fake_model

    def _create_standard_view(self, model, schema_editor):
        """CREATE VIEW in DB"""
        sql_template = "CREATE VIEW %(table)s AS %(definition)s"
        qs = str(model.view())
        args = {
            "table": schema_editor.quote_name(model._meta.db_table),
            "definition": qs,
        }
        sql = sql_template % args
        self._create_view_from_raw_sql(sql, schema_editor)

    @staticmethod
    def _create_view_from_raw_sql(sql, schema_editor):
        """Execute sql"""
        schema_editor.execute(sql, None)

    def create_view(self, app_label, schema_editor, state):
        """create view method"""
        fake_model = state.apps.get_model(app_label, self.name)
        model = self._get_model(app_label, fake_model)

        self._drop_view(model, schema_editor)

        if hasattr(model, "view"):
            self._create_standard_view(model, schema_editor)
        elif hasattr(model, "get_view_str"):
            self._create_view_from_raw_sql(model.get_view_str(), schema_editor)
        else:
            raise Exception(f"{model} has neither view nor get_view_str")

    def drop_view(self, app_label, schema_editor, state):
        """Drop view method"""
        fake_model = state.apps.get_model(app_label, self.name)
        model = self._get_model(app_label, fake_model)
        self._drop_view(model, schema_editor)


class DropView(migrations.DeleteModel, SQLViewsMixin):
    """Drop SQL View migrations"""

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        """Forwards DROP VIEW from DB"""
        self.drop_view(app_label, schema_editor, to_state)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        """Backwards CREATE VIEW from DB"""
        self.create_view(app_label, schema_editor, from_state)


class CreateView(migrations.CreateModel, SQLViewsMixin):
    """Create SQL View migrations"""

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        """Forwards CREATE VIEW from DB"""
        self.create_view(app_label, schema_editor, to_state)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        """Backwards DROP VIEW from DB"""
        self.drop_view(app_label, schema_editor, from_state)
