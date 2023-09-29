from django.shortcuts import redirect
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView, DeleteView

PER_PAGE = 6


class PostListView(ListView):
    template_name = 'blog/pages/index.html'
    queryset = Post.objects.get_published()
    paginate_by = PER_PAGE
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Home -'
        return context


class CreatedByListView(PostListView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._temp_context = {}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        page_title = 'Posts de ' + user_full_name + ' - '

        ctx.update({
            'page_title': page_title,
        })

        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)
        return qs

    def get(self, request, *args, **kwargs):
        _id = self.kwargs.get('_id')
        user = User.objects.filter(pk=_id).first()

        if user is None:
            raise Http404

        self._temp_context.update({
            '_id': _id,
            'user': user,
        })

        return super().get(request, *args, **kwargs)


class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self):
        return super().get_queryset().filter(
            category__slug=self.kwargs['slug']
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = f'{self.object_list[0].category.name} - Categoria'
        return ctx


class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self):
        return super().get_queryset().filter(
            tags__slug=self.kwargs['slug']
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = f'{self.object_list[0].tags.first().name} - Tag -'
        return ctx


class SearchListView(PostListView):
    def __init__(self, *agrs, **kwargs) -> None:
        super().__init__(*agrs, **kwargs)
        self._search_value = ''

    def setup(self, request, *args, **kwargs) -> None:
        self._search_value = request.GET.get('search').strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset().filter(
            Q(title__icontains=self._search_value) |
            Q(exerpt__icontains=self._search_value) |
            Q(content__icontains=self._search_value)
        )[0:PER_PAGE]
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['page_title'] = f'{self._search_value[:20]} - Search -'
        ctx['search_value'] = self._search_value
        return ctx

    def get(self, request, *args, **kwargs):
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)


class PageDetailView(DeleteView):
    model = Page
    template_name = 'blog/pages/page.html'
    slug_field = 'slug'
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        print(ctx)
        single_page = self.get_object()
        ctx['page_title'] = f'{single_page.title} - Página -'
        return ctx

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class PostDetailView(DeleteView):
    model = Post
    template_name = 'blog/pages/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        single_post = self.get_object()
        ctx['page_title'] = f'{single_post.title} - Post -'
        return ctx

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)
