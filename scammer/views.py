from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import FormView, ListView
from .forms import SearchForm
from .models import TheShop


# Create your views here.


class Index(FormView):
    template_name = 'pages/index.html'
    form_class = SearchForm


class SearchResult(ListView):
    template_name = 'pages/result_search.html'

    def get(self, request, *args, **kwargs):
        self.query = request.GET.get('query')
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            self.result = TheShop.objects.filter(name__icontains=query)
        else:
            self.result = TheShop.objects.none()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['result'] = self.result
        context['query'] = self.query
        return context
    
    def get_queryset(self):
        return self.result
