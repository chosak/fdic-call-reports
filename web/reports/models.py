from django.db import connection, models

from reports.util import model_unicode



class ReportManager(models.Manager):
    def most_recent(self, offset=None, limit=None):
        inner_query = '''
SELECT
    idrssd,
    max(date) max_date
FROM
    reports_report
GROUP BY
    idrssd
ORDER BY
    name ASC
        '''.strip()

        if limit:
            inner_query += ' LIMIT {}'.format(int(limit))
        if offset:
            inner_query += ' OFFSET {}'.format(int(offset))

        query = '''
SELECT
    *
FROM
    reports_report r1
INNER JOIN (
    {inner_query}
) r2
ON
    r1.idrssd = r2.idrssd AND
    r1.date = r2.max_date
        '''.strip().format(
            inner_query=inner_query
        )

        return self.model.objects.raw(query)


    def num_banks(self):
        return len(self.values_list('idrssd', flat=True).distinct())



class Report(models.Model):
    idrssd = models.PositiveIntegerField()
    date = models.DateField()
    name = models.CharField(max_length=255)

    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=16)
    zipcode = models.PositiveIntegerField()

    assets = models.PositiveIntegerField()
    deposits = models.PositiveIntegerField()
    liabilities = models.PositiveIntegerField()


    objects = ReportManager()


    def __unicode__(self):
        return model_unicode(self, (
            'idrssd', 'date', 'name', 'address', 'city', 'state', 'zipcode',
            'assets', 'deposits', 'liabilities'
        ))
