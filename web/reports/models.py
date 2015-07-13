from django.db import models

from reports.util import model_unicode



class Bank(models.Model):
    idrssd = models.PositiveIntegerField(primary_key=True)  


    def __unicode__(self):
        return model_unicode(self, ('idrssd',))



class Report(models.Model):
    bank = models.ForeignKey(Bank, related_name='reports')
    date = models.DateField()
    name = models.CharField(max_length=255)

    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=16)
    zipcode = models.PositiveIntegerField()

    assets = models.PositiveIntegerField()
    deposits = models.PositiveIntegerField()
    liabilities = models.PositiveIntegerField()


    def __unicode__(self):
        return model_unicode(self, (
            'bank', 'date', 'name', 'address', 'city', 'state', 'zipcode',
            'assets', 'deposits', 'liabilities'
        ))
