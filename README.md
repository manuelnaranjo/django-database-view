# django-database-view

A simple pluggable application that allows to work with database views.

So far only MySQL is supported as backend, but more could be added if necessary.

## Quick start

1. In your models.py create classes which extend dbview.DbView like this:

    ```python

    from django.db import models
    from dbview.models import DbView

    class ModelA(models.Model):
        fielda = models.CharField()
        fieldc = models.IntegerField()

    class MyView(DbView):
        fieldA = models.OneToOneField(ModelA, primary_key=True,
            db_column='fielda__id')
        fieldB = models.IntegerField(blank=True, null=True, db_column='fieldb')

        @classmethod
        def view(cls):
            '''
            This method returns the SQL string that creates the view, in this
            example fieldB is the result of annotating another column
            '''
            qs = modelA.objects.all().\
                 annotate(fieldb=models.Sum('fieldc')) .\
                 annotate(fielda__id=models.F('pk')) .\
                 order_by('fielda__id') .\
                 values('fielda__id', 'fieldb')
            return str(qs.query)
    ```

Alternatively `get_view_str` method could be used to write a custom SQL:

    ```python

    class MyView(DbView):

        # ...

        @classmethod
        def get_view_str(cls):
            return """
            CREATE VIEW my_view AS (
                SELECT ...
            )
            """
    ```

2. Then create a migration point for your view generation, edit that migration
and modify it, add: `from dbview.helpers import CreateView` and replace the
line the call to `migrations.CreateModel` with `CreateView`.

3. Migrate your database and start using your database views.
