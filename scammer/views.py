from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, JsonResponse
from django.views.generic import FormView, ListView, DetailView, View, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from . import urls
from .forms import SearchForm, CommentForm
from .models import TheShop, Image, Comment


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


class DetailShop(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'pages/detail.html'
    model = TheShop
    form_class = CommentForm


    def get_object(self):
        self.shop = get_object_or_404(TheShop, id=self.kwargs['pk'], slug=self.kwargs['slug'])
        return self.shop

    def get_success_url(self):
        return reverse("scam:detail", kwargs={"pk": self.object.pk, 'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop'] = self.shop
        context['form'] = self.get_form
        context['comments'] = self.shop.comments.all()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.shop = self.object
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

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


class EditPost(LoginRequiredMixin, UpdateView):
    model = TheShop
    fields = ['name', 'slug', 'description']
    template_name = "pages/theshop_update_form.html"
    success_url = reverse_lazy('scam:profile')

    def form_valid(self, form):
        response = super().form_valid(form)

        # گرفتن فایل تصویر جدید، اختیاری
        img_file = self.request.FILES.get('img_file')
        if img_file:
            # فقط وقتی کاربر فایل جدید انتخاب کرد، تصویر جدید ایجاد می‌کنیم
            Image.objects.create(shop=self.object, img_file=img_file)

        # اگر هیچ فایلی انتخاب نشده، تصویر قبلی دست نخورده می‌مونه
        return response


class DeletePost(LoginRequiredMixin, DeleteView):
    model = TheShop
    success_url = reverse_lazy('scam:profile')
    template_name = 'pages/theshop_confirm_delete.html'


