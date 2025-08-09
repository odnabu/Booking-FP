# Django-форма UserRegisterForm для регистрации нового пользователя.
# Смотри:
#   - реализация форм: https://chatgpt.com/s/t_6893b3d1ec7881918bd7ff040240ed52.
#   - валидация данных: https://chatgpt.com/s/t_6894427e82588191b2cb6feddd3dec2b.
from django import forms
from django.contrib.auth.models import User
from apps.users.models import UserProfile


class UserRegisterForm(forms.ModelForm):
    # Поля, которых нет в модели User напрямую:
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'phone_number']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email is already registered.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if UserProfile.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("A user with this phone number is already registered.")
        return phone_number

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("The username is already taken.")
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        # Можно добавить дополнительные проверки: хотя бы 1 цифра, заглавная буква и т.п.
        return password

