from .models import Post, Book_User
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, Http404
from django.core.paginator import Paginator
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.views.generic.base import View
from django.core.exceptions import ObjectDoesNotExist
from blog.forms import BookForm
from django.shortcuts import render
from django.http import HttpResponse


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "blog/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "blog/login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    success_url = "/"

    def get(self, request):
        return_path = request.META.get('HTTP_REFERER', '/')
        logout(request)
        return redirect(return_path)


def post_list(request, page_number=1):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    current_page = Paginator(posts, 3)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.ordered = '0'
            post.save()
            return redirect('bookexmp', pk=post.pk)
    else:
        form = BookForm()
    return render(request, 'blog/post_list.html', {'posts': current_page.page(page_number), 'form': form})


def books(request, pk):
    post = get_object_or_404(Post, pk=pk)
    book_user = Book_User.objects.filter(book=pk)
    return render(request, 'blog/bookexmp.html', {'post': post, 'book_user': book_user})


def test(request):
    return render(request, 'blog/siteshab.html', {})


def addtoorder(request, pk):
    try:
        return_path = request.META.get('HTTP_REFERER', '/')
        post = get_object_or_404(Post, pk=pk)
        post.ordered += 1
        post.save()
        if post.pk > 0:
            if Book_User.objects.filter(user=request.user.username, book=pk).exists():
                b_u = Book_User.objects.get(user=request.user.username, book=pk)
                b_u.number += 1
                b_u.save()
            else:
                b_u = Book_User(user=request.user.username, book=pk, number=1)
                b_u.save()
    except ObjectDoesNotExist:
        raise Http404
    return redirect(return_path)


def add(request):
    if request.method == "POST":
        form = BookForm(request.POST)
    else:
        form = BookForm()
    return render(request, 'blog/edit.html', {'form': form})


def contact(request):
    errors = []
    form = {}
    if request.POST:


        form['message'] = request.POST.get('message')


        if not form['message']:
            errors.append('Введите сообщение')

        if not errors:
            # ... сохранение данных в базу
            return HttpResponse('Спасибо за ваше сообщение!')

    return render(request, 'bookexmp.html', {'errors': errors, 'form': form})