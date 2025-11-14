from django.contrib import messages
from django.shortcuts import redirect,get_object_or_404,render
from django.views.generic import ListView,CreateView,UpdateView,DetailView,View,FormView
from .models import Post
from .forms import PostCreateForm
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.core.models import Comment
from apps.core.forms import CommentForm
from django.db.models import Q


class PostListView(ListView):
    model = Post
    template_name = "blog_list.html"
    context_object_name = "posts"
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get('query', '').strip()
        queryset = Post.objects.filter(is_active=True)

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(short_description__icontains=q) |
                Q(description__icontains=q) |
                Q(meta_name__icontains=q) |
                Q(meta_description__icontains=q) |
                Q(meta_keywords__icontains=q)
            )

        return queryset.order_by("-is_pin", "-write_date")



class PostCreateView(LoginRequiredMixin,CreateView):
    template_name = 'post_create.html'
    form_class = PostCreateForm
    success_url = reverse_lazy('blog-page')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.is_active = False
        post.is_verify = False
        post.is_pin = False

        posts = Post.objects.filter(author=self.request.user)
        if posts.count() > 10:
            post.is_active = True

        one_day_ago = timezone.now() - timedelta(days=1)
        posts_today = Post.objects.filter(author=self.request.user, write_date__gte=one_day_ago)
        
        if posts_today.count() > 10 and not self.request.user.is_staff:
            messages.warning(self.request,"شما بیش از 10 مقاله نوشتید!")
            return redirect("home-page")

        post.save()
        messages.success(self.request, "مقاله شما ثبت شد.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "لطفاً خطاهای فرم را بررسی کنید.")
        return super().form_invalid(form)




class PostDetailView(DetailView, FormView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy("post-detail-page", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["comments"] = Comment.objects.filter(to=post, reply_to__isnull=True,is_active=True)
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        post = Post.objects.get(id=self.object.pk)
        form = self.get_form()
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.to = self.object

            reply_to_id = request.POST.get("reply_to")
            if reply_to_id:
                comment.reply_to = get_object_or_404(Comment, id=reply_to_id)
            if post.author.confirmation_comments:
                comment.is_active = True
                comment.is_check_of_author_post = True
            else:
                comment.is_check_of_author_post = False
                comment.is_active = False
            comment.save()
            messages.success(request, "نظر شما با موفقیت ثبت شد.")
            return redirect(self.get_success_url())

        return self.form_invalid(form)



class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = "post_update.html"
    pk_url_kwarg = "id"
    context_object_name = "post"
    success_url = reverse_lazy("blog-page")
    def form_valid(self, form):
        messages.success(self.request,"پست تغییر یافت")
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin,View):
    def get(self,request,pk):
        post = get_object_or_404(Post, pk=pk)
        
        if post.author != self.request.user and not self.request.user.is_staff:
            messages.error(request,"شما به این پست دسترسی ندارید")
            return render(request,'blog_list.html',)    
        return render(request,'post_delete.html',{'post':post})
    
    def post(self, request, pk):

        post = get_object_or_404(Post, pk=pk)
        post.is_active = False
        post.save()
        messages.success(request,"پست با موفقیت حذف شد")
        return redirect('home-page')

class CommentDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.author == request.user or request.user.is_staff:
            comment.is_active = False
            messages.success(request, "نظر با موفقیت حذف شد.")
        else:
            messages.error(request, "شما اجازه‌ی حذف این نظر را ندارید.")
        return redirect(request.META.get('HTTP_REFERER', 'home-page'))