from django.http import Http404
from django.views.generic import ListView

from reports.models import Report
from reports.util import IndexableQuery



class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'banks'
    paginate_by = 100


    def __init__(self, *args, **kwargs):
        super(IndexView, self).__init__(*args, **kwargs)
        self.num_banks = Report.objects.num_banks()


    def get_queryset(self):
        return IndexableQuery(self.num_banks, Report.objects.most_recent)


    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['num_banks'] = self.num_banks
        return context



class BankView(ListView):
    template_name = 'bank.html'
    context_object_name = 'reports'


    def get_queryset(self):
        qs = Report.objects \
            .filter(idrssd=self.kwargs['idrssd']) \
            .order_by('-date')

        if not qs.exists():
            raise Http404

        return list(qs)
