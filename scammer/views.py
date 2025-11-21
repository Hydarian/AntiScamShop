from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.views.generic import FormView, ListView, DetailView, View, TemplateView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SearchForm
from .models import TheShop, Image


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


class LikeShop(LoginRequiredMixin, View):
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


class DisLikeShop(LoginRequiredMixin, View):
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


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'pages/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_posts'] = TheShop.objects.filter(author=self.request.user).order_by('-created')
        return context


class CreatePost(LoginRequiredMixin, CreateView):
    model = TheShop
    fields = ['name', 'slug', 'description']
    template_name = 'pages/theshop_form.html'
    success_url = reverse_lazy('scam:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        if self.request.FILES:
            for f in self.request.FILES.getlist('images'):
                Image.objects.create(shop=self.object, img_file=f)
        return response
