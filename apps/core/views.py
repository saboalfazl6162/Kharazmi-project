from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from apps.news.models import Post
from apps.users.models import CustomUser,MainPoint

class HomePageView(TemplateView):
    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ["home.html"]
        return ["index.html"]    
class AboutPageView(TemplateView):
    template_name = "about_us.html"

class ContactPageView(TemplateView):
    template_name = "contact_us.html"


class GlobalSearchView(TemplateView):
    template_name = 'global_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query', '').strip()

        posts = Post.objects.none()
        users = CustomUser.objects.none()
        mainpoints = MainPoint.objects.none()

        if query:
            mainpoints = MainPoint.objects.all()
            posts = Post.objects.filter(
                Q(title__icontains=query) |
                Q(short_description__icontains=query) |
                Q(description__icontains=query) |
                Q(meta_name__icontains=query) |
                Q(meta_description__icontains=query) |
                Q(meta_keywords__icontains=query)
            )
            users = CustomUser.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(bio__icontains=query)
            )

        post_paginator = Paginator(posts, 10)
        post_page_number = self.request.GET.get('post_page')
        post_page_obj = post_paginator.get_page(post_page_number)

        user_paginator = Paginator(users, 10)
        user_page_number = self.request.GET.get('user_page')
        user_page_obj = user_paginator.get_page(user_page_number)

        mainpoint_paginator = Paginator(mainpoints, 10)
        mainpoint_page_number = self.request.GET.get('mainpoint_page')
        mainpoint_page_obj = mainpoint_paginator.get_page(mainpoint_page_number)

        mainpoints_with_posts = []
        for mp in mainpoint_page_obj:
            related_posts = posts.filter(post_mainpoint=mp)
            mainpoints_with_posts.append({
                'mainpoint': mp,
                'posts': related_posts
            })

        context.update({
            'query': query,
            'post_page_obj': post_page_obj,
            'user_page_obj': user_page_obj,
            'mainpoints_with_posts': mainpoints_with_posts,
            'mainpoint_page_obj': mainpoint_page_obj,
        })

        return context
