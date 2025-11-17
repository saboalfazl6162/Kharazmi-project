from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser,MainPoint,MiniMainPoint
from django import forms
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    model = CustomUser

    class meta:
        fields = ("username", "email", "first_name", "last_name", "phone_number")


class CustomUserChangeForm(UserChangeForm):
    model = CustomUser

    class meta:
        fields = "__all__"

class MainPointForm(forms.Form):
    FIELDS = [
    "بازارچه کسب و کار دانش آموزش",
    "بازی های مهارتی و توسعه فردی",
    "برنامه نویسی",
    "دست سازه",
    "ریاضی",
    "زبان خارجی",
    "زبان و ادبیات فارسی",
    "سلامت و تربیت بدنی",
    "فرهنگ و هنر",
    "فعالیت های آزمایشگاهی",
    "قرآن و معارف اسلامی",
    "مطالعات اجتماعی",
    "پژوهش",
]
    main_point = forms.ModelChoiceField(
        queryset=MainPoint.objects.none(),
        label="",
        empty_label="انتخاب محور",
        widget=forms.Select(attrs={
            "class": "pes pes category-select",
        })
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.FIELDS:
            MainPoint.objects.get_or_create(name=name)
        self.fields['main_point'].queryset = MainPoint.objects.all()

class SignUpForm(forms.Form):
    mini_mainpoint = forms.ModelChoiceField(
        queryset=MiniMainPoint.objects.none(),
        label="",
        required=False,
        widget=forms.Select(attrs={
            "class": "pes pes category-select",
        })
    )
    username = forms.CharField(
        label='',
        max_length=110,
        validators=[RegexValidator(r"^[\w.@+-]+$")],
        widget=forms.TextInput(attrs={"placeholder": _("نام کاربری"),"class":"pes pes pes pes1"}),
    )
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": _("نام"),"class":"pes pes pes pes2"}),
        required=False,
        label='',
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": _("نام خانوادگی"),"class":"pes pes pes pes3"}),
        required=False,
        label='',
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": _("ایمیل"),"class":"pes pes pes pes4"}),
        required=False,
        label='',
    )
    phone_number = forms.CharField(
        max_length=15,
        validators=[RegexValidator(r"^\+?\d{10,15}$")],
        widget=forms.TextInput(attrs={"placeholder": _("شماره تلفن"),"class":"pes pes pes pes6"}),
        required=False,
        label='',
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={"placeholder": _("گذرواژه"),"class":"pes pes pes pes7"}),
    )
    password_confirm = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={"placeholder": _("تایید گذرواژه",),"class":"pes pes pes pes8"}),
    )
    def __init__(self, *args, **kwargs):
        main_point = kwargs.pop('mainpoint', None)
        super().__init__(*args, **kwargs)
        if main_point:
            self.fields['mini_mainpoint'].queryset = MiniMainPoint.objects.filter(main_mainpoint=main_point)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        email = cleaned_data.get("email")
        phone_number = cleaned_data.get("phone_number")

        if password != password_confirm:
            raise forms.ValidationError(_("دو فیلد گذرواژه با هم مطابقت ندارند"))

        if not email and not phone_number:
            raise forms.ValidationError(_("باید حتما شماره تلفن یا ایمیل داشته باشید"))
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(
        required=False,
        label='',
        max_length=110,
        validators=[RegexValidator(r"^[\w.@+-]+$")],
        widget=forms.TextInput(attrs={"placeholder": _("نام کاربری"),"class":"pes pes1"}),
    )
    phone_number = forms.CharField(
        max_length=15,
        validators=[RegexValidator(r"^\+?\d{10,15}$")],
        widget=forms.TextInput(attrs={"placeholder": _("شماره تلفن"),"class":"pes pes2"}),
        required=False,
        label="",
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": _("ایمیل"),"class":"pes pes3"}),
        required=False,
        label='',
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={"placeholder": _("گذرواژه"),"class":"pes pes4"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        phone_number = cleaned_data.get("phone_number")
        username = cleaned_data.get("username")

        if not email and not phone_number and not username:
            raise forms.ValidationError(
                _(
                    "برای ورود حداقل یا شماره تلفن،یا ایمیل یا نام کاربری خود را وارد کنید"
                )
            )
        return cleaned_data
