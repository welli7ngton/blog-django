from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Post

PER_PAGE = 9


def index(request):
    posts = Post.objects.get_published()
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def created_by(request, _id):
    posts = Post.objects.get_published().filter(created_by__pk=_id)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def category(request, slug):
    posts = Post.objects.get_published().filter(category__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def tag(request, slug):
    posts = Post.objects.get_published().filter(tags__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def page(request, slug):
    return render(
        request,
        'blog/pages/page.html',
        {
            # 'page_obj': page_obj,
        }
    )


def post(request, slug):

    single_post = Post.objects.get_published().filter(slug=slug).first()

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': single_post,
        }
    )
