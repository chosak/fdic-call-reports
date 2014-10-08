from datetime import date
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.generic import View

from reports.dynamo import DynamoTable



class IndexView(View):
    def __init__(self):
        self.cache = cache


    def get(self, request):
        page = request.GET.get('page')
        banks, page_number, has_previous, has_next = self.banks_for_page(page)

        context = {
            'banks': banks,
            'page': page_number,
            'has_previous': has_previous,
            'has_next': has_next,
        }

        return render(request, 'index.html', context)


    def banks_for_page(self, page):
        cache_key = self.cache_key(page)

        bank_data = self.cache.get(cache_key)
        if bank_data is not None:
            return bank_data

        paginator = Paginator(self.get_banks(), 25)
        try:
            banks = paginator.page(page)
        except PageNotAnInteger:
            banks = paginator.page(1)
        except EmptyPage:
            banks = paginator.page(paginator.num_pages)
    
        bank_data = (
            banks.object_list,
            banks.number,
            banks.has_previous(),
            banks.has_next()
        )
        self.cache.set(cache_key, bank_data, timeout=None)
        return bank_data


    def cache_key(self, page):
        try:
            page = int(page)
        except (TypeError, ValueError):
            page = 1

        return 'banks-{}'.format(page)


    def get_banks(self):
        table = DynamoTable('banks')
        results = table.get_table().scan()

        return [self.bank_from_row(row) for row in results]


    def bank_from_row(self, row):
        return {
            'idrssd': row['idrssd'],
            'name': row['name'],
            'address': row['address'],
            'city': row['city'],
            'state': row['state'],
            'zip': row['zip'],
            'last_report': self.last_report(row['report_date']),
        } 


    def last_report(self, mmddyyyy):
        y = int(mmddyyyy[4:])
        m = int(mmddyyyy[:2])
        d = int(mmddyyyy[2:4])
        return date(y, m, d).isoformat()
