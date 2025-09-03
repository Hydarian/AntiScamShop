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
    paginate_by = 1
    model = TheShop

    def get_queryset(self):
        self.query = self.request.GET.get('query')
        form = SearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            self.result = TheShop.objects.filter(name__icontains=query)
            return self.result  # اینجا حتما باید queryset واقعی رو برگردونی
        self.result = TheShop.objects.none()
        return self.result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        return context
    
