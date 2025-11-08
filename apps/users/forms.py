from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser,MainPoint
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


class SignUpForm(forms.Form):
    FIELDS = FIELDS = [
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

    for name in FIELDS:
        MainPoint.objects.get_or_create(name=name)


    main_point = forms.ModelChoiceField(
        queryset=MainPoint.objects.all(),
        label="محور مورد نظر",
        empty_label="انتخاب کنید"
    ) 
    username = forms.CharField(
        label=_("نام کاربری"),
        max_length=110,
        validators=[RegexValidator(r"^[\w.@+-]+$")],
        widget=forms.TextInput(attrs={"placeholder": _("نام کاربری")}),
    )
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": _("نام")}),
        required=False,
        label=_("نام"),
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": _("نام خانوادگی")}),
        required=False,
        label=_("نام خانوادگی"),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": _("ایمیل")}),
        required=False,
        label=_("ایمیل"),
    )
    phone_number = forms.CharField(
        max_length=15,
        validators=[RegexValidator(r"^\+?\d{10,15}$")],
        widget=forms.TextInput(attrs={"placeholder": _("شماره تلفن")}),
        required=False,
        label=_("شماره تلفن"),
    )
    password = forms.CharField(
        label=_("گذرواژه"),
        widget=forms.PasswordInput(attrs={"placeholder": _("گذرواژه")}),
    )
    password_confirm = forms.CharField(
        label=_("تائید گذرواژه"),
        widget=forms.PasswordInput(attrs={"placeholder": _("تایید گذرواژه")}),
    )

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
        label=_("username"),
        max_length=110,
        validators=[RegexValidator(r"^[\w.@+-]+$")],
        widget=forms.TextInput(attrs={"placeholder": _("نام کاربری")}),
    )
    phone_number = forms.CharField(
        max_length=15,
        validators=[RegexValidator(r"^\+?\d{10,15}$")],
        widget=forms.TextInput(attrs={"placeholder": _("شماره تلفن")}),
        required=False,
        label=_("شماره تلفن"),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": _("ایمیل")}),
        required=False,
        label=_("ایمیل"),
    )
    password = forms.CharField(
        label=_("گذرواژه"),
        widget=forms.PasswordInput(attrs={"placeholder": _("گذرواژه")}),
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
