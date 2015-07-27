====================
django-database-view
====================

A simple pluggable application that allows to work with database views.

Quick start
-----------

1. Add "dbview" to your INSTALLED_APPS settings like this::

   INSTALLED_APPS = (
     ...
     'dbview',
   )

2. In your models.py create classes which extend dbview.models.DbView
like this::

.. code-block:: python
   :caption: models.py
   :name: models.py

   ...
   from dbview.models import DbView

   ...
   class MyView(DbView):
      fieldA = models.OneToOneField(modelA, primary_key=True, db_column='fielda__id')
      fieldB = models.IntegerField(blank=True, null=True, db_column='fieldb')

      @classmethod
      dev view(klass):
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

3. Then create a migration point for your view generation, edit that migration
and modify it to match:
