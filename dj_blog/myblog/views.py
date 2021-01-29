from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentForm, PostForm
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.generic import CreateView


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def index(request):
    categories = Category.objects.all()
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    paginator = Paginator(queryset, 10)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {
        'categories': categories,
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
        'q_search': query
    }
    return render(request, 'index.html', context)

@login_required
def blog_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("blog", kwargs={
                'blog_id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)

@login_required
def blog_update(request, blog_id):
    title = 'Update'
    blog_post = get_object_or_404(Post, id=blog_id)
    form = PostForm(request.POST or None, request.FILES or None, instance=blog_post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("blog", kwargs={
                'blog_id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)

@login_required
def blog_delete(request, blog_id):
    blog_post = get_object_or_404(Post, id=blog_id)
    blog_post.delete()
    return redirect("index")


def blog(request, blog_id):
    categories = Category.objects.all()
    blog_post = get_object_or_404(Post, id=blog_id)
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = blog_post
            form.save()
            return redirect('blog', blog_id=blog_id)
    context = {
        'categories': categories,
        'form': form,
        'blog': blog_post
    }
    return render(request, 'blog.html', context)


def category_view(request, cats):
    categories = Category.objects.all()
    category_post = Post.objects.filter(categories__title__contains=cats)
    context = {
        'categories': categories,
        'cats': cats,
        'category_post': category_post
    }
    return render(request, 'categories.html', context)


class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('index')
