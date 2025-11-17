from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login,logout
from django.views.generic import FormView,View,DetailView
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.shortcuts import redirect,render
from .forms import SignUpForm,LoginForm,MainPointForm
from .models import CustomUser,MainPoint,MiniMainPoint
from apps.news.models import Post

class SelectMainPointView(FormView):
    template_name = "select_mainpoint.html"
    form_class = MainPointForm
    
    def form_valid(self, form):
        main_point_id = form.cleaned_data['main_point'].id
        signup = reverse("signup")
        response = redirect(signup)
        response.set_cookie('selected_main_point', main_point_id, max_age=86400)
        
        return response

class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('home-page')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        
        main_point_id = self.request.COOKIES.get('selected_main_point')
        mainpoint = None
        if main_point_id:
            try:
                mainpoint = MainPoint.objects.get(id=int(main_point_id))
            except MainPoint.DoesNotExist:
                mainpoint = None
        
        kwargs['mainpoint'] = mainpoint
        return kwargs

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        phone_number = form.cleaned_data['phone_number']
        if CustomUser.objects.filter(username=username).exists():
            messages.error(self.request, "این نام کاربری قبلاً انتخاب شده است.")
            return redirect('signup')

        if CustomUser.objects.filter(email=email).exists() and email!='':
            messages.error(self.request, "این ایمیل قبلاً ثبت شده است.")
            return redirect('signup')

        if CustomUser.objects.filter(phone_number=phone_number).exists() and phone_number!='':
            messages.error(self.request, "این شماره قبلاً ثبت شده است.")
            return redirect('signup')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            phone_number=form.cleaned_data['phone_number'],
            main_point =form.cleaned_data['main_point'],
        )
        user.save()
        login_user = authenticate(self.request, username=user.username,password=form.cleaned_data['password'],)
        if login_user is not None:
            login(self.request, login_user)
        else:
            messages.error(self.request,"مشکلی در ورود پیش آمده،لطفا به طور دستی وارد شوید و اگر ارور گرفتید،دوباره ثبت نام کنید")
            return redirect('login')

        messages.success(self.request, "ثبت‌نام با موفقیت انجام شد ✅")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "لطفاً خطاهای فرم را بررسی کنید.")
        return super().form_invalid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.COOKIES.get('selected_main_point'):
            return redirect('select-mainpoint')
        return super().dispatch(request, *args, **kwargs)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone_number')
        password = form.cleaned_data.get('password')

        user = None

        if username:
            user = authenticate(self.request, username=username, password=password)
        elif email:
            try:
                u = CustomUser.objects.get(email=email)
                user = authenticate(self.request, username=u.username, password=password)
            except CustomUser.DoesNotExist:
                user = None
        elif phone:
            try:
                u = CustomUser.objects.get(phone_number=phone)
                user = authenticate(self.request, username=u.username, password=password)
            except CustomUser.DoesNotExist:
                user = None

        if user is not None:
            login(self.request, user)
            messages.success(self.request, _("ورود با موفقیت انجام شد ✅"))
            return redirect(self.get_success_url())
        else:
            messages.error(self.request, _("نام کاربری، ایمیل یا گذرواژه اشتباه است."))
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("لطفاً خطاهای فرم را بررسی کنید."))
        return super().form_invalid(form)

class LogoutView(LoginRequiredMixin,View):
    
    def get(self,request):
        return render(request,"logout_confirm.html")
    
    def post(self,request):
        logout(request)
        messages.success(request,"با موفقیت خارج شدید")
        return redirect("home-page")
    
class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "profile_detail.html"
    context_object_name = "account"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(author=self.request.user)
        return context

class UserDetailView(DetailView):
    model = CustomUser
    template_name = "profile_detail.html"
    context_object_name = "account"

    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(author=self.object)
        return context
