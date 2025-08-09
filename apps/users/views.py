# apps/users/views.py
from django.shortcuts import render, redirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.views import View
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.users.models import *
from apps.users.serializers import *
# from common.permissions import IsOwnerOrReadOnly
from apps.users.forms import UserRegisterForm



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   AUTHENTICATION  &  AUTHORISATION   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# Автосохранение и автоиспользование JWT токенов.
# Вспомогательная функция для установки cookie:
def set_jwt_cookies(response, user):
    """
    Function for setting cookies.
    """
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token

    response.set_cookie(
        key='access_token',
        value=str(access_token),
        httponly=True,
        secure=False,                            #  NB! True на проде
        samesite='Lax'
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh),
        httponly=True,
        secure=False,
        samesite='Lax'
    )


# --------------------------------------------------------------------------------------
# РЕГИСТРАЦИЯ пользователя с JWT:
# Через APIView, которое не работает:
# class RegistrationView(APIView):
#     """
#     Registration of new user.
#     """
#     permission_classes = [AllowAny]
#
#     def get(self, request):
#         return Response(
#             {"detail": "Пожалуйста, отправьте POST-запрос с данными для регистрации."},
#             status=status.HTTP_405_METHOD_NOT_ALLOWED
#         )
#
#     def post(self, request):
#         serializer = UserRegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             # Создаем ответ с данными пользователя:
#             response = Response({
#                 'user': {
#                     'username': user.username,
#                     'email': user.email
#                 }
#             }, status=status.HTTP_201_CREATED)
#
#             # Вызываем функцию, чтобы добавить cookie с токенами в ответ:
#             set_jwt_cookies(response, user)
#
#             return response
#
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# адаптировать `RegistrationView` к обычному Django `View`, чтобы заработало:
# Смотри здесь https://chatgpt.com/s/t_6893b50349748191a5c9290a4875d308
class RegistrationView(View):
    """
    Registration of new user.
    """
    permission_classes = [AllowAny]
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Создаём пользователя
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Создаём профиль
            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role'],
                phone_number=form.cleaned_data['phone_number']
            )
            # Отправляем куки с токенами
            response = render(request, 'users/register_success.html', {'user': user})
            set_jwt_cookies(response, user)
            return response
        else:
            # Если форма не валидна — показать ошибки:
            return render(request, 'users/register.html', {'form': form})




# --------------------------------------------------------------------------------------
# Реализация ЛОГИНА с сохранением токенов в куки:
class LoginView(APIView):
    """
    Login to account. Dict example: { "email": "<your email>", "password": "<your password>" }
    """
    # Разрешаем доступ всем (даже анонимным пользователям), чтобы они могли войти:
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'detail': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # В authenticate передаём username=email, потому что User использует username как логин по умолчанию
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            return Response({'detail': 'User with this email not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            response = Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)

            # Устанавливаем токены в куки, если нужно
            set_jwt_cookies(response, user)

            return response

        return Response({'detail': 'Incorrect password.'}, status=status.HTTP_401_UNAUTHORIZED)

# --------------------------------------------------------------------------------------
# РАЗЛОГИНИВАНИЕ пользователя с JWT:
class LogoutView(APIView):
    """
    Logout from an account.
    """
    def post(self, request, *args, **kwargs):
        # Создаем пустой ответ:
        response = Response(data={'message': 'Logout successful'}, status=status.HTTP_204_NO_CONTENT)
        # Отправляем команду браузеру на удаление cookie:
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response





# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        OTHER  VIEWS      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# NB!  ModelViewSet - для каждой модели используется ЕДИНОЖДЫ.

# Получение для Админов:
#       сокращенного списка пользователей (ListUserSerializer)
#   ИЛИ детальной информации (DetailUserSerializer)
#   ИЛИ создания / обновления пользователей:
class UserViewSet(viewsets.ModelViewSet):
    """
    This view provides a complete set of CRUD actions for the UserProfile model.
    API endpoint that allows users' profiles to be VIEWED or EDITED.
    Get list of users for ADMIN.
    """
    queryset = User.objects.all()

    # Подключение бэкендов для фильтрации, поиска и сортировки для модели User:
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # Поля, по которым можно будет точно фильтровать (username=...):
    filterset_fields = ['first_name', 'last_name', 'username', 'email', 'date_joined']      # 'profile__role',
    # Поля, по которым будет работать полнотекстовый поиск (search=...):
    search_fields = ['last_name', 'email']
    # Поля, по которым можно будет сортировать (ordering=...):
    ordering_fields = ['profile__created_at']

    # Настройка JWT-Authentication:
    # Явно указываем классы аутентификации для этого представления.
    # Это переопределит глобальные настройки, если они есть.
    authentication_classes = [JWTAuthentication]

    # Явно указываем классы разрешений для этого представления:
    permission_classes = [IsAdminUser]

    # _____  Переопределяем метод ViewSet  ______
    # Этот метод позволяет динамически выбирать сериалайзер:
    def get_serializer_class(self):
        # Для безопасных методов (только чтение), таких, как GET:
        if self.action == 'list':
            return ListUserSerializer
        elif self.action == 'retrieve':
            return DetailUserSerializer
        # Для остальных методов (POST, PUT, DELETE):
        return CreateUpdateUserSerializer

