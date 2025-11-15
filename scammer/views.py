from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.views.generic import FormView, ListView, DetailView, View
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
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
            return self.result
        self.result = TheShop.objects.none()
        return self.result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        return context


class DetailShop(DetailView):
    template_name = 'pages/detail.html'
    model = TheShop

    def get_object(self):
        self.shop = get_object_or_404(TheShop, id=self.kwargs['pk'], slug=self.kwargs['slug'])
        return self.shop

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop'] = self.shop
        return context


class LikeShop(View):
    http_method_names = ['post']

    def post(self, request):
        shop_id = request.POST.get('shop_id')

        if shop_id is not None:
            shop = get_object_or_404(TheShop, id=shop_id)
            user = request.user
            if user in shop.like.all():
                shop.like.remove(user)
            else:
                shop.like.add(user)
                if user in shop.dislike.all():
                    shop.dislike.remove(user)

            shop_dislikes_count = shop.dislike.count()
            shop_likes_count = shop.like.count()

            response_data = {
                'likes_count': shop_likes_count,
                'dislikes_count': shop_dislikes_count,
            }
        else:
            response_data = {
                'error': 'invalid shop id!'
            }

        return JsonResponse(response_data)


class DisLikeShop(View):
    http_method_names = ['post']

    def post(self, request):
        shop_id = request.POST.get('shop_id')

        if shop_id is not None:
            shop = get_object_or_404(TheShop, id=shop_id)
            user = request.user

            if user in shop.dislike.all():
                shop.dislike.remove(user)
            else:
                shop.dislike.add(user)

                if user in shop.like.all():
                    shop.like.remove(user)

            shop_dislikes_count = shop.dislike.count()
            shop_likes_count = shop.like.count()
            response_data = {
                'likes_count': shop_likes_count,
                'dislikes_count': shop_dislikes_count,

            }
        else:
            response_data = {
                'error': 'invalid shop id!'
            }

        return JsonResponse(response_data)


class Login(LoginView):
    authentication_form = AuthenticationForm
    template_name = 'registration/login.html'
