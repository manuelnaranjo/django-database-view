====================
django-database-view
====================

A simple pluggable application that allows to work with database views.

So far only MySQL is supported as backend, but more could be added if necessary.

Quick start
-----------

1. Add "dbview" to your INSTALLED_APPS settings like this::

   INSTALLED_APPS = (
     ...
     'dbview',
   )


2. In your models.py create classes which extend dbview.models.DbView
like this::

.. literalinclude:: example.py
   :languague: python
   :emphasize-lines: 9-26
   :linenos:

3. Then create a migration point for your view generation, edit that migration
and modify it, add: `from dbview.helpers import CreateView` and replace the line
the call to migrations.CreateModel with CreateView.


4. Migrate your database and start using your database views.
