from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView

PER_PAGE = 2


class PostListView(ListView):
    template_name = 'blog/pages/index.html'
    queryset = Post.objects.get_published()
    ordering = ('-pk',)
    paginate_by = PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Home -'
        return context

# Function based view Index

# def index(request):
#     posts = Post.objects.get_published()
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': 'Home',
#         }
#     )


def created_by(request, _id):
    posts = Post.objects.get_published().filter(created_by__pk=_id)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    user = User.objects.filter(pk=_id).first()

    if user is None:
        raise Http404()

    if user.first_name:
        user_name = f'{user.first_name} {user.last_name}'

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': f'{user_name} posts -',
        }
    )


def category(request, slug):
    posts = Post.objects.get_published().filter(category__slug=slug)

    if len(posts) == 0:
        raise Http404()

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': f'{page_obj[0].category.name} - Categoria -',
        }
    )


def tag(request, slug):
    posts = Post.objects.get_published().filter(tags__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404()

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': f'{page_obj[0].tags.first().name} - Tag -',

        }
    )


def search(request):
    search_value = request.GET.get('search').strip()
    posts = Post.objects.get_published().filter(
        Q(title__icontains=search_value) |
        Q(exerpt__icontains=search_value) |
        Q(content__icontains=search_value)
    )[0:PER_PAGE]

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
            'page_title': f'{search_value[:20]} - Search -',
        }
    )


def page(request, slug):
    single_page = (
        Page.objects
        .filter(is_published=True)
        .filter(slug=slug)
        .first()
    )

    if single_page is None:
        raise Http404()

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': single_page,
            'page_title': f'{single_page.title} - Página -',
        }
    )


def post(request, slug):

    single_post = Post.objects.get_published().filter(slug=slug).first()

    if single_post is None:
        raise Http404()

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': single_post,
            'page_title': f'{single_post.title}',
        }
    )
