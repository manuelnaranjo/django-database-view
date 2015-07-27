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
    def view(klass):
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
