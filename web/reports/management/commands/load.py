import json

from datetime import datetime
from django.core.management import BaseCommand, CommandError
from optparse import make_option

from reports.models import Bank, Report



class Command(BaseCommand):
    help = 'load bank data into database'


    option_list = BaseCommand.option_list + (
        make_option('-f', '--filename', help='input filename'),
    )


    def handle(self, *args, **kwargs):
        filename = kwargs['filename']

        if filename is None:
            raise CommandError('filename')

        Bank.objects.all().delete()

        with open(filename, 'rb') as f:
            for bank_json in map(json.loads, f):
                self.load_bank(bank_json)


    def load_bank(self, bank_json):
        bank = Bank.objects.create(idrssd=bank_json['IDRSSD']) 
        print('loaded bank {}'.format(bank))

        reports = Report.objects.bulk_create([
            self.construct_report(bank.pk, r) for r in bank_json['reports']
        ])
        print('loaded {} reports'.format(len(list(reports))))


    def construct_report(self, bank_id, report_json):
        report_json['date'] = datetime.strptime(
            report_json['date'],
            '%m%d%Y'
        ).date()
        report_json['zipcode'] = report_json.pop('zip')

        return Report(bank_id=bank_id, **report_json)
